import os
import json

from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

from .prompt import SYSTEM_PROMPT
from .interpreter import interpret_notes


BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")


api_key = os.getenv("OPENAI_API_KEY")


client = OpenAI(
    api_key=api_key
)



def ask_llm(note):

    try:

        response = client.chat.completions.create(

            model="gpt-4o-mini",

            temperature=0,

            messages=[

                {
                    "role":"system",
                    "content":SYSTEM_PROMPT
                },

                {
                    "role":"user",
                    "content":note
                }

            ]

        )


        output = response.choices[0].message.content


        return json.loads(output)



    except Exception as e:

        print("⚠️ LLM unavailable")
        print("Using rule-based fallback")


        fallback = interpret_notes([note])


        return fallback[0]["structured_adjustment"]