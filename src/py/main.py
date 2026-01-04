import pathlib

import requests
from bs4 import BeautifulSoup

import py.tests.TestCrawl as tc
import py.tests.TestScrape as ts
from py.model.ScrapingPipeline import ALZConnectedScrapingPipeline
from py.model.EmbeddingPipeline import EmbeddingPipeline

base = r'C:\Users\wslam\Everything\health_city_lab\project1\hcl-project\src\data'
path = pathlib.Path(base)
early_onset = {
    'url_base': 'https://alzconnected.org/categories/i-have-younger-onset-alzheimers',
    'num_pages': 10,
    'seed_path': path / 'Seeds_Output' / 'ALZConnected' / 'test.txt',
    'crawl_path': path / 'Crawl_Output' / 'ALZConnected' / 'test.txt',
    'scrape_path': path / 'Scrape_Output' / 'ALZConnected' / 'test.txt'
}

def testing():
    url = 'https://alzconnected.org/discussion/comment/260911#Comment_260911?utm_source=community-search&utm_medium=organic-search&utm_term=Working'
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    div_discussion = soup.find('div', class_='Discussion')
    div_content = soup.find('div', class_='Message userContent')
    arr = div_content.find_all('p')
    for p in arr:
        if p.string: print(p.string)
        else: print(p.get_text(separator='\n'))

def main():
    '''
    pipeline = ALZConnectedScrapingPipeline()
    pipeline.run_pipeline(
        url_base=early_onset['url_base'],
        seed_path=early_onset['seed_path'],
        seed_num=early_onset['num_pages'],
        crawl_path=early_onset['crawl_path'],
        scrape_path=early_onset['scrape_path']
    )
    '''

    # test embedding


if __name__ == '__main__':
    main()
    quit()