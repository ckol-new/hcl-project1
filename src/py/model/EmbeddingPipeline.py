import sentence_transformers
from sentence_transformers import SentenceTransformer, SparseEncoder
from Post import Post
from EmbeddedSentence import EmbeddedSentence
from pathlib import Path

# embedding pipeline handles the embedding of scraped data
class EmbeddingPipeline:
    def __init__(self):
        self.index = 0 # index field is the index of the current sentences being embedded, is tracked as a part of tracking info
        self.cur_post_location = 0 # field of the line number currently being embedded

    def load_post(self, data: str) -> Post:
        post = Post.from_dict(json.loads(data))
        return post

    def embed_sentence(self, sentence: str, sentence_type: str, url: str, title: str) -> EmbeddedSentence:
        dense_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        sparse_model = SparseEncoder('naver/splade-cocondenser-ensembledistil')

        dense_embedded_sentence = dense_model.encode(sentence)
        sparse_embedded_sentence = sparse_model.encode(sentence)

        embedded_sentence = EmbeddedSentence(
            sentence,
            dense_embedded_sentence,
            sparse_embedded_sentence,
            url=url,
            title=title,
            post_location=self.cur_post_location,
            sentence_type=sentence_type
        )

        return embedded_sentence

    # embed each sentence in the post
    # return a list of embedded sentences
    def embed_post(self, post: Post) -> (list[EmbeddedSentence]):
        types = {
            1: 'post-title',
            2: 'post-content',
            3: 'comment-content'
        }
        embeddings = []

        embed_title = self.embed_sentence(post.title, types[1], url=post.url, title=post.title)
        embeddings.append(embed_title)
        self.index += 1

        for sentence in post.content:
            embed_content_sentence = self.embed_sentence(sentence, types[2], url=post.url, title=post.title)
            embeddings.append(embed_content_sentence)
            self.index += 1

        for comment in post.comments:
            for sentence in comment.content:
                embed_comment_sentence = self.embed_sentence(sentence, types[3], url=post.url, title=post.title)
                embeddings.append(embed_comment_sentence)
                self.index += 1

    def embed_scraped_data(self, scrape_path: str or Path, limit: int = None) -> list[EmbeddedSentence]:
        length = 0
        embeddings = []

        with open(scrape_path, 'r') as f:
            length = sum(1 for _ in f)

        with open(scrape_path, 'r') as f:
            num = 0
            # for line in file
            for line in f:
                if limit:
                    if num >= limit: break
                if num % 10 == 0:
                    print(f'%{(num / length) * 100}')
                num += 1

                # load post
                post = self.load_post(line)

                # get embedded sentences
                post_embeddings = self.embed_post(post)
                embeddings = embeddings + post_embeddings

                self.cur_post_location += 1

        return embeddings

    def save_embedded_data(self, embeddings: list[EmbeddedSentence], embed_path: str or Path):
        with open(embed_path, 'r') as f:
            for embedding in embeddings:
                f.write(json.dumps(embedding.to_dict()))
                f.write('\n')

    def run_pipeline(self, scrape_path: str or Path, embedding_path: str or Path, limit: int = None):
        embeddings = self.embed_scraped_data(scrape_path, limit)
        self.save_embedded_data(embeddings, embedding_path)
