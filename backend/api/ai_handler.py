import os
from mistralai import Mistral
from google import genai
from google.genai import types
import requests

# Set up logging to a file
log_filename = "log.txt"
log_file = open(log_filename, "w", encoding="utf-8")

def log_print(message):
    """Print to both console and log file"""
    print(message)
    log_file.write(f"{message}\n")
    log_file.flush()  # Force write to disk

def ask_mistral(msg, conversation_history):
    try:
        api_key = os.environ["MISTRAL_KEY"]
        model = "mistral-large-latest"

        client = Mistral(api_key=api_key)

        messages = [
            {
                "role": "system",
                "content": "You are an expert doctor with over 20 years of experience. Provide basic medical aid and advice to the user.Your answer should preferably follow a structure like-start with -What is the exact problem and how did it arise in the first place.1) assuring the patient that its not a big deal and it is normal where appropriate 2)Give timeline of how much time it would take for pain to subside 3)Provide First Aids (only if required) to releif pain imediately and Easy Solutions like home remedies that the patient can do. 5)Ask Patient to visit the a proffesional doctor in person in case pain increases6).Best practices and Precautions to avoid such similiar problems next time Here is the conversation history: " + conversation_history,
            },
            {
                "role": "user",
                "content": msg,
            },
        ]

        chat_response = client.chat.complete(
            model=model,
            messages=messages
        )
        log_print(chat_response.choices[0].message.content)
        return chat_response.choices[0].message.content
    except Exception as e:
        log_print(f"Error in ask_mistral: {str(e)}")
        return None

def ask_gemini(url, question, conversation_history):
    try:
        image = requests.get(url)
        client = genai.Client(api_key=os.environ["GEMINI_KEY"])
        prompt = f"Here is an image. {question} Consider as context that you . Here is the conversation history: " + conversation_history
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[prompt,
                      types.Part.from_bytes(data=image.content, mime_type="image/jpeg")])
        log_print(response.text)
        return response.text
    except Exception as e:
        log_print(f"Error processing image at {url}: {str(e)}")
        return None


def handle_ai(question, image_url, conversation_history):
    """Handles the AI response, choosing between Gemini and Mistral based on image presence."""
    if image_url:
        log_print("Using Gemini for image-based query.")
        ai_response = ask_gemini(image_url, question, conversation_history)
    else:
        log_print("Using Mistral for text-based query.")
        ai_response = ask_mistral(question, conversation_history)

    return ai_response