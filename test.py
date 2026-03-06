import requests

token = "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"

headers = {
    "Authorization": f"token {token}"
}

response = requests.get("https://api.github.com/user", headers=headers)

print("Status Code:", response.status_code)
print("Response:", response.text)