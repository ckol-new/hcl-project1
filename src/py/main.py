import pathlib
import py.tests.TestCrawl as tc


base = r'C:\Users\wslam\Everything\health_city_lab\project1\hcl-project\src\data'
path = pathlib.Path(base)
early_onset = {
    'url_base': 'https://alzconnected.org/categories/i-have-younger-onset-alzheimers',
    'num_pages': 10,
    'seed_path': path / 'Seeds_Output' / 'ALZConnected' / 'test.txt',
    'crawl_path': path / 'Crawl_Output' / 'ALZConnected' / 'test.txt'
}



def main():
    tc.test_crawl(
        url_base= early_onset['url_base'],
        num_pages= early_onset['num_pages'],
        seed_path=early_onset['seed_path'],
        crawl_path=early_onset['crawl_path'],
        limit = 5
    )
    pass



if __name__ == '__main__':
    main()
    quit()