import requests


class BlogRepository:
    def __init__(self):
        self.owner = None
        self.repo = None
        self.last_known_commit = None

    def init_app(self, app):
        github_repo_url = app.config['BLOG_GITHUB_REPO_URL']
        # Assuming URL is in the format 'https://github.com/owner/repo'
        parts = github_repo_url.split('/')
        self.owner = parts[-2]
        self.repo = parts[-1]

        self.last_known_commit = app.config['BLOG_BASE_COMMIT']

    def _get_latest_commit(self):
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/commits/master"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()['sha']

    def get_diff(self):
        latest_commit = self._get_latest_commit()

        added, deleted = self._compare_commits(latest_commit)

        self.last_known_commit = latest_commit
        return added, deleted

    def _compare_commits(self, latest_commit):
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/compare/{self.last_known_commit}...{latest_commit}"
        response = requests.get(url)
        response.raise_for_status()
        comparison_data = response.json()

        added = [file['filename'] for file in comparison_data['files'] if file['status'] in ['added', 'modified']]
        deleted = [file['filename'] for file in comparison_data['files'] if file['status'] in ['removed', 'modified']]
        
        return added, deleted


blog_repository = BlogRepository()


def initialize_blog_repository(app):
    blog_repository.init_app(app)    
