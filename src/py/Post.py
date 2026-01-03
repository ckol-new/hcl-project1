class Post:
    def __init__(self, url: str, post_id: int, title: str, content: list[str], author: Author, date: str, comments: list[Comment]):
        self.url = url
        self.post_id = post_id
        self.title = title
        self.content = content
        self.author = author
        self.date = date
        self.comments = comments