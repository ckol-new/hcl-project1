import numpy as np

# embedded sentence object contains a sentence, it's dense and sparse embeddings, as well as meta data and tracking info.
# my embedded data set will contain a bunch of embedded objects.

# tracking info_metadata: url to post, title of post, line number of post object in json
class EmbeddedSentence:
    def __init__(self, sentence: str, dense_embedding, sparse_embedding, url: str, title: str, post_location: int, sentence_type: str):
        self.sentence = sentence
        self.dense_embedding = dense_embedding
        self.dense_embedding_shape = dense_embedding.shape
        self.sparse_embedding = sparse_embedding
        self.sparse_embedding_shape = sparse_embedding.shape
        self.url = url
        self.title = title
        self.post_location = post_location
        self.sentence_type = sentence_type

    def to_dict(self):
        return {
            'sentence': self.sentence,
            'dense_embedding': {
                '__np_arr': True,
                'dtype': str(self.dense_embedding.dtype),
                'shape': str(self.dense_embedding_shape),
                'vector': self.dense_embedding.tolist()
            },
            'sparse_embedding': {
                '__np_arr': True,
                'dtype': str(self.sparse_embedding.dtype),
                'shape': str(self.sparse_embedding_shape),
                'vector': self.dense_embedding.tolist()
            },
            'url': self.url,
            'title': self.title,
            'post_location': self.post_location,
            'sentence_type': self.sentence_type
        }

    @classmethod
    def from_dict(cls, data):
        dense_data = data['dense_embedding']
        dense_embedding = np.array(dense_data['vector'], dtype=dense_data['dtype'])
        sparse_data = data['sparse_embedding']
        sparse_embedding = np.array(sparse_data['vector'], dtype=sparse_data['dtype'])
        return cls(
            sentence=data['sentence'],
            dense_embedding=dense_embedding,
            sparse_embedding=sparse_embedding,
            url =data['url'],
            title=data['title'],
            post_location=data['post_location'],
            sentence_type=data['sentence_type']
        )

    def __eq__(self, other):
        if not isinstance(other, EmbeddedSentence): return False
        return (
            self.sentence == other.sentence and
            np.array_equal(self.dense_embedding, other.dense_embedding) and
            self.dense_embedding_shape == other.sparse_embedding_shape and
            self.sparse_embedding_shape == other.sparse_embedding_shape and
            np.array_equal(self.sparse_embedding, other.sparse_embedding) and
            self.url == other.url and
            self.title == other.title and
            self.post_location == other.post_location,
        )