from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def classify_vendor(
    vendor: str,
    description: str
):

    prompt = f"""
You are a finance transaction classifier.

Vendor:
{vendor}

Description:
{description}

Choose the most likely accounting category.

Possible categories:
- Cloud Infrastructure
- SaaS Tools
- Travel Expense
- Meals & Entertainment
- Marketing Expense
- Office Supplies

Return only:
Category:
Confidence:
Reason:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text