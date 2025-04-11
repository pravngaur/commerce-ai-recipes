from app.model_call import generate_prod_description, generate_reviews_summary


def generate_description(product, persona, reviews):
    
    response = ""
    if(product == None or persona == None  or reviews == None):
        return response
    else:
        response = generate_prod_description(product, persona, reviews)
    
    return response

def generate_summary(product, persona, reviews):
    
    response = ""
    if(product == None or persona == None  or reviews == None):
        return response
    else:
        response = generate_reviews_summary(product, persona, reviews)
    
    return response
