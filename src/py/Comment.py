class Comment:
    def __init__(self, url: str, post_id: int, date: str,  author: Author, content: list[str]):
        self.url = url
        self.post_id = post_id
        self.author = author
        self.date = date
        self.contetn = content