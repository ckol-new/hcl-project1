from Author import Author
from Comment import Comment

# post object holds all data around a given forum post
# post object contains author object and list of comment objects
# post objects is serializable to and from json
class Post:
    def __init__(self, url: str, post_id: int, title: str, content: list[str], author: Author, date: str, comments: list[Comment]):
        self.url = url
        self.post_id = post_id
        self.title = title
        self.content = content
        self.author = author
        self.date = date
        self.comments = comments

    def to_dict(self):
        return {
            'url': self.url,
            'post_id': self.post_id,
            'title': self.title,
            'content': self.content,
            'author': self.author.to_dict(),
            'date': self.date,
            'comments': [
                Comment.from_dict(comment) for comment in self.comments if self.comments
            ]
        }

    @classmethod
    def from_dict(cls, data):
        comments_data = data['comments']
        comments = []
        if comments_data:
            for comment in comments_data:
                comment = Comment.from_dict(comment)
                comments.append(comment)

        return cls(
            url=data['url'],
            post_id=data['post_id'],
            title=data['title'],
            content=data['content'],
            author=Author.from_dict(data['author']),
            date=data['date'],
            comments=comments
        )

    def __eq__(self, other):
        if not isinstance(other, Post): return False
        return (
            self.url == other.url and
            self.post_id == other.post_id and
            self.date == other.date and
            self.author == other.author and
            self.title == other.title and
            self.content == other.content and
            self.comments == other.comments
        )