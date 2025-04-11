import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
HF_API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
#HF_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}

def build_prompt(product, persona, reviews):
    return f"""
        Rewrite the product description below to better appeal to the following customer persona.

        Input parameters are provided to help you understand the persona's tone and focus. You should take the generic product description and relevant customer reviews into account and rewrite the description to align with the persona's needs.

        Inputs are delimited by `###`. Instructions are provided between triple backticks. Only return the rewritten product description — do not repeat the inputs or explain anything.

        ###

        Persona Tone: {persona['tone']}
        Persona Focus: {persona['focus']}
        Generic Product Description: {product['description']}
        Relevant Customer Reviews:{chr(10).join(['- ' + r['review'] for r in reviews])}
        
        ###

        ```
        Instructions:
        - Incorporate the persona’s tone and focus.
        - Highlight key product benefits.
        - Use simple, persuasive language.
        - Weave in customer sentiment if helpful.
        - Do not return bullet points, tables, or meta commentary.
        - Return only the rewritten product description, nothing else.
        ```
        """

    # return (
    #     f"You are a helpful product copywriter.\n"
    #     f"Persona: {persona['tone']} tone, focus on {persona['focus']}.\n\n"
    #     f"Generic Description: {product['description']}\n\n"
    #     f"Customer Reviews:\n"
    #     + "\n".join([f"- {review['review']}" for review in reviews]) +
    #     "\n\nGenerate a personalized product description:"
    # )

def generate_description(prompt):
    response = ""
    try:
        api_response = requests.post(
            HF_API_URL,
            headers=headers,
            json={"inputs": prompt, "parameters": {"max_new_tokens": 400, "temperature":0.7, "top_p": 0.95, "repetition_penalty": 1.1}},
        )
        if(api_response.status_code == 200 and api_response.json() != None):
            response = api_response.json()[0]['generated_text']
        else:
            print(f"❌ Error: {api_response.status_code} - {api_response.text}")
            raise ValueError("Unexpected response format from model")
            
    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"❌ Request error: {req_err}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    return response

def extract_output(text, prompt):
    # Strip everything that matches the prompt to get only the model’s continuation
    if text.startswith(prompt):
        text = text[len(prompt):]

    # Clean up any weird leftover formatting or extra newlines
    import re
    text = re.sub(r"<[^>]+>", "", text)  # remove tags
    text = re.sub(r"\n{2,}", "\n", text)  # multiple line breaks
    return text.strip()

# def generate_description(prompt):
#     payload = {
#         "inputs": prompt,
#         "parameters": {
#             "temperature": 0.7,
#             "max_new_tokens": 400,
#             "do_sample": True,
#             "top_p": 0.95
#         }
#     }

#     try:
#         response = requests.post(HF_API_URL, headers = headers, json=payload)
#         response.raise_for_status()  # Raises HTTPError for bad status codes

#         result = response.json()

#         if isinstance(result, list) and "generated_text" in result[0]:
#             return result[0]["generated_text"]
#         else:
#             raise ValueError("Unexpected response format from model")

#     except requests.exceptions.HTTPError as http_err:
#         print(f"❌ HTTP error occurred: {http_err}")
#     except requests.exceptions.ConnectionError:
#         print("❌ Connection error. Check your internet or model URL.")
#     except requests.exceptions.Timeout:
#         print("❌ Request timed out. Try again later.")
#     except requests.exceptions.RequestException as req_err:
#         print(f"❌ General request error: {req_err}")
#     except ValueError as ve:
#         print(f"❌ Response parsing error: {ve}")
#     except Exception as e:
#         print(f"❌ An unexpected error occurred: {e}")

#     return None 

def call_model(product, persona, reviews):
    prompt = build_prompt(product, persona, reviews)
    print(f"prompt: {prompt}")
    # response_raw = generate_description(prompt)
    # response = extract_output(response_raw, prompt)
    #return response

