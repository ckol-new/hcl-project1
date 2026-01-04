from py.model.Author import Author

# comment object holds all data around an individual comment, as well as tracking data back to the post it belongs to
# comment objects contains the author object of the comment
# comment object is fully serializable to and from json
class Comment:
    def __init__(self, url: str, post_id: int, date: str,  author: Author, content: list[str]):
        self.url = url
        self.post_id = post_id
        self.author = author
        self.date = date
        self.content = content

    def to_dict(self) -> dict:
        return {
            'url': self.url,
            'post_id': self.post_id,
            'date': self.date,
            'author': self.author.to_dict(),
            'content': self.content
        }

    @classmethod
    def from_dict(cls, data):
         return cls(
             url=data['url'],
             post_id=data['post_id'],
             date=data['date'],
             author=Author.from_dict(data['author']),
             content=data['content']
         )

    def __eq__(self, other):
        if not isinstance(other, Comment): return False
        return (
            self.url == other.url and
            self.post_id == other.post_id and
            self.date == other.date and
            self.author == other.author and
            self.content == other.content
        )