# Telegram Member Manager

Python automation tool for managing Telegram groups.

## Features

- Scrape group members
- Export members to CSV
- Add members to another group
- Flood protection delays

## Technologies

Python
Telethon
CSV data processing

## Usage

1 install dependencies

pip install -r requirements.txt

2 edit config.py

3 run

python main.py


- Project structure

telegram-member-manager
│
├── main.py
├── config.py
├── scraper.py
├── adder.py
├── requirements.txt
├── README.md
├── members.csv
└── added_members.csv
