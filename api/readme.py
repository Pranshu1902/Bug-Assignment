import requests
from bs4 import BeautifulSoup

username = "Kushagra102"

try:
    res = requests.get(f"https://raw.githubusercontent.com/{username}/{username}/main/README.md")

    if res.status_code == 200:
        html_content = res.content
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extracting text from HTML
        text = soup.get_text()
        
        print(text)
    else:
        print("Failed to fetch README")
except Exception as e:
    print("Error:", e)
