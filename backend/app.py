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

@app.post("/submit")
async def submit_text(submission: TextSubmission):
    # Store the text submission in the database
    # Add your database logic here
    print("Submission",submission)
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
        'Overall Truth Percentage': 100.0, 
        'Overall Bias Percentage': 30.95, 
        'Context Contributions': [{'Context': 'True statements are those that can be verified through scientific evidence and factual data.', 'Truth Contribution': True, 'Bias Contribution': False, 'Truth Relevance Scale (1-5)': 2, 'Bias Relevance Scale (1-5)': 2, 'Uncertaintly Relevance Scale (1-5)': 2, 'Improved': '', 'TruthSources': ['https://www.scientificamerican.com/article/the-science-behind-how-we-know-what-we-know/'], 'Reason': 'The statement accurately defines true statements using verifiable scientific evidence.'}, {'Context': 'For example, water boils at 100°C at standard atmospheric pressure, the Earth orbits around the Sun, and the human body is composed of approximately 60% water.', 'Truth Contribution': True, 'Bias Contribution': False, 'Truth Relevance Scale (1-5)': 3, 'Bias Relevance Scale (1-5)': 3, 'Uncertaintly Relevance Scale (1-5)': 3, 'Improved': '', 'TruthSources': ['https://www.nationalgeographic.com/science/article/boiling-point-of-water'], 'Reason': 'Examples provided are widely recognized as true and align with scientific consensus.'}, {'Context': 'False statements, on the other hand, are claims that have been debunked or lack supporting evidence.', 'Truth Contribution': True, 'Bias Contribution': False, 'Truth Relevance Scale (1-5)': 3, 'Bias Relevance Scale (1-5)': 3, 'Uncertaintly Relevance Scale (1-5)': 3, 'Improved': '', 'TruthSources': ['https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6240660/'], 'Reason': 'The statement correctly indicates that false claims lack supporting evidence and provides appropriate examples.'}, {'Context': 'Examples include the notion that the Moon is made of cheese, the false claim that vaccines cause autism, and the myth that the Great Wall of China is the only man-made structure visible from space.', 'Truth Contribution': True, 'Bias Contribution': False, 'Truth Relevance Scale (1-5)': 4, 'Bias Relevance Scale (1-5)': 4, 'Uncertaintly Relevance Scale (1-5)': 4, 'Improved': '', 'TruthSources': ['https://www.cdc.gov/vaccinesafety/concerns/autism.html'], 'Reason': 'The examples provided are recognized as false claims and have been disproven by research.'}, {'Context': "For instance, claiming that 'the government always lies to its citizens' or that 'private corporations are inherently more efficient than public institutions' reflects a biased perspective that lacks nuance.", 'Truth Contribution': True, 'Bias Contribution': True, 'Truth Relevance Scale (1-5)': 4, 'Bias Relevance Scale (1-5)': 4, 'Uncertaintly Relevance Scale (1-5)': 4, 'Improved': "Claiming that 'some governments can mislead citizens' or 'private corporations can sometimes be more efficient than public institutions' reflects a more balanced view.", 'TruthSources': None, 'Reason': 'The statement presents a subjective and exaggerated view that can mislead rather than providing a nuanced stance.'}, {'Context': 'In contrast, unbiased statements present information in a neutral, fact-based manner.', 'Truth Contribution': True, 'Bias Contribution': False, 'Truth Relevance Scale (1-5)': 2, 'Bias Relevance Scale (1-5)': 2, 'Uncertaintly Relevance Scale (1-5)': 2, 'Improved': '', 'TruthSources': None, 'Reason': 'The statement accurately describes unbiased expressions of information.'}, {'Context': "Saying that 'the government has made both truthful and misleading statements in different contexts,' or that 'studies show efficiency varies between private and public institutions based on specific conditions' provides a more balanced and analytical perspective.", 'Truth Contribution': True, 'Bias Contribution': False, 'Truth Relevance Scale (1-5)': 5, 'Bias Relevance Scale (1-5)': 5, 'Uncertaintly Relevance Scale (1-5)': 5, 'Improved': '', 'TruthSources': None, 'Reason': 'The examples provided are balanced statements that reflect unbiased perspectives.'}, {'Context': "Likewise, stating that 'consumer preferences for phones vary based on individual needs and priorities' avoids promotional bias and allows for individual interpretation.", 'Truth Contribution': True, 'Bias Contribution': False, 'Truth Relevance Scale (1-5)': 4, 'Bias Relevance Scale (1-5)': 4, 'Uncertaintly Relevance Scale (1-5)': 4, 'Improved': '', 'TruthSources': None, 'Reason': 'The statement correctly highlights consumer preferences, which can vary individually.'}, {'Context': "Phrases like 'this politician supports policies that some believe will benefit the economy,' 'many people say that this diet leads to better health,' or 'the future of artificial intelligence is uncertain' do not provide clear definitions or verifiable data.", 'Truth Contribution': True, 'Bias Contribution': True, 'Truth Relevance Scale (1-5)': 5, 'Bias Relevance Scale (1-5)': 5, 'Uncertaintly Relevance Scale (1-5)': 5, 'Improved': 'This politician supports policies that some believe might benefit the economy based on proposed data.', 'TruthSources': None, 'Reason': 'Ambiguity arises from vague language that lacks specificity, leading to misinterpretation.'}, {'Context': "'many people say that this diet leads to better health,'", 'Truth Contribution': True, 'Bias Contribution': True, 'Truth Relevance Scale (1-5)': 2, 'Bias Relevance Scale (1-5)': 2, 'Uncertaintly Relevance Scale (1-5)': 2, 'Improved': 'Numerous people have reported perceived benefits from this diet but research is ongoing.', 'TruthSources': None, 'Reason': 'Generalizations and vague phrases create bias and ambiguity, making the statement less reliable.'}, {'Context': "'the future of artificial intelligence is uncertain'", 'Truth Contribution': True, 'Bias Contribution': True, 'Truth Relevance Scale (1-5)': 2, 'Bias Relevance Scale (1-5)': 2, 'Uncertaintly Relevance Scale (1-5)': 2, 'Improved': 'The predictions regarding the future of artificial intelligence are currently uncertain and involve ongoing research.', 'TruthSources': None, 'Reason': 'The phrase states a level of uncertainty without defining specific future parameters, creating ambiguity.'}, {'Context': 'In conclusion, distinguishing between true and false information, recognizing bias, and identifying ambiguity are crucial skills in analyzing information.', 'Truth Contribution': True, 'Bias Contribution': False, 'Truth Relevance Scale (1-5)': 3, 'Bias Relevance Scale (1-5)': 3, 'Uncertaintly Relevance Scale (1-5)': 3, 'Improved': '', 'TruthSources': None, 'Reason': 'The statement accurately reflects the importance of distinguishing between various forms of information for critical analysis.'}, {'Context': 'Being aware of these distinctions allows for more informed decision-making and critical evaluation of sources.', 'Truth Contribution': True, 'Bias Contribution': False, 'Truth Relevance Scale (1-5)': 3, 'Bias Relevance Scale (1-5)': 3, 'Uncertaintly Relevance Scale (1-5)': 3, 'Improved': '', 'TruthSources': None, 'Reason': 'The sentence correctly states the benefits of understanding these distinctions.'}], 
        'Overall Uncertain Truth Percentage': 0.0, 
        'Overall Uncertain Bias Percentage': 0.0



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