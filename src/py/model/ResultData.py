from pathlib import Path
from py.model.Post import Post


class ResultData:
    def __init__(self, title: str, url: str, post_id: int, similarity: float, sentence: str, context: list[str], data_origin: str or Path, line_number: int, post: Post):
        self.title = title
        self.url = url
        self.post_id = post_id,
        self.similarity = similarity
        self.sentence = sentence,
        self.context = context
        self.data_origins = data_origin
        self.line_number=line_number
        self.post = post

    def to_dict(self):
        return {
            'title': self.title,
            'url': self.url,
            'post_id': self.post_id,
            'similarity': self.similarity,
            'sentence': self.sentence,
            'context': self.context,
            'data_origin': self.data_origins,
            'line_number': self.line_number,
            'post': self.post.to_dict()
        }

    @classmethod
    def from_dict(cls, data):
        post_data = data['post']
        post = Post.from_dict(post_data)
        return cls(
            title=data['title'],
            url=data['url'],
            post_id=data['post_id'],
            similarity=data['similarity'],
            sentence=data['sentence'],
            context=data['context'],
            data_origin=data['data_origin'],
            line_number=data['line_number'],
            post=post
        )

    def __eq__(self, other):
        if not isinstance(other, ResultData): return False
        return (
            self.title == other.title and
            self.url == other.url and
            self.post_id == other.post_id and
            self.similarity == other.similarity and
            self.sentence == other.sentence and
            self.context == other.context and
            self.data_origins == other.data_origins and
            self.line_number == other.line_number and
            self.post == other.post
        )

