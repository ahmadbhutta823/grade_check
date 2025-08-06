# GPT Model Comparison Tool

This tool allows you to compare responses from GPT-4 and GPT-3.5 models for the same prompt.

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

## Usage

1. Run the script:
   ```
   python gpt_compare.py
   ```
2. Enter your question when prompted
3. The tool will display responses from both GPT-4 and GPT-3.5 models
4. Type 'quit' to exit the program

## Note
Make sure you have access to both GPT-4 and GPT-3.5 models in your OpenAI account.