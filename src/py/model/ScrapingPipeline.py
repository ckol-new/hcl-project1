from abc import ABC, abstractmethod
import json
import requests
import bs4
from bs4 import BeautifulSoup
from py.model.Author import Author
from py.model.Post import Post
from py.model.Comment import Comment


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

    @abstractmethod
    def scrape_title(self, soup):
        pass

    @abstractmethod
    def scrape_post_id(self, soup) -> int:
        pass

    @abstractmethod
    def scrape_post_content(self, soup: BeautifulSoup) -> list[str]:
        pass

    @abstractmethod
    def scrape_post_author(self, soup: BeautifulSoup) -> Author:
        pass

    @abstractmethod
    def scrape_post_date(self, soup: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def scrape_comment_content(self, soup: BeautifulSoup) -> list[str]:
        pass

    @abstractmethod
    def scrape_comment_author(self, soup: BeautifulSoup) -> Author:
        pass

    @abstractmethod
    def scrape_comment_date(self, soup: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def scrape_comments(self, soup) -> list[Comment]:
        pass


    # COMMON METHODS
    def request_page(self, url: str) -> str:
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        try:
            response = requests.get(url, headers=header)
            if response.status_code == 200:
                ...
            else: print("REQUEST FAILED: ", response.status_code)
        except requests.exceptions.RequestException as e:
            raise Exception(e)

        return response.text


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


    # scrape a page for data
    def scrape_page(self, url: str) -> Post or None:
        html = self.request_page(url)
        soup = BeautifulSoup(html, 'html.parser')
        title = self.scrape_title(soup)
        post_id = self.scrape_post_id(soup)
        date = self.scrape_post_date(soup)
        content = self.scrape_post_content(soup)
        author = self.scrape_post_author(soup)

        # scrape comments
        comments = self.scrape_comments(soup)

        # only return if all elements are not none
        if not title: return None
        if not post_id: return None
        if not date: return None
        if not content or len(content) == 0: return None
        if not comments or len(comments) == 0: return None

        post = Post(
            url=url,
            post_id=post_id,
            title=title,
            content=content,
            author=author,
            date=date,
            comments=comments
        )

        return post

    def scrape(self, crawl_path: str):
        length = 0
        scrape_results = []
        with open(crawl_path, 'r') as f:
            length = sum([1 for _ in f])
        with open(crawl_path, 'r') as f:
            n = 0
            for link in f:
                if n % 10 == 0:
                    print(f'%{(n / length) * 100}')

                # get post object
                post = self.scrape_page(link)
                scrape_results.append(post)

        return scrape_results

    def save_scrape_results(self, scrape_path: str, scrape_results: list[Post]):
        with open(scrape_path, 'w') as f:
            for post in scrape_results:
                # none check
                if post:
                    f.write(json.dumps(post.to_dict()))
                    f.write('\n')



class ALZConnectedScrapingPipeline(ScrapingPipeline, ABC):
    def __init__(self):
        pass

    def run_pipeline(self, url_base: str, seed_path: str, seed_num: int, crawl_path: str, scrape_path: str, seed_start: int = 2, seed_limit: int = None, crawl_limit: int = None):
        # generate seeds
        seeds = self.generate_seeds(url_base, seed_num, seed_start, seed_limit)
        self.save_seeds(seed_path, seeds)

        # crawl
        crawl_results = self.generate_crawl_result(seed_path, crawl_limit)
        self.save_crawl_results(crawl_path,  crawl_results)
        pass

    def generate_seeds(self, url_base: str, num_pages: int, start: int = 2, limit: int = None) -> list[str]:
        num = 0
        seeds = [url_base]
        for page in range(start, num_pages + 1):
            seed = url_base + '/p' + str(page)
            seeds.append(seed)

        return seeds

    def crawl_page(self, page_url) -> list[str] or None:
        html = self.request_page(page_url)
        if not html: return None

        soup = bs4.BeautifulSoup(html, 'html.parser')

        links = set()
        for link in soup.find_all('a'):
            href = link.get('href')

            if '/discussion/' in href:
                links.add(href)

        return list(links)

    def generate_crawl_result(self, seed_path: str, limit: int = None) -> list[str]:
        crawl_result = set()
        length = None
        with open(seed_path, 'r') as f:
            length = sum([1 for _ in f])
        with open(seed_path, 'r') as f:
            n = 0

            for seed in f:
                if limit:
                    if n >= limit:
                        break
                if n % 10 == 0:
                    print(f'%{(n / length) * 100}')
                n += 1

                page_results = self.crawl_page(seed)
                for page in page_results:
                    crawl_result.add(page)

        return list(crawl_result)


    def scrape_title(self, soup):
        pass

    def scrape_post_id(self, soup) -> int:
        pass

    def scrape_post_content(self, soup: BeautifulSoup) -> list[str]:
        pass

    def scrape_post_author(self, soup: BeautifulSoup) -> Author:
        pass

    def scrape_post_date(self, soup: BeautifulSoup) -> str:
        pass

    def scrape_comment_content(self, soup: BeautifulSoup) -> list[str]:
        pass

    def scrape_comment_author(self, soup: BeautifulSoup) -> Author:
        pass

    def scrape_comment_date(self, soup: BeautifulSoup) -> str:
        pass

    def scrape_comments(self, soup) -> list[Comment]:
        pass