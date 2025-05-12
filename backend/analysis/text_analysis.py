import os
import random

from huggingface_hub import InferenceClient

import requests
import json
import numpy as np
from scipy.stats import entropy
import time
from functools import lru_cache
from cachetools import LRUCache, cached, TTLCache
from dotenv import load_dotenv
from openai import OpenAI
import fitz

class text_analyzer:
    def __init__(self):
        self.model = "gpt-4o-mini"
        load_dotenv()

        self.hf_token = os.getenv("HF_TOKEN_SECONDARY")
        self.openai_api = os.getenv("OPENAI_API")

        self.model_response = None
        # For global cache accross users need to change this (also resets every class instance)
        self.cache = LRUCache(maxsize=100)
        self.client = OpenAI(api_key=self.openai_api)
        self.parsed_model_response = None
        self.sources = ""
        self.improved_text = ""

    
    def _cache_query_huggingface(self, model, payload_str):
        """Manually apply caching within the function."""
        cache_key = (model, payload_str)
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # If not cached, call the function and store the result
        result = None  # Replace with actual logic to fetch the result
        self.cache[cache_key] = result
        return result

    def update_cache(self, model, payload, result):
        payload_str = json.dumps(payload, sort_keys=True)
        self.cache[(model, payload_str)] = result

    def get_completions(self, messages, client, payload, model="gpt-4o-mini",buffer=100, max_tokens=500):
      # new_message = {"role": "assistant", "content": "Make sure your responses are complete and there are no cutoffs."}
      # messages.append(new_message)
      print("TOKEN", self.hf_token)
      completion = client.chat.completions.create(
                        model=model,
                        messages=messages
                        # max_tokens=max_tokens+buffer
                    )
      result = completion.choices[0].message.content
      self.update_cache(model, payload, result)
      return completion

    def read_file(self,file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    
    def get_message(self,system_context, user_context):
        messages = [
            {"role": "system", "content": system_context},
            {"role": "user", "content": user_context}
        ]
        return messages

    def query_llm_cache(self, model, payload, messages, client):
        """Uses cache first; if not found, queries the API."""
        # make sure cache is looked at first
        # model_result = None

        payload_str = json.dumps(payload, sort_keys=True)  # Ensure hashability
        result = self._cache_query_huggingface(model, payload_str)


        if result is not None:
            print("Cache hit!")
            return result
        else:
            print("Cache miss! Querying API...")
            _result = self.get_completions(messages=messages, client=client, model=model, payload=payload)
            return _result.choices[0].message.content
        
    def extract_text_from_pdf(pdf_path):
        with fitz.open(pdf_path) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
        return text

    # Step 1 call
    def analyze_text_llm(self,text):

        messages = [
            {"role": "system", "content": (f"You are like a turing machine that takes in text and only outputs the following..."
                                    f"A boolean for everything in the text that is either true, false, or null if validity is uncertain/unkown."
                                    f"A boolean for everything in the text that contains subjectivity/bias as either true, false, or the empty string if uncertain/unkown"
                                    f"The specific context or statement that influences the false, true, or unkowns analysis."
                                    f"A string that represents a reputable link to a source (i.e website/paper/book) to find more info about the topic and verify information, or null if there are no relevant sources."
                                    f"The improved/modfied version of the statement to reduce bias and falsity as a whole. If the needed change is unkown/uncertain include null. If no change is needed include an empty string."
                                    f"All outputs are in the form of a list of dictonaries where each dictonary contains the following key value pairs"
                                    f"key(Truth):bool (as true/false/null based on the truth of its central claim.), key(Biased):bool (as true/false/null), key(Improved): string (as a plausible modification to make statement true and or not biased), key(Reason): string (as the thorough reasoning behind the choices), and key(Context):string (as the entire influencing context/statement word for word line for line punctuation for punctuation)"
                                    f"key(TruthSources): string (as a reputable source(s) or website(s) for finding more info about the validity)"
                                    f"Be sure to keep the output in the form of a parseable list of dictonaries and nothing else. Ignore parts of the text that don't have either a true or bias aspect to them like the statement, hello how are you."
                                    f"Most importantly, ensure that the entire text is segmented into reasonably sized and coherent chunks, where each chunk contains all necessary context to make each statement, assumption, or assertion made in the chunk understandable on its own.")},
            {"role": "user", "content": f"Text: {text}"}
        ]
        # combine system content with text for more detail when caching
        prompt_text = text + messages[0]["content"]

        result = self.query_llm_cache(messages=messages, model=self.model,payload=prompt_text, client=self.client)

        # ignore cache
        # result = get_completions(messages=messages, client=client, model="Qwen/Qwen2.5-Coder-32B-Instruct", payload=text)
        # result = result.choices[0].message.content
        print(result)
        self.model_response = result
        return result
    

    # Step 2 call
    def parse_json(self, input_data):
        """Parses JSON input and ensures it returns a list of dictionaries."""
        if isinstance(input_data, str):
            try:
                # input_data = input_data.strip()
                input_data = json.loads(input_data)  # Convert JSON string to Python object
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON input: {e}")

        if not isinstance(input_data, list):
            raise ValueError("Expected a list of dictionaries")

        parsed_data = []
        for entry in input_data:
            if isinstance(entry, dict):
                parsed_data.append(entry)
            else:
                raise ValueError("Each entry must be a dictionary")
        self.parsed_model_response = parsed_data
        return parsed_data
    
    # Change to take in account the entire text length instead
    def compute_relevance_scale(self,context, all_contexts_truth, all_contexts_bias):
        """Assigns a relevance score from 1 to 5 based on context length proportion."""
        max_length_bias = max(len(c) for c in all_contexts_bias) if all_contexts_bias else len(context)
        max_length_truth = max(len(c) for c in all_contexts_truth) if all_contexts_truth else len(context)
        return round((len(context) / max_length_truth) * 4) + 1, round((len(context) / max_length_bias) * 4) +1   # Scale from 1 to 5

    def compute_uncertain_relevance_scale(self,context, all_contexts):
        """Assigns a relevance score from 1 to 5 based on context length proportion."""
        max_length = max(len(c) for c in all_contexts) if all_contexts else 1
        print(all_contexts)
        print(len(context), max_length)
        return round((len(context) / max_length) * 4) + 1   # Scale from 1 to 5

    # Step 2 call
    def compute_overall_truth_bias(self,data):
        """Calculates overall truth and bias percentages based on weighted relevance."""

        total_truth_score = 0
        total_bias_score = 0
        total_uncertain_truth = 0
        total_uncertain_bias = 0
        total_weight_truth = 0
        total_weight_bias = 0
        total_weight_uncertain_truth = 0
        total_weight_uncertain_bias = 0
        all_contexts_truth = [entry["Context"] for entry in data if entry and entry["Truth"] != None]
        all_contexts_bias = [entry["Context"] for entry in data if entry and entry["Biased"] != None]
        all_contexts = [entry["Context"] for entry in data]

        contributions = []  # To store how each context contributes


        for entry in data:
            if entry:
                context = entry["Context"]
            else:
                continue



            truth_value = entry["Truth"]
            bias_value = entry["Biased"]
            relevance_truth, relevance_bias= self.compute_relevance_scale(context, all_contexts_truth, all_contexts_bias)  # 1-5 scale
            relevance_uncertain = self.compute_uncertain_relevance_scale(context, all_contexts=all_contexts)

            if truth_value is not None:
                truth_score = 100 if truth_value else 0
                total_truth_score += truth_score * relevance_truth
            else:
                truth_score = 100
                total_uncertain_truth += truth_score * relevance_uncertain

            if bias_value is not None:
                bias_score = 100 if bias_value else 0
                total_bias_score += bias_score * relevance_bias
            else:
                bias_score = 100
                total_uncertain_bias += bias_score * relevance_uncertain


            if truth_value is not None:
                total_weight_truth += relevance_truth
            else:
                total_weight_uncertain_truth += relevance_uncertain

            if bias_value is not None:
                total_weight_bias += relevance_bias
            else:
                total_weight_uncertain_bias += relevance_uncertain

            contributions.append({
                "Context": context,
                "Truth Contribution": truth_value if truth_value is not None else None,
                "Bias Contribution": bias_value if bias_value is not None else None,
                "Truth Relevance Scale (1-5)": relevance_truth,
                "Bias Relevance Scale (1-5)": relevance_bias,
                "Uncertaintly Relevance Scale (1-5)": relevance_uncertain,
                "Improved": entry["Improved"],
                "TruthSources": entry["TruthSources"],
                "Reason": entry["Reason"]

            })
        overall_truth = (total_truth_score / total_weight_truth) if total_weight_truth else 0
        overall_bias = (total_bias_score / total_weight_bias) if total_weight_bias else 0
        overall_uncertain_truth = (total_uncertain_truth / total_weight_uncertain_truth) if total_weight_uncertain_truth else 0
        overall_bias_uncertain = (total_uncertain_bias / total_weight_uncertain_bias) if total_weight_uncertain_bias else 0

        return {
            "Overall Truth Percentage": round(overall_truth, 2),
            "Overall Bias Percentage": round(overall_bias, 2),
            "Context Contributions": contributions,
            "Overall Uncertain Truth Percentage": round(overall_uncertain_truth, 2),
            "Overall Uncertain Bias Percentage": round(overall_bias_uncertain, 2)
        }
    
    # Step 3 call
    def display_improved_text(self, data):
        improved_text = ""
        for entry in data:
            if not entry:
                continue
            improved_text += f"{entry['Improved']}\n"
        self.improved_text = improved_text
        return improved_text

    # Step 4 call
    def display_sources(self,data):
        sources = ""
        for entry in data:
            if not entry:
                continue
            sources += f"Sources to verify {entry['Context']}: {entry['TruthSources']}\n"
        self.sources = sources
        return sources
    
    
            
