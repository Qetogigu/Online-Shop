from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_ai_characteristics(product):
    prompt = f"""
    Analyze the following product and describe its characteristics,features, and best use cases. there should be only text and respond like you are trying to persuade the user:

    Name: {product.name}
    Price: {product.price}
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text

def ai_recommend(products, user_request):
    product_data = ""

    for p in products:
        product_data += f"ID:{p.id} | {p.name} | price:{p.price}\n"

    prompt = f"""
    User request:
    {user_request}

    Available products:
    {product_data}

    TASK:
    - Choose the BEST matching products
    - Return ONLY product IDs
    - Use this format exactly:

    ID:<number> 
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text
