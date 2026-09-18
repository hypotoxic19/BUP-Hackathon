from .llm_client import ask_llm


note = """
Solar generation will decrease by 50%
between 2 PM and 4 PM
"""


result = ask_llm(note)


print(result)