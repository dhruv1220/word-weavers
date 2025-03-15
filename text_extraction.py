import subprocess

def extract_text_with_gemma3(file_path):
    # Build the command as a string exactly as you use in the terminal
    command = f'ollama run gemma3 "Extract the text from image {file_path}"'
    
    try:
        # Run the command using shell=True to mimic your terminal environment
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("Error running command:")
        print(e.stderr)
        return None

if __name__ == "__main__":
    # Ensure this file path is accessible by gemma3 (same as your terminal)
    file_path = "/Users/vineetarora/Desktop/word-weavers/test_img.png"
    output = extract_text_with_gemma3(file_path)
    print("Gemma3 output:")
    print(output)
