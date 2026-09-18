import os
import json
import google.generativeai as genai

from dotenv import load_dotenv

from .prompt import SYSTEM_PROMPT
from .interpreter import interpret_notes


load_dotenv()


genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)


model = genai.GenerativeModel(
    "gemini-2.5-flash"
)



def ask_llm(note):

    try:

        prompt = f"""

{SYSTEM_PROMPT}


Operator instruction:

{note}


Return ONLY JSON.
No explanation.

"""


        response = model.generate_content(
            prompt
        )


        text = response.text.strip()


        return json.loads(text)



    except Exception as e:


        print(
            "Gemini unavailable, using fallback"
        )


        return interpret_notes([note])[0]["structured_adjustment"]