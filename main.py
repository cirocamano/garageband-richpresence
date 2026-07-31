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

## compatibilty for logic pro
def is_logic_open():
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] == "Logic Pro":
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

## use OSAscirpt to make  garageband tell us what the name of the project is
def get_project_name(app):
    return subprocess.run(
        [
            "osascript",
            "-e",
            f'tell application "System Events" to tell process "{app}" to get name of front window',

        ],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


## w just initialize the rpc client for discord make sure you have it spread wide open
def rpc_init():
    rpc = None
    connected = False
    last_presence = None

    print("Searching for GarageBand or Logic Pro...")

    while True:
        try:
            app = "GarageBand" if is_garageband_open() else "Logic Pro" if is_logic_open() else None

            if app:
                if not connected:
                    print(f"{app} found!")
                    rpc = Presence(CLIENT_ID)
                    rpc.connect()
                    connected = True

                project = get_project_name(app)
                presence = (app, project)

                if presence != last_presence:
                    rpc.update(
                        state="Making Music!",
                        details=f"Proyecto: {project}"[:128],
                        large_image="garageband_logo" if app == "GarageBand" else "logic_logo",
                        large_text=f"{app} for macOS",
                        start=time.time(),
                    )
                    last_presence = presence
                    print(f"Current project: {project}")

            elif connected:
                print("GarageBand or Logic Pro has been closed. Disconnecting...")
                rpc.clear()
                rpc.close()
                rpc = None
                connected = False
                last_presence = None

            time.sleep(5)

        except Exception as e:
            print(f"There is a little error: {e}. Retrying...")
            connected = False
            rpc = None
            last_presence = None
            time.sleep(15)


# if name blabla
if __name__ == "__main__":
    rpc_init()
