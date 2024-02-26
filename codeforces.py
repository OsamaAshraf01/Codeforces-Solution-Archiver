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

codes = []

for problem in data:
    URL = f"https://codeforces.com/contest/{problem['contest_id']}/submission/{problem['submission_id']}"
    r = requests.get(URL, verify=False)

    soup = BeautifulSoup(r.content, 'html5lib')

    code = soup.select("pre")
    os.system('mkdir Code\\'+problem['problem_index'])
    with open(f'Code\\{problem['problem_index']}\\{problem['problem_index']+' - '+problem['problem_name']}.cpp', 'w') as f:
        f.write(f"// Link To Problem: https://codeforces.com/contest/{problem['contest_id']}/problem/{problem['problem_index']}\n\n")
        f.write(code[0].text)
    
    repo.add('*')
    index = Repo.init("Code\\").index
    index.commit(f"{problem['problem_tags']}")



# Add origin to the repo and push the changes
os.system('push.bat')

