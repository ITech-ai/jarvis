import webbrowser
import subprocess
import os



base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, "commands.txt")

command = {}
with open(file_path, "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        if not line:
            continue
        line = line.replace(",", "")
        key, value = line.split(":", 1)
        key = key.strip().replace('"', '')
        value = value.strip().replace('"', '')

        command[key] = value

def clean_url(url):
    url = url.lower()
    for prefix in ["https://", "http://", "www."]:
        url = url.replace(prefix, "")
    url = url.split("/")[0]
    parts = url.split(".")
    return parts[0]
def run_command(text):
    try:
        text = text.lower()

        for key in command:

            if key in text:
                value = command[key]
                # __________________site______________
                if value.startswith("http"):

                    webbrowser.open(value)
                    
                    return None

                # __________________-app______________
                elif value.endswith(".exe"):

                    subprocess.Popen(value, shell=True)
                    return None
                elif value.endswith(".ord"):
                    return value

        return text
    except:pass

