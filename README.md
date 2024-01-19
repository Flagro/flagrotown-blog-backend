This is an implementation for my personal blog at: [blog.flagrotown.com](https://blog.flagrotown.com)
The frontend implementation is at: [flagrotown-blog](https://github.com/Flagro/flagrotown-blog)

The backend is written in Flask with 3 microservices:
- auth service for OAuth2 with google
    - implemented with Authlib library
- blog posts service for managing blog texts and images
    - implemented with PostgreSQL, SQLAlchemy, AWS S3 + Boto3, GitHub Webhooks and GitHub API
- blog metrics service for mangaing upvotes/comments
