#Note to run this program you must have the below import downloaded else import and run this colab 
import requests

def lastCommitTime(commits,ownre,repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits?per_page={commits}" 
    response = requests.get(url)

    last_commit = response.json()[0]
    print(last_commit["commit"]['author']['date'])

