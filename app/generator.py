# This module provides functions to generate product descriptions and review summaries
# by utilizing external model calls. It ensures input validation before invoking the models. Perform your transformations/pre-processing of the data/inputs here.

from app.model_call import generate_prod_description, generate_reviews_summary

def generate_description(product, persona, reviews, description_word_limit, response_locale, prompt_influence):
    """
    Generates a product description based on the provided product details, persona, and reviews.
    
    Args:
        product (str): The product name or details.
        persona (str): The target persona for the description.
        reviews (list): A list of reviews related to the product.
        description_word_limit (int): The word limit for the generated description.
        response_locale (str): The locale for the response (e.g., language or region).
        prompt_influence (float): A parameter to control the influence of the prompt on the output.
    
    Returns:
        str: The generated product description or an empty string if inputs are invalid.
    """
    
    response = ""
    if(product == None or persona == None  or reviews == None):
        return response
    else:
        response = generate_prod_description(product, persona, reviews, description_word_limit, response_locale, prompt_influence)
    
    return response

def generate_summary(product, persona, reviews, reviews_word_limit, response_locale, prompt_influence):
    """
    Generates a summary of reviews for a product based on the provided details.
    
    Args:
        product (str): The product name or details.
        persona (str): The target persona for the summary.
        reviews (list): A list of reviews related to the product.
        reviews_word_limit (int): The word limit for the generated summary.
        response_locale (str): The locale for the response (e.g., language or region).
        prompt_influence (float): A parameter to control the influence of the prompt on the output.
    
    Returns:
        str: The generated reviews summary or an empty string if inputs are invalid.
    """
    
    response = ""
    if(product == None or persona == None  or reviews == None):
        return response
    else:
        response = generate_reviews_summary(product, persona, reviews, reviews_word_limit, response_locale, prompt_influence)
    
    return response
