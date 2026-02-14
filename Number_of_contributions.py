#Note to run this program you must have both the below imports downloaded else run on colab
import requests
import pandas as pd

#This function is to evaulate the level of investment for each contributor
def stage(x): 
  if x==1: return "D0"  #This is a first time commiter or contributor
  elif x>5: return "D2" #This is a regular commitor
  else: return "D1" 
    
def investment(owner,repo):
  
  url = f"https://api.github.com/repos/{owner}/{repo}/contributors" 
  response = requests.get(url)
  data = response.json()
  
  contributors = pd.DataFrame(data)[["login", "contributions"]]
  print(contributors.head()) #This will print out each contributors with their number of commits
  contributors["investment"]=contributors["contributions"].apply(stage)
  print(contributors.head())
