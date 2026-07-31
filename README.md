# GarageBand / Logic Pro Rich Presence

Shows your current GarageBand or Logic Pro project as a Discord Rich Presence status.

## Requirements

- macOS with GarageBand or Logic Pro
- Discord Desktop
- Python 3

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## macOS permission

The script reads the DAW window title to find the project name. Allow
your terminal app under **System Settings > Privacy & Security > Accessibility**.
macOS may also request permission to control **System Events**.

## Usage

Open Discord Desktop and GarageBand or Logic Pro, then run:

```bash
source .venv/bin/activate
python main.py
```

The presence updates when you change projects and clears when GarageBand
closes. Stop the script with `Ctrl+C`.

> The active project name is shown on your Discord profile while the script is
> running.
