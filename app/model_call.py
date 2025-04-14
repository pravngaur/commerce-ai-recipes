# This file contains utility functions to interact with the OpenAI API for generating product descriptions
# and summarizing customer reviews. It includes methods to build prompts, call the API, and process responses.
# You can modify the code to choose a different model of your choice.

import os
import openai
import sys

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # Load environment variables from a .env file

openai.api_key = os.getenv("OPENAI_API_KEY")  # Set the OpenAI API key from environment variables

# Create a client object for interacting with the OpenAI API
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

# Function to build a prompt for generating a product description
# This function constructs a detailed prompt using the product details, persona information, and other parameters.
# The prompt is designed to guide the model in rewriting the product description to align with the persona's needs.
def build_prod_description_prompt(product, persona, reviews, description_word_limit, response_locale, prompt_influence):
    return f"""
        Rewrite the product description below to better appeal to the following customer persona.

        Following input parameters are provided to help you understand the context:
        Persona Tone: required response tone
        Persona priorities: persona's priorities and interests
        Generic Product Description: This is the generic product description.
        Relevant Customer Reviews: use these reviews to understand the product's strengths and weaknesses. And comeup with a description that aligns with the persona's needs.
        Persona Intent: This reflects the in-session intent of the persona, which could be different than 'Persona priorities' for example a customer buying a table for her daugher's dorm room would be looking for sturdiness and durability, but the persona's priorities could be style and aesthetics.
        Persona Confidence: confidence of the calling application in the persona's intent. This is a number between 0 and 1, where 1 means the application is very confident in the persona's intent and 0 means it is not confident at all. Use this number to determine how much weight to give the persona's intent in the final product description. For example, if the confidence is 0.8, you should give more weight to the persona's intent than if the confidence is 0.2.
        
        {f'Prompt Influence: {prompt_influence}' if prompt_influence is not None else ''}
        
        You should take all the input params into account and rewrite the description to align with the persona's needs.

        Inputs are delimited by `###`. Instructions are provided between triple backticks. Only return the rewritten product description — do not repeat the inputs or explain anything.

        ###

        Persona Tone: {persona['tone']}
        Persona priorities: {persona['priorities']}
        Generic Product Description: {product['description']}
        Relevant Customer Reviews:{chr(10).join(['- ' + r['review'] for r in reviews])}
        Persona Intent: {persona['intent']}
        Persona Confidence: {persona['confidence']}
        
        ###

        ```
        Instructions:
        - Incorporate the persona’s tone and priorities.
        - Highlight key product benefits.
        - Use simple, persuasive language.
        - Weave in customer sentiment if helpful.
        - Do not return bullet points, tables, or meta commentary.
        - Return only the rewritten product description, nothing else.
        - Ensure the summary is no more than {description_word_limit} words.
        - Response required in this locale: {response_locale}
        ```
        """

# Function to build a prompt for summarizing customer reviews
# This function constructs a prompt using the product details, persona information, and reviews.
# The prompt is designed to guide the model in summarizing reviews in a way that aligns with the persona's tone and priorities.
def build_prod_reviews_prompt(product, persona, reviews, reviews_word_limit, response_locale,prompt_influence):
    return f"""
        
        Summarize the relevant customer reviews below to better align with the following customer persona.

        Following input parameters are provided to help you understand the context:
        Persona Tone: required response tone
        Persona priorities: persona's priorities and interests
        Generic Product Description: This is the generic product description.
        Relevant Customer Reviews: use these reviews to understand the product's strengths and weaknesses. And comeup with a description that aligns with the persona's needs.
        Persona Intent: This reflects the in-session intent of the persona, which could be different than 'Persona priorities' for example a customer buying a table for her daugher's dorm room would be looking for sturdiness and durability, but the persona's priorities could be style and aesthetics.
        Persona Confidence: confidence of the calling application in the persona's intent. This is a number between 0 and 1, where 1 means the application is very confident in the persona's intent and 0 means it is not confident at all. Use this number to determine how much weight to give the persona's intent in the final product description. For example, if the confidence is 0.8, you should give more weight to the persona's intent than if the confidence is 0.2.
        
        You should take all the input params into account and summarise reviews in a single paragraph to align with the persona's needs.

        Inputs are delimited by `###`. Instructions are provided between triple backticks. Only return the summarized reviews — do not repeat the inputs or explain anything.

        ###

        Persona Tone: {persona['tone']}
        Persona priorities: {persona['priorities']}
        Generic Product Description: {product['description']}
        Relevant Customer Reviews:{chr(10).join(['- ' + r['review'] for r in reviews])}
        Persona Intent: {persona['intent']}
        Persona Confidence: {persona['confidence']}
        
        ###

        ```
        Instructions:
        - Summarize the customer reviews in a way that aligns with the persona’s tone and priorities.
        - Highlight key sentiments and insights from the reviews that are relevant to the persona.
        - Use concise, clear, and engaging language.
        - Incorporate the product description where helpful to provide context.
        - Ensure the summary is no more than {reviews_word_limit} words.
        - Do not return bullet points, tables, or meta commentary.
        - Return only the summarized reviews, nothing else.
        - Response required in this locale: {response_locale}
        ```
        """

# Function to generate a rewritten product description
# This function uses the OpenAI API to generate a product description based on the provided inputs.
# It calls the `build_prod_description_prompt` function to create the prompt and then sends it to the API.
def generate_prod_description(product, persona, reviews, description_word_limit, response_locale, prompt_influence):

    prompt = build_prod_description_prompt(product, persona, reviews, description_word_limit, response_locale, prompt_influence)
    system_message = prompt
    
    messages =  [  
        {'role':'system', 'content': system_message}    
    ] 
    return call_model(messages)

# Function to generate a summary of customer reviews
# This function uses the OpenAI API to summarize customer reviews based on the provided inputs.
# It calls the `build_prod_reviews_prompt` function to create the prompt and then sends it to the API.
def generate_reviews_summary(product, persona, reviews, reviews_word_limit, response_locale, prompt_influence):

    prompt = build_prod_reviews_prompt(product, persona, reviews, reviews_word_limit, response_locale, prompt_influence)
    system_message = prompt
    
    messages =  [  
        {'role':'system', 'content': system_message}    
    ] 
    return call_model(messages)

