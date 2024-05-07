import subprocess

def toggle_bluetooth():
    rfkill_output = subprocess.check_output("rfkill list bluetooth", shell=True).decode()
    if 'Soft blocked: yes' in rfkill_output:
        subprocess.call("rfkill unblock bluetooth", shell=True)
    else:
        subprocess.call("rfkill block bluetooth", shell=True)

toggle_bluetooth()
