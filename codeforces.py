from bs4 import BeautifulSoup
import requests
import os
import json
from git import Repo
repo = Repo.init('Code\\').git

# Get submissions from codeforces
handle = "YOUR_HANDLE"
URL = f"https://codeforces.com/api/user.status?handle={handle}"
data = requests.get(URL, verify=False).json()['result']
SPECIAL_CHARACTERS = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']



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
        r = requests.get(URL, verify=False)

        soup = BeautifulSoup(r.content, 'html5lib')

        code = soup.select("pre")
        if not os.path.exists('Code\\'+problem['problem_index']):
            os.makedirs('Code\\'+problem['problem_index'])

        cleared_name = ''
        for i in problem['problem_name']:
            if i not in SPECIAL_CHARACTERS:
                cleared_name += i

        with open(f'Code\\{problem['problem_index']}\\{problem['problem_index']+' - '+cleared_name}.cpp', 'w') as f:
            f.write(f"// Link To Problem: https://codeforces.com/contest/{problem['contest_id']}/problem/{problem['problem_index']}\n\n")
            f.write(code[0].text)
        
        repo.add('*')
        index = Repo.init("Code\\").index
        index.commit(f"{problem['problem_tags']}")


        if problem not in uploaded:
            # Send Message on Telegram
            token = 'YOUR_BOT_TOKEN'
            chat_id = 'CHAT_ID'
            message = f"Problem {problem['problem_index']} - {problem['problem_name']} has been added to the repository ✅\n\nLink: https://codeforces.com/contest/{problem['contest_id']}/problem/{problem['problem_index']}"

            method = f'sendMessage?chat_id={chat_id}&text={message}'

            URL = f'https://api.telegram.org/bot{token}/{method}'
            r = requests.get(URL)


# Update the uploaded file
with open('uploaded.json', 'w') as f:
    json.dump(data, f)

# Push Changes to GitHub
os.system('push.bat')

