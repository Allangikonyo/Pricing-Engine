# engine/recommender.py
# Builds the prompt and calls the OpenAI API

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def build_prompt(product_name, category, your_price, cost, units_sold,
                 elasticity_label, margin, competitor_data, goal):
    """
    Assembles all the pricing data into a structured prompt for the AI.
    """

    comp_summary = ""
    if competitor_data:
        comp_summary = f"""
Competitor Pricing:
- Average competitor price: ${competitor_data['avg_competitor_price']}
- Lowest competitor price: ${competitor_data['lowest_competitor']}
- Highest competitor price: ${competitor_data['highest_competitor']}
- Your price vs market: {competitor_data['price_gap_percent']}% ({competitor_data['position']})
"""
    else:
        comp_summary = "No competitor data provided."

    prompt = f"""
You are an expert pricing strategist helping an independent seller make smart pricing decisions.

Here is the data about their product:

Product: {product_name}
Category: {category}
Current Price: ${your_price}
Cost to Produce/Source: ${cost}
Profit Margin: {margin}%
Units Sold Per Month: {units_sold}
Price Sensitivity: {elasticity_label}
Seller Goal: {goal}

{comp_summary}

Based on this data, provide a clear and actionable pricing recommendation. Include:
1. Whether they should raise, lower, or hold their price
2. A specific suggested price or price range
3. A plain-English explanation of why (2-3 sentences max)
4. One risk to watch out for

Keep your response friendly, concise, and practical. You are talking directly to a small business owner.
"""
    return prompt


def get_recommendation(product_name, category, your_price, cost, units_sold,
                       elasticity_label, margin, competitor_data, goal):
    """
    Sends the prompt to OpenAI and returns the recommendation.
    """
    prompt = build_prompt(
        product_name, category, your_price, cost, units_sold,
        elasticity_label, margin, competitor_data, goal
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful pricing strategist for small business owners."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=400
    )

    return response.choices[0].message.content
