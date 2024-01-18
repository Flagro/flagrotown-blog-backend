import git


class BlogRepository:
    def __init__(self):
        self.github_repo_url = None
        self.last_known_commit = None

    def init_app(self, app):
        self.github_repo_url = app.config['BLOG_GITHUB_REPO_URL']

    def get_diff(self):
        # request the latest commit from the self.github_repo_url
        # git diff the latest commit with the self.last_known_commit
        # Delete all the deleted/updated files
        # Add all the new/updated files
        pass
    

blog_repository = BlogRepository()


def initialize_blog_repository(app):
    blog_repository.init_app(app)    
