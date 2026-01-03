from abc import ABC, abstractmethod


class ScrapingPipeline(ABC):
    # ABSTRACT METHODS
    # generate 'seeds', or pages containing discussion posts
    @abstractmethod
    def generate_seeds(self, url_base: str, num_pages: int, limit: int = None) -> list[str]:
        pass

    # return list of forum post links from a given page
    @abstractmethod
    def crawl_page(self, page_url) -> list[str]:
        pass

    # generate crawl results: links to all discussion posts
    @abstractmethod
    def generate_crawl_result(self, seed_path: str) -> list[str]:
        pass

    # scrape a page for data
    @abstractmethod
    def scrape_page(self):
        pass

    @abstractmethod
    def scrape(self):
        pass

    # COMMON METHODS
    def save_seeds(self, seed_path: str, seeds: list[str]):
        with open(seed_path, 'w') as f:
            for seed in seeds:
                f.write(seed)
                f.write('\n')

    def save_crawl_results(self, crawl_path: str, crawl_results: list[str]):
        with open(crawl_path, 'w') as f:
            for crawl_result in crawl_results:
                f.write(crawl_result)
                f.write('\n')
