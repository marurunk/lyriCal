import subprocess

def notify(title:str, description:str):
    subprocess.run(
        ["notify-send", "-u", "normal", "-i", " ", title, description],
        check=True)
