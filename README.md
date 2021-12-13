# hanabi-show

Written with python3.10.1

----

### If your OS Maintains compatibility with the Ubuntu repositories

With this README is in your terminal's current working directory (CWD), the following commands should set up and run this project

- `sudo apt update && sudo apt upgrade -y`
- `sudo add-apt-repository ppa:deadsnakes/ppa`
- `sudo apt install python3.10`
- `sudo apt install python3.10-venv`
- `sudo apt-get install python3.10-tk`
- `python3.10 -m venv .venv`
- `source .venv/bin/activate`
- `python -m pip install --upgrade pip`
- `python -m pip install -r requirements.txt`
- `python main.py`

### Update requirements.txt

- `python -m pip freeze > requirements.txt`