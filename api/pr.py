import requests
from github import Github
from github import Auth
from dotenv import load_dotenv
import os

load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")

auth = Auth.Token(github_token)

g = Github(auth=auth)

def get_pr(username, state):
    """Fetches and parses GitHub PR data.

    Args:
        username (str): The GitHub username of the repository owner.
        state (str): The type of PR, either 'open' or 'closed'.

    Returns:
        list: A list of dictionaries containing PR details,
              or an empty list if the request fails.
    """
    try:
        pr_issues = g.search_issues('', state=state, author=username, type='pr')
        data = [] 
        for i in range(pr_issues.totalCount):
            dict_data = {
                "number": i+1,
                "issue_title": pr_issues.get_page(0)[i].title,
                "issue_body": pr_issues.get_page(0)[i].body
            }
            data.append(dict_data)
        return data
    except e:
        print(f"Error in fetching PRs: {e}")
        return []

g.close()

print(get_pr("Kushagra102", "open"))