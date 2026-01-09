import pathlib

import requests
from bs4 import BeautifulSoup
import pprint

import py.tests.TestSerialization as ts
from py.model.ScrapingPipeline import ALZConnectedScrapingPipeline
from py.model.EmbeddingPipeline import EmbeddingPipeline
from py.model.QueryPipeline import QueryPipeline

base = r'C:\Users\wslam\Everything\health_city_lab\project1\hcl-project\src\data'
path = pathlib.Path(base)
early_onset_test = {
    'url_base': 'https://alzconnected.org/categories/i-have-younger-onset-alzheimers',
    'num_pages': 10,
    'seed_path': path / 'Seeds_Output' / 'ALZConnected' / 'test.txt',
    'crawl_path': path / 'Crawl_Output' / 'ALZConnected' / 'test.txt',
    'scrape_path': path / 'Scrape_Output' / 'ALZConnected' / 'test.txt',
    'embedding_path': path / 'Embed_Output' / 'ALZConnected' / 'test.jsonl',
    'results_path': path / 'Results' / 'test.jsonl'
}
early_onset = {
    'url_base': 'https://alzconnected.org/categories/i-have-younger-onset-alzheimers',
    'num_pages': 10,
    'seed_path': path / 'Seeds_Output' / 'ALZConnected' / 'early_onset_seed.txt',
    'crawl_path': path / 'Crawl_Output' / 'ALZConnected' / 'early_onset_crawl.txt',
    'scrape_path': path / 'Scrape_Output' / 'ALZConnected' / 'early_onset_scrape.jsonl',
    'embedding_path': path / 'Embed_Output' / 'ALZConnected' / 'early_onset_embedding.jsonl',
    'results_path': path / 'Results' / 'test.jsonl'
}
dementia_or_other = {
    'url_base': 'https://alzconnected.org/categories/i-have-alzheimers-or-other-dementia',
    'num_pages': 11,
    'seed_path': path / 'Seeds_Output' / 'ALZConnected' / 'dementia_or_other_seeds.txt',
    'crawl_path': path / 'Crawl_Output' / 'ALZConnected' / 'dementia_or_other_crawl.txt',
    'scrape_path': path / 'Scrape_Output' / 'ALZConnected' / 'dementia_or_other_scrape.jsonl',
    'embedding_path': path / 'Embed_Output' / 'ALZConnected' / 'dementia_or_other_embedding.jsonl',
    'results_path': path / 'Results' / 'dementia_or_other_results.jsonl'
}
caregiver_general_p1_100= {
    'url_base': 'https://alzconnected.org/categories/i-am-a-caregiver-(general-topics)',
    'num_pages': 100,
    'seed_path': path / 'Seeds_Output' / 'ALZConnected' / 'caregiver_general_p1_100_seeds.txt',
    'crawl_path': path / 'Crawl_Output' / 'ALZConnected' / 'caregiver_general_p1_100_crawl.txt',
    'scrape_path': path / 'Scrape_Output' / 'ALZConnected' / 'caregiver_general_p1_100_scrape.jsonl',
    'embedding_path': path / 'Embed_Output' / 'ALZConnected' / 'caregiver_general_p1_100_embedding.jsonl',
    'results_path': path / 'Results' / 'caregiver_general_p1_100_results.jsonl'
}
caregiver_general_p101_188= {
    'url_base': 'https://alzconnected.org/categories/i-am-a-caregiver-(general-topics)',
    'page_start': 101,
    'num_pages': 188,
    'seed_path': path / 'Seeds_Output' / 'ALZConnected' / 'caregiver_general_p101_188_seeds.txt',
    'crawl_path': path / 'Crawl_Output' / 'ALZConnected' / 'caregiver_general_p101_188_crawl.txt',
    'scrape_path': path / 'Scrape_Output' / 'ALZConnected' / 'caregiver_general_p101_188_scrape.jsonl',
    'embedding_path': path / 'Embed_Output' / 'ALZConnected' / 'caregiver_general_p101_188_embedding.jsonl',
    'results_path': path / 'Results' / 'caregiver_general_p101_188_results.jsonl'
}

def testing():
    url = 'https://alzconnected.org/discussion/comment/260911#Comment_260911?utm_source=community-search&utm_medium=organic-search&utm_term=Working'
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    div_discussion = soup.find('div', class_='Discussion')
    div_content = soup.find('div', class_='Message userContent')
    arr = div_content.find_all('p')
    for p in arr:
        if p.string: print(p.string)
        else: print(p.get_text(separator='\n'))


def scrape1():
    s_pipeline = ALZConnectedScrapingPipeline()
    e_pipeline = EmbeddingPipeline()

    s_pipeline.run_pipeline(
        url_base=early_onset['url_base'],
        seed_path=early_onset['seed_path'],
        seed_num=early_onset['num_pages'],
        crawl_path=early_onset['crawl_path'],
        scrape_path=early_onset['scrape_path']
    )

    e_pipeline.run_pipeline(
        scrape_path=early_onset['scrape_path'],
        embedding_path=early_onset['embedding_path']
    )
def scrape_queue():
    s_pipeline = ALZConnectedScrapingPipeline()
    e_pipeline = EmbeddingPipeline()


    e_pipeline.run_pipeline(
        scrape_path=early_onset['scrape_path'],
        embedding_path=early_onset['embedding_path'],
    )

    s_pipeline.run_pipeline(
        url_base=dementia_or_other['url_base'],
        seed_path=dementia_or_other['seed_path'],
        seed_num=dementia_or_other['num_pages'],
        crawl_path=dementia_or_other['crawl_path'],
        scrape_path=dementia_or_other['scrape_path']
    )

    e_pipeline.run_pipeline(
        scrape_path=dementia_or_other['scrape_path'],
        embedding_path=dementia_or_other['embedding_path'],
    )


def query_single():
    q_pipeline = QueryPipeline()
    query_text= "Does my diagnosis have to take more than a year?"
    results = q_pipeline.query(
        query_text,
        dementia_or_other['embedding_path'],
        top_n=100,
        top_k=20
    )
    q_pipeline.display_result(results)

def query_multi():
    q_pipeline = QueryPipeline()
    query_text = 'Abusive hospital staff, physically abusing patients, abusive family members'
    datasets = (early_onset['embedding_path'], dementia_or_other['embedding_path'])
    results = q_pipeline.multi_query(
        query_text,
        *datasets,
        top_n=50,
        top_k=10
    )
    q_pipeline.display_result(results)

def main():
    query_multi()

if __name__ == '__main__':
    main()
    quit()