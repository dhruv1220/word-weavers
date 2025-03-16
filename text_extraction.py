import subprocess
from llm_call import llm_call

def extract_text_with_gemma3(file_path):
    # Build the command as a string exactly as you use in the terminal
    command = f"Extract the text from image without any initial or trailing text {file_path}"
    return llm_call(command)

if __name__ == "__main__":
    file_path = "/Users/vineetarora/Desktop/word-weavers/test_img.png"
    output = extract_text_with_gemma3(file_path)
    print("Gemma3 output:")
    print(output)
