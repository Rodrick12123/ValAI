import uuid 
from fastapi import FastAPI, File, UploadFile, HTTPException, Form 
from fastapi.responses import JSONResponse 
from fastapi.middleware.cors import CORSMiddleware 
from fastapi.responses import FileResponse 
from supabase import create_client, Client 
from dotenv import load_dotenv 
from pydantic import BaseModel 
import os 

# THINGS TO REMEBER
# ToRun: python -m backend.app
# ToDo: Fix cacheing
# payload size can be reduced by loading in elements as needed. (do this before prod)

app = FastAPI() 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

load_dotenv() 
# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL") 
supabase_key = os.getenv("SUPABASE_KEY") 

supabase: Client = create_client(supabase_url, supabase_key) 

class TextSubmission(BaseModel): 
    user_id: int
    original_text: str



@app.get("/") 
def health_check(): 
    return {"status": "healthy"} 

@app.post("/submitTextDatabase") 
async def submit_text_database(submission: TextSubmission): 
    # code to submit to database here 
    return submission.original_text 

@app.post("/submit/document")
async def submit_document(user_id: int = Form(...), uploaded_file: UploadFile = File(...)):
    contents = await uploaded_file.read()
    print(f"Received from user {user_id}: {uploaded_file.filename}, {uploaded_file.content_type}")
    res2 = {
        "fullText": """**Analyzing Truth, Bias, and Ambiguity in Information**
 
                    Information is often presented with varying degrees of accuracy, bias, and clarity. Understanding the distinctions between truth and falsehood, bias and neutrality, and clarity and ambiguity is essential for critical thinking. This paper explores these distinctions through various examples.

                    True statements are those that can be verified through scientific evidence and factual data. For example, water boils at 100°C at standard atmospheric pressure, the Earth orbits around the Sun, and the human body is composed of approximately 60% water. These facts are widely accepted and backed by research.

                    False statements, on the other hand, are claims that have been debunked or lack supporting evidence. Examples include the notion that the Moon is made of cheese, the false claim that vaccines cause autism, and the myth that the Great Wall of China is the only man-made structure visible from space. These statements have been disproven through scientific inquiry and analysis.

                    Bias can be introduced into statements through generalization, exaggeration, or omission of key details. For instance, claiming that "the government always lies to its citizens" or that "private corporations are inherently more efficient than public institutions" reflects a biased perspective that lacks nuance. Similarly, promotional statements like "this new phone is the best device on the market, and everyone should buy it" push a subjective viewpoint rather than objective facts.

                    In contrast, unbiased statements present information in a neutral, fact-based manner. Saying that "the government has made both truthful and misleading statements in different contexts," or that "studies show efficiency varies between private and public institutions based on specific conditions" provides a more balanced and analytical perspective. Likewise, stating that "consumer preferences for phones vary based on individual needs and priorities" avoids promotional bias and allows for individual interpretation.

                    Ambiguity arises when statements lack specificity or rely on vague references. Phrases like "this politician supports policies that some believe will benefit the economy," "many people say that this diet leads to better health," or "the future of artificial intelligence is uncertain" do not provide clear definitions or verifiable data. Such ambiguity can lead to misinterpretation or confusion.

                    In conclusion, distinguishing between true and false information, recognizing bias, and identifying ambiguity are crucial skills in analyzing information. Being aware of these distinctions allows for more informed decision-making and critical evaluation of sources.

                    """, 
        'Overall Truth Percentage': 57.89, 
        'Overall Bias Percentage': 0.0, 
        'Context Contributions': [{'Context': 'True statements are those that can be verified through scientific evidence and factual data. For example, water boils at 100°C at standard atmospheric pressure, the Earth orbits around the Sun, and the human body is composed of approximately 60% water. These facts are widely accepted and backed by research.', 'Truth Contribution': True, 'Bias Contribution': False, 'Truth Relevance Scale (1-5)': 3, 'Bias Relevance Scale (1-5)': 3, 'Uncertaintly Relevance Scale (1-5)': 3, 'Improved': '', 'TruthSources': ['https://www.sciencedirect.com/'], 'Reason': "Statements about scientific facts such as water boiling at 100°C at standard pressure, Earth's orbit, and human body's water content are well-established scientific facts."}, {'Context': 'False statements, on the other hand, are claims that have been debunked or lack supporting evidence. Examples include the notion that the Moon is made of cheese, the false claim that vaccines cause autism, and the myth that the Great Wall of China is the only man-made structure visible from space. These statements have been disproven through scientific inquiry and analysis.', 'Truth Contribution': False, 'Bias Contribution': False, 'Truth Relevance Scale (1-5)': 4, 'Bias Relevance Scale (1-5)': 4, 'Uncertaintly Relevance Scale (1-5)': 4, 'Improved': '', 'TruthSources': ['https://skepticalraptor.com/'], 'Reason': 'Claims such as the Moon being made of cheese, vaccines causing autism, and the Great Wall of China being the only visible man-made structure from space have been scientifically debunked or are myths.'}, {'Context': 'Bias can be introduced into statements through generalization, exaggeration, or omission of key details. For instance, claiming that "the government always lies to its citizens" or that "private corporations are inherently more efficient than public institutions" reflects a biased perspective that lacks nuance. Similarly, promotional statements like "this new phone is the best device on the market, and everyone should buy it" push a subjective viewpoint rather than objective facts.', 'Truth Contribution': None, 'Bias Contribution': None, 'Truth Relevance Scale (1-5)': 5, 'Bias Relevance Scale (1-5)': 5, 'Uncertaintly Relevance Scale (1-5)': 5, 'Improved': 'Bias can be minimized in statements by providing nuanced, evidence-based descriptions that acknowledge complexity rather than sweeping generalizations or stereotypes.', 'TruthSources': '', 'Reason': 'Bias arises from generalization, exaggeration, or omission which can be nuanced with more precise language, examples, and context.'}, {'Context': 'In contrast, unbiased statements present information in a neutral, fact-based manner. Saying that "the government has made both truthful and misleading statements in different contexts," or that "studies show efficiency varies between private and public institutions based on specific conditions" provides a more balanced and analytical perspective. Likewise, stating that "consumer preferences for phones vary based on individual needs and priorities" avoids promotional bias and allows for individual interpretation.', 'Truth Contribution': True, 'Bias Contribution': False, 'Truth Relevance Scale (1-5)': 5, 'Bias Relevance Scale (1-5)': 5, 'Uncertaintly Relevance Scale (1-5)': 5, 'Improved': '', 'TruthSources': ['https://www.nber.org/'], 'Reason': 'Statements highlighting the variability of accuracy in government and corporate practices, and individual differences in consumer preferences are factually accurate.'}, {'Context': 'Ambiguity arises when statements lack specificity or rely on vague references. Phrases like "this politician supports policies that some believe will benefit the economy," "many people say that this diet leads to better health," or "the future of artificial intelligence is uncertain" do not provide clear definitions or verifiable data. Such ambiguity can lead to misinterpretation or confusion.', 'Truth Contribution': False, 'Bias Contribution': False, 'Truth Relevance Scale (1-5)': 4, 'Bias Relevance Scale (1-5)': 4, 'Uncertaintly Relevance Scale (1-5)': 4, 'Improved': '', 'TruthSources': '', 'Reason': 'Vague references lacking specificity do not provide verifiable information and can lead to misinterpretation.'}, {'Context': 'In conclusion, distinguishing between true and false information, recognizing bias, and identifying ambiguity are crucial skills in analyzing information. Being aware of these distinctions allows for more informed decision-making and critical evaluation of sources.', 'Truth Contribution': True, 'Bias Contribution': False, 'Truth Relevance Scale (1-5)': 3, 'Bias Relevance Scale (1-5)': 3, 'Uncertaintly Relevance Scale (1-5)': 3, 'Improved': '', 'TruthSources': '', 'Reason': 'The conclusion underscores the importance of critical thinking skills, which is a factual and widely accepted viewpoint.'}], 
        'Overall Uncertain Truth Percentage': 20.83, 
        'Overall Uncertain Bias Percentage': 20.83
    } 

    return JSONResponse(content=res2)

@app.post("/submit") 
async def submit_text(submission: TextSubmission): 
    # Store the text submission in the database 
    # Add your database logic here 
    print("Submission", submission) 
    res = { 
            "fullText": "The power of collaboration AI Collaboratives are rooted in the idea that AI’s potential lies not just in the technology itself, but also in partnerships that make its responsible application possible. This is and will allways be the way",
            "results": [
                {
                "Truth": True,
                "Biased": False,
                "Improved": "",
                "Reason": "The statement accurately conveys the collaborative nature of AI and its potential contributions.",
                "Context": "The power of collaboration AI Collaboratives are rooted in the idea that AI’s potential lies not just in the technology itself, but also in partnerships that make its responsible application possible.",
                "TruthSources": "https://www.blog.google/outreach-initiatives/ai/new-initiative-united-ai-collaboratives/"
                } 
            ], 
            "message": "Text submitted successfully", 
            "revised_text": submission.original_text, 
            "submission_id": uuid.uuid4().int, 
            "bias_socre": "TestBias" 
        } 
    
    res2 = {
        "fullText": """**Analyzing Truth, Bias, and Ambiguity in Information**
 
                    Information is often presented with varying degrees of accuracy, bias, and clarity. Understanding the distinctions between truth and falsehood, bias and neutrality, and clarity and ambiguity is essential for critical thinking. This paper explores these distinctions through various examples.

                    True statements are those that can be verified through scientific evidence and factual data. For example, water boils at 100°C at standard atmospheric pressure, the Earth orbits around the Sun, and the human body is composed of approximately 60% water. These facts are widely accepted and backed by research.

                    False statements, on the other hand, are claims that have been debunked or lack supporting evidence. Examples include the notion that the Moon is made of cheese, the false claim that vaccines cause autism, and the myth that the Great Wall of China is the only man-made structure visible from space. These statements have been disproven through scientific inquiry and analysis.

                    Bias can be introduced into statements through generalization, exaggeration, or omission of key details. For instance, claiming that "the government always lies to its citizens" or that "private corporations are inherently more efficient than public institutions" reflects a biased perspective that lacks nuance. Similarly, promotional statements like "this new phone is the best device on the market, and everyone should buy it" push a subjective viewpoint rather than objective facts.

                    In contrast, unbiased statements present information in a neutral, fact-based manner. Saying that "the government has made both truthful and misleading statements in different contexts," or that "studies show efficiency varies between private and public institutions based on specific conditions" provides a more balanced and analytical perspective. Likewise, stating that "consumer preferences for phones vary based on individual needs and priorities" avoids promotional bias and allows for individual interpretation.

                    Ambiguity arises when statements lack specificity or rely on vague references. Phrases like "this politician supports policies that some believe will benefit the economy," "many people say that this diet leads to better health," or "the future of artificial intelligence is uncertain" do not provide clear definitions or verifiable data. Such ambiguity can lead to misinterpretation or confusion.

                    In conclusion, distinguishing between true and false information, recognizing bias, and identifying ambiguity are crucial skills in analyzing information. Being aware of these distinctions allows for more informed decision-making and critical evaluation of sources.

                    """, 
        'Overall Truth Percentage': 57.89, 
        'Overall Bias Percentage': 0.0, 
        'Context Contributions': [{'Context': 'True statements are those that can be verified through scientific evidence and factual data. For example, water boils at 100°C at standard atmospheric pressure, the Earth orbits around the Sun, and the human body is composed of approximately 60% water. These facts are widely accepted and backed by research.', 'Truth Contribution': True, 'Bias Contribution': False, 'Truth Relevance Scale (1-5)': 3, 'Bias Relevance Scale (1-5)': 3, 'Uncertaintly Relevance Scale (1-5)': 3, 'Improved': '', 'TruthSources': ['https://www.sciencedirect.com/'], 'Reason': "Statements about scientific facts such as water boiling at 100°C at standard pressure, Earth's orbit, and human body's water content are well-established scientific facts."}, {'Context': 'False statements, on the other hand, are claims that have been debunked or lack supporting evidence. Examples include the notion that the Moon is made of cheese, the false claim that vaccines cause autism, and the myth that the Great Wall of China is the only man-made structure visible from space. These statements have been disproven through scientific inquiry and analysis.', 'Truth Contribution': False, 'Bias Contribution': False, 'Truth Relevance Scale (1-5)': 4, 'Bias Relevance Scale (1-5)': 4, 'Uncertaintly Relevance Scale (1-5)': 4, 'Improved': '', 'TruthSources': ['https://skepticalraptor.com/'], 'Reason': 'Claims such as the Moon being made of cheese, vaccines causing autism, and the Great Wall of China being the only visible man-made structure from space have been scientifically debunked or are myths.'}, {'Context': 'Bias can be introduced into statements through generalization, exaggeration, or omission of key details. For instance, claiming that "the government always lies to its citizens" or that "private corporations are inherently more efficient than public institutions" reflects a biased perspective that lacks nuance. Similarly, promotional statements like "this new phone is the best device on the market, and everyone should buy it" push a subjective viewpoint rather than objective facts.', 'Truth Contribution': None, 'Bias Contribution': None, 'Truth Relevance Scale (1-5)': 5, 'Bias Relevance Scale (1-5)': 5, 'Uncertaintly Relevance Scale (1-5)': 5, 'Improved': 'Bias can be minimized in statements by providing nuanced, evidence-based descriptions that acknowledge complexity rather than sweeping generalizations or stereotypes.', 'TruthSources': '', 'Reason': 'Bias arises from generalization, exaggeration, or omission which can be nuanced with more precise language, examples, and context.'}, {'Context': 'In contrast, unbiased statements present information in a neutral, fact-based manner. Saying that "the government has made both truthful and misleading statements in different contexts," or that "studies show efficiency varies between private and public institutions based on specific conditions" provides a more balanced and analytical perspective. Likewise, stating that "consumer preferences for phones vary based on individual needs and priorities" avoids promotional bias and allows for individual interpretation.', 'Truth Contribution': True, 'Bias Contribution': False, 'Truth Relevance Scale (1-5)': 5, 'Bias Relevance Scale (1-5)': 5, 'Uncertaintly Relevance Scale (1-5)': 5, 'Improved': '', 'TruthSources': ['https://www.nber.org/'], 'Reason': 'Statements highlighting the variability of accuracy in government and corporate practices, and individual differences in consumer preferences are factually accurate.'}, {'Context': 'Ambiguity arises when statements lack specificity or rely on vague references. Phrases like "this politician supports policies that some believe will benefit the economy," "many people say that this diet leads to better health," or "the future of artificial intelligence is uncertain" do not provide clear definitions or verifiable data. Such ambiguity can lead to misinterpretation or confusion.', 'Truth Contribution': False, 'Bias Contribution': False, 'Truth Relevance Scale (1-5)': 4, 'Bias Relevance Scale (1-5)': 4, 'Uncertaintly Relevance Scale (1-5)': 4, 'Improved': '', 'TruthSources': '', 'Reason': 'Vague references lacking specificity do not provide verifiable information and can lead to misinterpretation.'}, {'Context': 'In conclusion, distinguishing between true and false information, recognizing bias, and identifying ambiguity are crucial skills in analyzing information. Being aware of these distinctions allows for more informed decision-making and critical evaluation of sources.', 'Truth Contribution': True, 'Bias Contribution': False, 'Truth Relevance Scale (1-5)': 3, 'Bias Relevance Scale (1-5)': 3, 'Uncertaintly Relevance Scale (1-5)': 3, 'Improved': '', 'TruthSources': '', 'Reason': 'The conclusion underscores the importance of critical thinking skills, which is a factual and widely accepted viewpoint.'}], 
        'Overall Uncertain Truth Percentage': 20.83, 
        'Overall Uncertain Bias Percentage': 20.83



 
    } 
    
    return res2 

@app.post("/analyze/{submission_id}") 
async def analyze_text(submission_id: int): 
    # Perform analysis on the text
    # Add your analysis logic here
    return {"message": "Text analyzed successfully"} 

@app.get("/results/{submission_id}") 
async def get_results(submission_id: int): 
    # Retrieve analysis results from the database
    # Add your retrieval logic here
    return {"message": "Results retrieved successfully"} 

if __name__ == '__main__': 
    import uvicorn 
    uvicorn.run(app,  host="0.0.0.0", port=5000) 