import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_stars():
    """Create a star decoration for kids."""
    return "\n" + "*" * 50 + "\n"

def setup_client():
    """Set up OpenAI client with API key."""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("Please set OPENAI_API_KEY in your .env file")
    return OpenAI(api_key=api_key)

def create_grade_specific_prompt(question, grade):
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

def get_response(client, prompt):
    """Get response from the model."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using GPT-3.5 for both to keep responses consistent
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Oops! Something went wrong: {str(e)}"

def get_grade_response(prompt, grade):
    """Get response formatted for specific grade level."""
    client = setup_client()
    grade_prompt = create_grade_specific_prompt(prompt, grade)
    response = get_response(client, grade_prompt)
    
    if grade == 2:
        print(create_stars())
        print("🌟 Hello Grade 2 Friend! 🌟")
        print(create_stars())
    else:
        print("\n=== Grade 5 Learning Zone ===\n")
    
    print(response)

def main():
    print("""
    🎓 Welcome to the Smart Learning Helper! 🎓
    This tool will help explain things in two different ways:
    1. For Grade 2 students (age 7-8)
    2. For Grade 5 students (age 10-11)
    """)
    
    while True:
        question = input("\nWhat would you like to learn about? (or type 'quit' to exit): ")
        if question.lower() == 'quit':
            print("\nThank you for learning with us! Goodbye! 👋")
            break
        
        print("\n--- Grade 2 Explanation ---")
        get_grade_response(question, 2)
        
        print("\n--- Grade 5 Explanation ---")
        get_grade_response(question, 5)

if __name__ == "__main__":
    main()