import requests

username = "Kushagra102"
res = requests.get(f"https://raw.githubusercontent.com/{username}/{username}/main/README.md")

print(res._content)
