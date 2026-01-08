from sentence_transformers import SparseEncoder, SentenceTransformer, CrossEncoder
from py.model.EmbeddedSentence import EmbeddedSentence
from pathlib import Path
import torch
import numpy as np
import json

class QueryPipeline:
    def __init__(self):
        self.__dense_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.__sparse_model = SparseEncoder('naver/splade-cocondenser-ensembledistil')
        self.__cross_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")

    def query(self, query: str, embedded_path: str or Path, top_n: int = 50, top_k = 5):
        # load database
        print('loading database')
        db = self.load_embedded_db(embedded_path)

        # embed query
        print('embedding query')
        dense_query = self.__dense_model.encode(query, convert_to_numpy=True)
        sparse_query = self.__sparse_model.encode(query)

        # sparse retrieval
        print('sparse retrieval')
        sparse_retrieval_results = self.sparse_retrieval(sparse_query, db, top_n)

        # dense retrieval
        print('sparse retrieval')
        dense_retrieval_results = self.dense_retrievel(dense_query, db, top_n)

        # pool sparse and dense results
        print('pooling results')
        pooled_results = self.pool_results(dense_retrieval_results, sparse_retrieval_results)

        # cross encoder rerank
        print('reranking results')
        reranked_results = self.rerank(pooled_results, query, top_k)

        return reranked_results


    def sparse_retrieval(self, query_vector: torch.tensor, embedded_db: list[EmbeddedSentence], top_n: int = 50) -> list[(EmbeddedSentence, float)]:
        dot_similarities = []
        for embedded_sentence in embedded_db:
            dot_similarities.append(self.dot_similarity(query_vector, embedded_sentence.sparse_embedding))

        sorted_similarities = sorted(enumerate(dot_similarities), key=lambda x: x[1], reverse=True)
        top_n = [(embedded_db[index], value) for index, value in sorted_similarities[:top_n]]
        return top_n


    def dense_retrievel(self, query_vector: np.ndarray, embedded_db: list[EmbeddedSentence], top_n: int = 50) -> list[(EmbeddedSentence, float)]:
        cos_similarities = []
        for embedded_sentence in embedded_db:
            cos_similarities.append(self.cosine_similarity(query_vector, embedded_sentence.dense_embedding))

        sorted_similarities = sorted(enumerate(cos_similarities), key=lambda x: x[1], reverse=True)
        top_n = [(embedded_db[index], value) for index, value in sorted_similarities[:top_n]]
        return top_n

    # pool sparse and dense initial semantic retrieval together, removing all documents
    def pool_results(self, dense_top_n, sparse_top_n):
        pooled: list[(EmbeddedSentence, float)] = dense_top_n + sparse_top_n # concatenate together

        # remove duplicates by text
        seen = set()
        clean_pooled_results = []
        for embedded_sentence, similarity in pooled:
            if embedded_sentence.sentence not in seen:
                seen.add(embedded_sentence.sentence)
                clean_pooled_results.append((embedded_sentence, similarity))

        return clean_pooled_results

    def rerank(self, pooled: list, query_sentence: str, top_k: int = 10) -> list[(EmbeddedSentence, float)]:
        pooled_sentences = [result[0].sentence for result in pooled]
        rerank_results = self.__cross_model.rank(query_sentence, pooled_sentences, return_documents=True)

        # sort rerank results
        sorted_reranked_results = sorted(enumerate(rerank_results), key=lambda x: x[1]['score'], reverse=True)

        # top k embedded sentence objects
        top_k_results: list[(EmbeddedSentence, float)] = [(pooled[index][0], value['score']) for index, value in sorted_reranked_results[:top_k]]
        return top_k_results


    # load a list of Embedded Sentence from embedded vector database file
    def load_embedded_db(self, embedded_path: str or Path) -> list[EmbeddedSentence]:
        db = []
        with open(embedded_path, 'r') as f:
            for line in f:
                embedded_dict = json.loads(line)
                embedded_sentence = EmbeddedSentence.from_dict(embedded_dict)
                db.append(embedded_sentence)
        return db

    # save results (note just save the embedded sentence)
    def save_query_result(self, save_path: str or Path, results: list[(EmbeddedSentence, float)]):
        with open(save_path, 'w') as f:
            for result in results:
                embedded_sentence: EmbeddedSentence = result[0]
                f.write(json.dumps(embedded_sentence.to_dict()))
                f.write('\n')

    # similarity calculations
    # cosine similarity for dense vectors
    def cosine_similarity(self, A: np.ndarray, B: np.ndarray):
        return A.dot(B) / (np.linalg.norm(A) * np.linalg.norm(B))
    # dot product for sparse vectors
    def dot_similarity(self, A: torch.tensor, B: torch.tensor):
        A = A.coalesce()
        B = B.coalesce()

        # make sure dimensions are proper for dot product
        A = A.unsqueeze(0) # 1, D
        B = B.unsqueeze(1) # D, 1

        # calculate dot product
        result = torch.sparse.mm(A, B)
        return result.item()

    # display results
    def display_result(self, results: list):
        for result in results:
            embedded_sentence = result[0]
            similarity = result[1]

            print(embedded_sentence.title)
            print(embedded_sentence.url)
            print(embedded_sentence.sentence_type)
            print(embedded_sentence.sentence)
            print(f'\t similarity is {float(similarity)}')
            print()
