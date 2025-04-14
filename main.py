# This file defines a Flask web application for generating product descriptions and review summaries.
# It uses predefined personas and customer reviews to customize the output based on user input.

from flask import Flask, render_template, request
from app.generator import generate_description, generate_summary
import json

import os
print("Current working directory:", os.getcwd())

app = Flask(__name__)

# Load product data and customer reviews from a JSON file
with open("app/data/products.json") as f:
    product = json.load(f)
    customer_reviews = product["customer_reviews"]
    
# Load persona data from a JSON file
with open("app/data/personas.json") as f:
    personas = json.load(f)

@app.route("/", methods=["GET"])
def home():
    """
    Home route that renders the main page of the application.
    - Retrieves the persona from query parameters (defaults to "family").
    - Filters customer reviews based on the selected persona.
    - Generates a product description and reviews summary using the generator module.
    - Passes the generated content and other data to the HTML template for rendering.
    """
    # Get the 'persona' value from the URL query parameters, default to "family" if not provided
    persona_req = request.args.get("persona", "family")

    # Getting the relevant product reviews based on the selected persona
    reviews = []
    for review in customer_reviews:
        if(review["persona"] == persona_req):
            reviews.append(review)
    
    
    if(persona_req in personas):
        persona = personas[persona_req]

    # setting these params here for demo, but these actually would come from the calling application/storefront
    description_word_limit = 100
    reviews_word_limit = 100
    response_locale = "en-US"

    # This is just for dmeo -- showing locale param in action, remove it from your implementations
    if(persona_req == "family"):
        response_locale = "fr-CA"
        prompt_influence = "This is an adventure family, bring in the family fun and adventure in the description and reviews summary"

    # Generate product description and reviews summary
    description = generate_description(product, persona, reviews, description_word_limit, response_locale, prompt_influence=None)
    reviews_summary = generate_summary(product, persona, reviews, reviews_word_limit, response_locale, prompt_influence=None)
    
    # Render the HTML template with the generated data
    return render_template("index.html", product=product,reviews_summary=reviews_summary, description=description, persona=persona_req, reviews=customer_reviews)

if __name__ == "__main__":
    # Run the Flask application
    app.run(debug=False)