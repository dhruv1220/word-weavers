import subprocess

def llm_call(command_temp: str):
    command = f'ollama run gemma3 "{command_temp}"'
    try:
        # Run the command using shell=True to mimic your terminal environment
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("Error running command:")
        print(e.stderr)
        return None