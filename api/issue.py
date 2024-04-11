import requests

def get_issue(username, repo):
    """Fetches and parses GitHub issue data.

    Args:
        username (str): The GitHub username of the repository owner.
        repo (str): The name of the repository.

    Returns:
        list: A list of dictionaries containing issue details,
              or an empty list if the request fails.
    """

    url = f"https://api.github.com/repos/{username}/{repo}/issues"
    try:
        response = requests.get(url)
        response.raise_for_status()

        data = []
        for issue in response.json():
            dict_data = {
                "number": issue["number"],
                "title": issue["title"],
                "body": issue.get("body", ""),
                "state": issue["state"],
                "created_at": issue["created_at"],
                "label_name": issue.get("labels") != [] and issue.get("labels")[0].get("name", "default") or "default",
                "assignee_name": issue.get("assignees") != [] and issue.get("assignees")[0].get("login", "default") or "default"
            }
            data.append(dict_data)

        return data

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching issues: {e}")
        return []







if __name__ == "__main__":
    username = "Pranshu1902"
    repo = "Bug-Assignment"

    data = get_issue(username, repo)
    print(data)


