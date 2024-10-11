import os
import requests
import subprocess
from subprocess import call

# Your GitHub personal access token
GITHUB_TOKEN = ""

# Function for cloning a repository into the 'repos' folder
def clone_repo(repo_url, repo_name):
    repo_dir = os.path.join('repos', repo_name)
    if not os.path.exists(repo_dir):
        os.makedirs('repos', exist_ok=True)
        print(f"Cloning the repository {repo_name} into 'repos' folder...")
        call(['git', 'clone', repo_url, repo_dir])
    else:
        print(f"Repository {repo_name} already exists in 'repos' folder.")

# Get a list of repository files and check if there are files in the required language
def get_repo_contents(owner, repo, language):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        files = response.json()
        for file in files:
            if file['type'] == 'file' and file['name'].endswith(get_file_extension(language)):
                return True
    return False

# Determine the file extension depending on the language
def get_file_extension(language):
    extensions = {
        'Python': '.py',
        'JavaScript': '.js',
        'C++': '.cpp',
        'Java': '.java',
        # Add other languages ​​if needed
    }
    return extensions.get(language, '')

# Search repositories by language
def search_github_repos(language, num_pages=1):
    base_url = "https://api.github.com/search/repositories"
    params = {
        "q": f"language:{language}",
        "sort": "stars",
        "order": "desc",
        "per_page": 30
    }
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }

    repositories = []
    for page in range(1, num_pages + 1):
        params['page'] = page
        response = requests.get(base_url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            repositories.extend(data['items'])
        else:
            print(f"Error: {response.status_code} - {response.json().get('message')}")
            break

    return repositories

def main():
    language = "Python"  # Select language
    num_pages = 1        # Number of pages

    repos = search_github_repos(language, num_pages)

    # Filter and clone only those repositories that contain files in the desired language
    for repo in repos:
        repo_name = repo['name']
        repo_url = repo['html_url']
        owner = repo['owner']['login']
        
        print(f"Checking the repository {repo_name}...")
        
        # Check if there are files in the required language
        if get_repo_contents(owner, repo_name, language):
            print(f"Repository {repo_name} contains code in {language}.")
            clone_repo(repo['clone_url'], repo_name)

            # Run the cleaner.py script to clean the repository
            print(f"Cleaning the repository {repo_name}...")
            subprocess.run(['python3', 'cleaner.py', repo_name])
        else:
            print(f"Repository {repo_name} does not contain code in {language}.")

if __name__ == "__main__":
    main()