import os
import openai
import sys

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key = os.getenv("OPENAI_API_KEY")

# Create a client object
client = openai.OpenAI()

# Common function to call the OpenAI API
# This function is used to call the OpenAI API with the provided messages and parameters.
# It returns the content of the first choice in the response.
# The function is designed to be flexible, allowing you to specify the model, temperature, and max tokens.
# The default model is "gpt-3.5-turbo", temperature is set to 0, and max tokens is set to 500.
def call_model(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=500):
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )

    return response.choices[0].message.content.strip()

def build_prod_description_prompt(product, persona, reviews):
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

def build_prod_reviews_prompt(product, persona, reviews):
    return f"""
        Summarize the relevant customer reviews below to better align with the following customer persona.

        Input parameters are provided to help you understand the persona's tone and focus. You should take the generic product description and relevant customer reviews into account and summarize the reviews to match the persona's needs and preferences.

        Inputs are delimited by `###`. Instructions are provided between triple backticks. Only return the summarized reviews — do not repeat the inputs or explain anything.

        ###

        Persona Tone: {persona['tone']}
        Persona Focus: {persona['focus']}
        Generic Product Description: {product['description']}
        Relevant Customer Reviews:{chr(10).join(['- ' + r['review'] for r in reviews])}
        
        ###

        ```
        Instructions:
        - Summarize the customer reviews in a way that aligns with the persona’s tone and focus.
        - Highlight key sentiments and insights from the reviews that are relevant to the persona.
        - Use concise, clear, and engaging language.
        - Incorporate the product description where helpful to provide context.
        - Ensure the summary is no more than 100 words.
        - Do not return bullet points, tables, or meta commentary.
        - Return only the summarized reviews, nothing else.
        ```
        """

def generate_prod_description(product, persona, reviews):

    prompt = build_prod_description_prompt(product, persona, reviews)
    system_message = prompt
    
    messages =  [  
        {'role':'system', 'content': system_message}    
    ] 
    return call_model(messages)

def generate_reviews_summary(product, persona, reviews):

    prompt = build_prod_reviews_prompt(product, persona, reviews)
    system_message = prompt
    
    messages =  [  
        {'role':'system', 'content': system_message}    
    ] 
    return call_model(messages)

