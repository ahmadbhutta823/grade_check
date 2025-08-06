# Grade-Specific GPT Responses API

This API provides grade-specific explanations using GPT-4, tailored for both Grade 2 and Grade 5 levels in a single response.

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Running the API

1. Start the FastAPI server:
   ```
   uvicorn api:app --reload
   ```
2. The API will be available at: `http://localhost:8000`
3. Interactive API documentation (Swagger UI) is available at: `http://localhost:8000/docs`
4. Alternative API documentation (ReDoc) is available at: `http://localhost:8000/redoc`

## API Endpoints

### GET /
- Root endpoint that returns API information
- No parameters required

### POST /explain/
- Get explanations for both grade levels (2 and 5) for a given question
- Request body:
  ```json
  {
    "question": "How does photosynthesis work?"
  }
  ```
- Response format:
  ```json
  {
    "question": "How does photosynthesis work?",
    "grade2_response": {
      "grade": 2,
      "explanation": "Simple explanation with emojis..."
    },
    "grade5_response": {
      "grade": 5,
      "explanation": "More detailed explanation..."
    }
  }
  ```

## Example Usage

Using curl:
```bash
curl -X POST "http://localhost:8000/explain/" \
     -H "Content-Type: application/json" \
     -d '{"question": "How does photosynthesis work?"}'
```

Using Python requests:
```python
import requests

response = requests.post(
    "http://localhost:8000/explain/",
    json={
        "question": "How does photosynthesis work?"
    }
)
print(response.json())
```

## Command Line Interface

You can still use the command-line interface by running:
```
python gpt_compare.py
```