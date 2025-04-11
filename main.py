from flask import Flask, render_template, request
from app.generator import generate_description, generate_summary
import json

import os
print("Current working directory:", os.getcwd())

app = Flask(__name__)

with open("app/data/products.json") as f:
    product = json.load(f)
    customer_reviews = product["customer_reviews"]
    
with open("app/data/personas.json") as f:
    personas = json.load(f)



@app.route("/", methods=["GET"])
def home():
    
    # Get the 'persona' value from the URL query parameters, default to "family" if not provided
    persona_req = request.args.get("persona", "family")

    # Getting the relevant product reviews based on the selected persona
    reviews = []
    for review in customer_reviews:
        if(review["persona"] == persona_req):
            reviews.append(review)
    
    
    if(persona_req in personas):
        persona = personas[persona_req]

    

    description = generate_description(product, persona, reviews)
    reviews_summary = generate_summary(product, persona, reviews)
    
    return render_template("index.html", product=product,reviews_summary=reviews_summary, description=description, persona=persona_req, reviews=customer_reviews)

if __name__ == "__main__":
    app.run(debug=False)