from bs4 import BeautifulSoup
import requests
import os
import json
from git import Repo
repo = Repo.init('Code\\').git
# TODO: Support for all languages

# Functions
def clear(text: str)->str:
    cleared_text = ""
    for i in text:
        if i not in SPECIAL_CHARACTERS:
            cleared_text += i

    return cleared_text

def send_message(token: str, chat_id: str):
    message = f"Problem {problem['problem_index']} - {problem['problem_name']} has been added to the repository ✅\n\nLink: https://codeforces.com/contest/{problem['contest_id']}/problem/{problem['problem_index']}"

    method = f'sendMessage?chat_id={chat_id}&text={message}'

    url = f'https://api.telegram.org/bot{token}/{method}'
    GET(url)

def GET(*args, **kwargs):
    return requests.get(*args, **kwargs)




# Constants
HANDLE = "YOUR_HANDLE"
URL = f"https://codeforces.com/api/user.status?handle={HANDLE}"
SPECIAL_CHARACTERS = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
TELEGRAM_TOKEN = "TELEGRAM_BOT_TOKEN_FROM_BOT_FATHER"
CHAT_ID = "CHAT_ID"


# Get submissions from codeforces
data = GET(URL, verify=False).json()['result']

# Filter Accepted Submissions
accepted = []
for submission in data:
    if submission['verdict'] == 'OK':
        accepted.append({"submission_id":submission['id'], 
                        "contest_id":submission['contestId'], 
                        "problem_index":submission['problem']['index'],
                        "problem_name": submission['problem']['name'],
                        "problem_tags": ','.join(submission['problem']['tags'])
          })

# Save the data to a json file
with open('data.json', 'w') as f:
    json.dump(accepted, f)


# Scraping the codeforces website for the code of the problems
with open('data.json', 'rb') as f:
    data = json.load(f)

# Get uploaded problems
with open('uploaded.json', 'rb') as f:
    uploaded = json.load(f)


codes = []

for problem in data[::-1]:
    URL = f"https://codeforces.com/contest/{problem['contest_id']}/submission/{problem['submission_id']}"
    PROBLEM_LINK = f"https://codeforces.com/contest/{problem['contest_id']}/problem/{problem['problem_index']}"
    cleared_name = clear(problem['problem_name'])
    FILE_NAME = f'Code\\{problem['problem_index']}\\{problem['problem_index']+' - '+cleared_name}.cpp'
    INDEX = f"Code\\{problem['problem_index']}"
        
    if not os.path.exists(INDEX):   # New index
        os.makedirs(INDEX)

    # Get Code
    r = GET(URL, verify=False)
    soup = BeautifulSoup(r.content, 'html5lib')
    code = soup.select("pre")[0]
    with open(FILE_NAME, 'w') as f:
        f.write(f"// Link To Problem: {PROBLEM_LINK}\n\n")
        f.write(code.text)


    # Check if the problem already exists
    if problem not in uploaded:
        # Add & Commit
        repo.add('*')
        index = Repo.init("Code\\").index
        index.commit(f"{problem['problem_tags']}")
        # Send Message on Telegram
        send_message(TELEGRAM_TOKEN, CHAT_ID)
            


# Update the uploaded file
with open('uploaded.json', 'w') as f:
    json.dump(data, f)

# Push Changes to GitHub
os.system('push.bat')

