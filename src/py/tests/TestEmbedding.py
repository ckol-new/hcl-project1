from pathlib import Path
import json
from py.model.EmbeddingPipeline import EmbeddingPipeline
from py.model.EmbeddedSentence import EmbeddedSentence
# test embedding
def test(scrape_path: str or Path, embed_path: str or Path, limit: int = 5, count: int = 1) -> None:
    test_embedding(scrape_path, embed_path, limit)
    test_loading_embed_sentence(embed_path, count)

# def make sure embedding works
def test_embedding(scrape_path: str or Path, embed_path: str or Path, limit: int = 5) -> None:
    pipeline = EmbeddingPipeline()
    pipeline.run_pipeline(
        scrape_path,
        embed_path,
        limit
    )

    with open(embed_path, 'r') as f:
        # count lines to make sure the file was actually written to
        s = 0
        for line in f:
            s += 1

        print(s)

def test_loading_embed_sentence(embed_path: str or Path, count: int = 1) -> EmbeddedSentence:
    with open(embed_path, 'r') as f:
        line = None
        for i in range(count):
            line = f.readline()
            data = json.loads(line)

            # try to deserialize object from line
            embed_sentence = EmbeddedSentence.from_dict(data)

            print(embed_sentence.sentence)
            print(embed_sentence.title)
            print(embed_sentence.url)
            print(embed_sentence.sentence_type)



