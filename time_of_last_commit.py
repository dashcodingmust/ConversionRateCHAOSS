#Note to run this program you must have the below import downloaded else import and run this colab 
import requests

owner = "" #insert file owner here
repo = "" #insert repo name here

#For 1 commit
url = f"https://api.github.com/repos/{owner}/{repo}/commits?per_page=1" #By putting this at =1 only one commit will be called whereas if it was 100 a hundred commits will be called
response = requests.get(url)

last_commit = response.json()[0]
print(last_commit["commit"]['author']['date'])

commits=100 #Setting this to 100, the user can change this to their specifications
url = f"https://api.github.com/repos/{owner}/{repo}/commits?per_page={commits}" 
response = requests.get(url)

last_commit = response.json()[0]
print(last_commit["commit"]['author']['date'])

def lastCommitTime(commits):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits?per_page={commits}" 
    response = requests.get(url)

    last_commit = response.json()[0]
    print(last_commit["commit"]['author']['date'])

