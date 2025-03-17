import subprocess
import shlex

def llm_call(command_temp: str):
    # Safely quote the command_temp to avoid shell syntax issues.
    command = f'ollama run gemma3 {shlex.quote(command_temp)}'
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("Error running command:")
        print(e.stderr)
        return None
