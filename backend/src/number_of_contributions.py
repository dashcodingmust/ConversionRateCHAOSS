import requests
import pandas as pd

# classify contributor
def stage(x, threshold):
    if x == 1:
        return "D0"   # first-time contributor
    elif x >= threshold:
        return "D2"   # regular contributor
    else:
        return "D1"

def investment(owner, repo):

    try:
        threshold = int(input("Enter threshold for regular contributor (default 5): "))
    except ValueError:
        threshold = 5

    url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
    response = requests.get(url)
    data = response.json()

    contributors = pd.DataFrame(data)[["login", "contributions"]]

    # apply classification
    contributors["investment"] = contributors["contributions"].apply(
        lambda x: stage(x, threshold)
    )

    print("\nContributor Classification:")
    print(contributors.head())

    total_D2 = (contributors["investment"] == "D2").sum()
    print("\nConversion rate:", round(total_D2 / len(contributors), 2))
