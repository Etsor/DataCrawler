@echo off

python3 -m venv .venv

call .venv\Scripts\activate

pip3 install -r requirements.txt

python3 -m src.main
