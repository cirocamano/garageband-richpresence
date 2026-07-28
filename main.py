import psutil
import time
from pypresence import Presence
import subprocess

# we just import a lot of stuff i dont care MAKE A VENV

CLIENT_ID = "1531723922599575743"

## take a look if garageband is opened or not
def is_garageband_open():
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] == "GarageBand":
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

## use OSAscirpt to make  garageband tell us what the name of the project is
def get_project_name():
    return subprocess.run(
        [
            "osascript",
            "-e",
            'tell application "System Events" to tell process "GarageBand" to get name of front window',

        ],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


## w just initialize the rpc client for discord make sure you have it spread wide open
def rpc_init():
    rpc = None
    connected = False
    last_project = None

    print("Searching for GarageBand...")

    while True:
        try:
            garageband_open = is_garageband_open()

            if garageband_open:
                if not connected:
                    print("GarageBand found!")
                    rpc = Presence(CLIENT_ID)
                    rpc.connect()
                    connected = True

                project = get_project_name()

                if project != last_project:
                    rpc.update(
                        state="Making Music!",
                        details=f"Proyecto: {project}"[:128],
                        large_image="garageband_logo",
                        large_text="GarageBand for macOS",
                        start=time.time(),
                    )
                    last_project = project
                    print(f"Current project: {project}")

            elif connected:
                print("GarageBand has been closed. Disconnecting...")
                rpc.clear()
                rpc.close()
                rpc = None
                connected = False
                last_project = None

            time.sleep(5)

        except Exception as e:
            print(f"There is a little error: {e}. Retrying...")
            connected = False
            rpc = None
            last_project = None
            time.sleep(15)


# if name blabla
if __name__ == "__main__":
    rpc_init()

