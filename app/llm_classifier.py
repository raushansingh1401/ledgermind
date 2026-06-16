from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def classify_vendor(
    vendor: str,
    description: str
):

    VALID_CATEGORIES = [
        "Cloud Infrastructure",
        "SaaS Tools",
        "Travel Expense",
        "Meals & Entertainment",
        "Marketing Expense",
        "Office Supplies"
    ]

    prompt = f"""
You are a finance transaction classifier.

Vendor:
{vendor}

Description:
{description}

Possible accounting categories:

- Cloud Infrastructure
- SaaS Tools
- Travel Expense
- Meals & Entertainment
- Marketing Expense
- Office Supplies

Choose ONLY one category from the list above.

Respond ONLY with valid JSON.

Example:
{{
  "category": "SaaS Tools",
  "confidence": 0.88,
  "reason": "Vendor appears to be software subscription provider"
}}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    # Remove markdown if Gemini returns ```json ... ```
    if text.startswith("```json"):
        print("markdown received")
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    try:
        return json.loads(text)

    except Exception:
        return {
            "category": None,
            "confidence": 0.0,
            "reason": f"Failed to parse Gemini response: {text}"
        }