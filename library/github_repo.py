import os
import requests
from pygithub3 import Github
import semantic_version
import datetime

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

def load_date_from_commit(repo_url, sha):
    user, repo_name = _get_user_repo_name_from_url(repo_url)
    gh = Github(user=GITHUB_AUTH_USER, token=GITHUB_AUTH_TOKEN)
    commit = gh.git_data.commits.get(sha=sha, user=user, repo=repo_name)
    return commit.author.date

def load_versions(repo_url, release_type):
    user, repo_name = _get_user_repo_name_from_url(repo_url)
    gh = Github(user=GITHUB_AUTH_USER, token=GITHUB_AUTH_TOKEN)
    releases = []
    if release_type == "tags":
        # get tags list
        result = gh.repos.list_tags(user=user, repo=repo_name)
        # filter them down to semantic version tags
        # store them as a list of dicts with version and sha we can use to lookup the date (todo)
        for tag in result.iterator():
            try:
                # for testing purposes, we'll allow the 'v' but this isn't technically valid.
                tag_name = tag.name
                if tag_name.startswith('v'):
                    tag_name = tag.name[1:]
                v = semantic_version.Version(tag_name)

            except ValueError:
                # invalid tag, skip it
                pass
            else:
                release_date = load_date_from_commit(repo_url, tag.commit.sha)
                releases.append({'name': tag_name, 'sha': tag.commit.sha, 'date': release_date,
                                 'download': tag.zipball_url,
                                 'url': 'https://github.com/%s/%s/tree/%s' % (user, repo_name,
                                                                              tag.name)})
    else:
        result = gh.repos.list_branches(user=user, repo=repo_name)
        branch = [b for b in result.all() if b.name == release_type]
        if branch:
            release_date = load_date_from_commit(repo_url, branch[0].commit.sha)
            release_name = datetime.datetime.strftime(release_date, "%Y.%m.%d.%H.%M.%S")
            releases = [{'name': release_name, 'sha': branch[0].commit.sha, 'date': release_date,
                         'url': 'https://github.com/%s/%s/tree/%s' % (user, repo_name,
                                                                      release_type)}]

    return releases


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


