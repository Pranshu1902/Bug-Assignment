import requests
import json

username = "Pranshu1902"
res = requests.get(f"https://api.github.com/users/{username}")
res = res.json()

data = {}

# getting user's name
data["name"] = res["name"]

# username
data["username"] = res["login"]

# bio
data["bio"] = res["bio"]

# created_at
data["created_at"] = res["created_at"]

# location
data["location"] = res["location"]

# methods to get tech wise repo counts
def get_repositories(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    return response.json()

def get_topics(repo_url):
    url = f"{repo_url}/topics"
    response = requests.get(url)
    return response.json()

def count_repositories(username):
    repos = get_repositories(username)
    technologies = {}
    total_forks = 0
    total_own = 0

    for repo in repos:
        if repo["fork"]:
            type_ = "forked"
            total_forks += 1
        else:
            type_ = "own"
            total_own += 1

        topics = get_topics(repo["url"])

        for topic in topics["names"]:
            if topic in technologies:
                technologies[topic][type_] += 1
            else:
                technologies[topic] = {"forked": 0, "own": 0}
                technologies[topic][type_] += 1

    data["forked_repos_count"] = total_forks
    data["own_repos_count"] = total_own

    return technologies

# tech wise repository count
data["technology"] = count_repositories(username)

# followers
def get_followers(username):
    url = f"https://api.github.com/users/{username}/followers"
    response = requests.get(url)
    
    if response.status_code == 200:
        return len(response.json())
    else:
        return "Error: {response.status_code}"

data["followers"] = get_followers(username)

# Pull requests
url = f"https://api.github.com/search/issues?q=is:pr+author:{username}&sort=created&order=desc"

# Make a GET request to the URL
response = requests.get(url, headers={"Accept": "application/vnd.github+json"})

# Check if the request was successful
if response.status_code == 200:
    response = response.json()
    items = response["items"]

    open_count = 0
    merged_count = 0
    closed_count = 0

    for item in items:
        if item["state"] == "open":
            open_count += 1
        elif item["state"] == "merged":
            merged_count += 1
        elif item["state"] == "closed":
            closed_count += 1
    
    prs = {"Total PRs": len(items), "Status": {"Open": open_count, "Merged": merged_count, "Closed": closed_count}}
    data["Pull requests"] = prs
else:
    print(f"Error: {response.status_code}")

with open("developer.json", 'a') as json_file:
    json.dump(data, json_file, indent=2)
