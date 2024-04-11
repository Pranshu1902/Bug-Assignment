import requests

def get_user_repos_and_languages(username):
    user_repos_url = f"https://api.github.com/users/{username}/repos"

    try:
        response = requests.get(user_repos_url)
        response.raise_for_status()
        user_repos = response.json()

        repos_with_languages = []
        for repo in user_repos:
            repo_languages_url = f"https://api.github.com/repos/{username}/{repo['name']}/languages"
            languages_response = requests.get(repo_languages_url)
            languages_response.raise_for_status()

            languages_data = {
                "repo_name": repo["name"],
                "languages": list(languages_response.json().keys()),
                "topics": repo["topics"]
            }
            repos_with_languages.append(languages_data)

        return repos_with_languages

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []


username = "kushagra102"
user_repos_with_languages = get_user_repos_and_languages(username)
print(user_repos_with_languages)
