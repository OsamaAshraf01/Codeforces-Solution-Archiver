# Codeforces Solution Uploader
This Python script automates uploading your accepted Codeforces solutions to your GitHub repository.

## Requirements
- Python 3
- Libraries:
    - requests
    - beautifulsoup4
    - json
    - os
    - GitPython
- A GitHub account and pre-made repo

## Features
- Scrapes Codeforces website to find your accepted solutions.
- Creates a new repository on your PC if it doesn't already exist.
- Commit each problem with message contains its tags
- Uploads each solution as a separate C++ file named after the problem code and title (e.g., "A - Problem.cpp").

## Instructions:
- Install the required libraries using pip:
	```
	pip install bs4
	pip install requests
	pip install json
	pip install os
	pip install GitPython
	```

- Put your Codeforces handle

- Put your Telegram Bot's token & Chat ID to send messages
>[!Tip] If you don't have bot token, you can get one using <a href="https://telegram.me/BotFather">BotFather</a>

- Add 'auto_run.bat' file to your task scheduler to run automatically everyday

