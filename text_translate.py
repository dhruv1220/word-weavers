import subprocess
from llm_call import llm_call

def translate_english_to_spanish(english_text: str):
    # Build the command as a string exactly as you use in the terminal
    command = f"Translate the following text to Spanish without any initial or trailing text: {english_text}"
    return llm_call(command)

if __name__ == "__main__":
    english_text = "Hi! My name is Dhruv."
    output = translate_english_to_spanish(english_text)
    print("Gemma3 output:")
    print(output)