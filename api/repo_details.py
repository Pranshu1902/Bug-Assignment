import requests
from datetime import datetime

merged_data = {}

projects = [
    {"username": "wagtail", "repo": "wagtail"},
    {"username": "google-research", "repo": "bert"},
    {"username": "microsoft", "repo": "generative-ai-for-beginners"},
    {"username": "openai", "repo": "whisper"},
    {"username": "twitter", "repo": "twitter-server"}
]

for project in projects:
  username = project["username"]
  repo = project["repo"]

  url = "https://api.github.com/repos/"+username+"/"+repo

  res = requests.get(url=url)
  res = res.json()

  data = {}

  def get_language():
    data["language"] = res["language"]
    return res["language"]

  def get_topics():
    data["topics"] = res["topics"]
    return res["topics"]

  data["forks"] = res["forks_count"]
  data["description"] = res["description"]
  data["no_of_issues"] = res["open_issues_count"]
  data["open_issues_count"] = res["open_issues_count"]

  get_language()
  get_topics()

  # issues
  issues = requests.get(url+"/issues")
  issues = issues.json()

  issue_data = {"titles": []}

  issue_data["count"] = len(issues)
  for issue in issues:
    issue_data["titles"].append(issue["title"])

  data["issues"] = issue_data

  # number of contributors
  contributors = requests.get(url+"/contributors")
  contributors = contributors.json()
  data["number_of_contributors"] = len(contributors)

  # number of PRs
  pulls = requests.get(url+"/pulls")
  pulls = pulls.json()
  data["number_of_prs"] = len(pulls)

  # date created
  data["created_at"] = datetime.strptime(res['created_at'], "%Y-%m-%dT%H:%M:%SZ")

  # archived
  data["is_archived"] = res["archived"]


  # put final data in main variable
  merged_data[repo] = data

print("Data fetched!")

# saving the data to a json file
import json

with open("data.json", 'a') as json_file:
    json.dump(merged_data, json_file, indent=2)
