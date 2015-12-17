import os
import requests
from pygithub3 import Github

GITHUB_AUTH_USER = "kporangehat"
GITHUB_AUTH_TOKEN = "27e909305f7b73cc9347d19c990d3b951921c5ab"


def _get_user_repo_name_from_url(repo_url):
    split_url = repo_url.split("/")
    return split_url[3], split_url[4]


def _get_url_from_user_repo_name(user, repo_name):
    return os.path.join(GITHUB_URL, user, repo_name)


def load_repo_url(url):
    print "Loading %s" % url
    user, repo_name = _get_user_repo_name_from_url(url)
    gh = Github(user=GITHUB_AUTH_USER, token=GITHUB_AUTH_TOKEN)
    repo = gh.repos.get(user=user, repo=repo_name)
    return repo


def load_readme(repo):
    # /repos/:owner/:repo/readme
    url = os.path.join(repo.url, "readme")
    resp = requests.get(url)
    return resp.json()


def get_user_data(username):
    print "Loading user %s" % username
    gh = Github(user=GITHUB_AUTH_USER, token=GITHUB_AUTH_TOKEN)
    user = gh.users.get(user=username)
    user_data = {
        "avatar_url": user.avatar_url,
        "html_url": user.html_url,
        "name": user.name,
        "company": user.company,
        "login": username
    }

    return user_data


def get_metadata(repo):
    """
    it's important to return empty strings in the case of None
    :param repo:
    :return:
    """
    data = {
        "description": repo.description or "",
        "homepage_gh": repo.homepage or "",
        "readme": load_readme(repo),
        "issues": repo.issues_url or "",
        "updated_at": repo.updated_at,
        "user": get_user_data(repo.owner.login),
    }
    return data


