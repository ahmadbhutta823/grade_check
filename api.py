from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
from openai import OpenAI
from dotenv import load_dotenv
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

# Load environment variables
load_dotenv()

# Initialize FastAPI app with enhanced documentation
app = FastAPI(
    title="Grade-Specific GPT Responses API",
    description="""
    API that provides grade-specific explanations using GPT-4.
    
    ## Quick Links
    - **Interactive API Documentation (Swagger UI)**: [/docs](/docs)
    - **Alternative API Documentation (ReDoc)**: [/redoc](/redoc)
    
    ## Overview
    This API provides explanations tailored for both Grade 2 and Grade 5 students in a single response.
    Simply send your question, and get back two age-appropriate explanations!
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.on_event("startup")
async def startup_event():
    """Print Swagger UI link on startup"""
    logger.info("API Documentation available at: http://localhost:8000/docs")

# Initialize OpenAI client
def get_openai_client():
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not found")
    return OpenAI(api_key=api_key)

# Pydantic models
class QuestionRequest(BaseModel):
    question: str

    class Config:
        json_schema_extra = {
            "example": {
                "question": "How does photosynthesis work?"
            }
        }

class GradeResponse(BaseModel):
    grade: int
    explanation: str

class CombinedResponse(BaseModel):
    question: str
    grade2_response: GradeResponse
    grade5_response: GradeResponse

def create_grade_specific_prompt(question: str, grade: int) -> str:
    """Create a grade-specific prompt for the AI."""
    if grade == 2:
        return f"""You are talking to a Grade 2 student (age 7-8). 
        Please explain this in a very simple, friendly way using:
        - Short, simple sentences
        - Basic vocabulary
        - Lots of examples
        - Fun and engaging tone
        - Include emojis where appropriate
        
        Question: {question}"""
    else:  # Grade 5
        return f"""You are talking to a Grade 5 student (age 10-11).
        Please explain this in an age-appropriate way using:
        - Clear explanations
        - Some technical terms (but explained)
        - Relevant examples
        - Educational tone
        - Encourage critical thinking
        
        Question: {question}"""

def get_explanation(client: OpenAI, question: str, grade: int) -> str:
    """Get explanation for a specific grade level."""
    grade_prompt = create_grade_specific_prompt(question, grade)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": grade_prompt}]
    )
    return response.choices[0].message.content

@app.get("/")
async def root():
    """Root endpoint that returns API information."""
    return {
        "message": "Welcome to Grade-Specific GPT Responses API",
        "documentation": {
            "Swagger UI (Interactive)": "/docs",
            "ReDoc": "/redoc"
        },
        "usage": "Send POST request to /explain/ to get explanations for both grade levels"
    }

@app.post("/explain/", response_model=CombinedResponse)
async def get_explanations(request: QuestionRequest):
    """
    Get explanations for both grade levels (2 and 5) for a given question.
    
    - **question**: The question to be explained
    Returns responses for both Grade 2 and Grade 5 levels.
    """
    try:
        client = get_openai_client()
        
        # Get both grade level responses
        grade2_explanation = get_explanation(client, request.question, 2)
        grade5_explanation = get_explanation(client, request.question, 5)
        
        return CombinedResponse(
            question=request.question,
            grade2_response=GradeResponse(
                grade=2,
                explanation=grade2_explanation
            ),
            grade5_response=GradeResponse(
                grade=5,
                explanation=grade5_explanation
            )
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)