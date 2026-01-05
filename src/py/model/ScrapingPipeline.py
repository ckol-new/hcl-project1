from abc import ABC, abstractmethod
from pathlib import Path
import re
import json
import requests
import unicodedata
import unidecode
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
    def scrape_title(self, soup: BeautifulSoup) -> str or None:
        pass

    @abstractmethod
    def scrape_post_id(self, url: str) -> str or None:
        pass

    @abstractmethod
    def scrape_post_content(self, soup: BeautifulSoup) -> list[str] or str or None:
        pass

    @abstractmethod
    def scrape_post_author(self, soup: BeautifulSoup) -> Author or None:
        pass

    @abstractmethod
    def scrape_post_date(self, soup: BeautifulSoup) -> str or None:
        pass

    @abstractmethod
    def scrape_comment_content(self, comment_div) -> list[str] or str or None:
        pass

    @abstractmethod
    def scrape_comment_author(self, comment_div) -> Author or None:
        pass

    @abstractmethod
    def scrape_comment_date(self, comment_div) -> str or None:
        pass

    @abstractmethod
    def scrape_comments(self, soup, url) -> list[Comment] or None:
        pass


    # COMMON METHODS
    # prepare for vectorization
    def clean_text(self, text: str) -> str or None:
        text = unidecode.unidecode(text)
        # strip of useless control characters
        text = ''.join(ch for ch in text if ch.isprintable())
        return text


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
        #TODO Remove newline character at the end of the url as it gets scraped.
        print(url)
        html = self.request_page(url)
        soup = BeautifulSoup(html, 'html.parser')
        title = self.scrape_title(soup)
        print(title)
        post_id = self.scrape_post_id(url)
        print(post_id)
        date = self.scrape_post_date(soup)
        print(date)
        content = self.scrape_post_content(soup)
        print(content)
        author = self.scrape_post_author(soup)
        print(author)

        # scrape comments
        comments = self.scrape_comments(soup=soup, url=url)

        # only return if all elements are not none
        if not title: return None
        if not post_id: return None
        if not date: return None
        if not content or len(content) == 0: return None
        if not comments or len(comments) == 0: return None
        print(title)

        post = Post(
            url=url,
            post_id=post_id,
            title=title,
            content=content,
            author=author,
            date=date,
            comments=comments
        )
        print(post)

        return post

    def scrape(self, crawl_path: str) -> list[Post]:
        length = 0
        scrape_results = []
        with open(crawl_path, 'r') as f:
            length = sum([1 for _ in f])
        with open(crawl_path, 'r') as f:
            n = 0
            for link in f:
                print(n)
                if n % 10 == 0:
                    print(f'%{(n / length) * 100}')
                n += 1

                # get post object
                post = self.scrape_page(link)
                if post:
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

    def run_pipeline(self, url_base: str, seed_path: str or Path, seed_num: int, crawl_path: str or Path, scrape_path: str, seed_start: int = 2, seed_limit: int = None, crawl_limit: int = None):
        # generate seeds
        seeds = self.generate_seeds(url_base, seed_num, seed_start, seed_limit)
        self.save_seeds(seed_path, seeds)

        # crawl
        crawl_results = self.generate_crawl_result(seed_path, crawl_limit)
        self.save_crawl_results(crawl_path,  crawl_results)

        # scrape
        scrape_results= self.scrape(crawl_path)
        self.save_scrape_results(scrape_path, scrape_results)


    def generate_seeds(self, url_base: str, num_pages: int, start: int = 2, limit: int = None) -> list[str]:
        num = 0
        seeds = [url_base]
        for page in range(start, num_pages + 1):
            if limit:
                if num >= limit: break
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


    def scrape_title(self, soup) -> str or None:
        title_text = soup.title.string
        title_text = title_text.removesuffix(' \u2014 ALZConnected')
        return title_text

    def scrape_post_id(self, url: str) -> str or None:
        if not url: return None
        if not isinstance(url, str):
            print("not string")
            return None
        sep = '/discussion/'
        _, _, id_string = url.partition(sep)
        post_id = id_string[0:5]
        return post_id

    def scrape_post_content(self, soup: BeautifulSoup) -> list[str] or str or None:
        content_p = []

        div_discussion = soup.find('div', class_='Discussion')
        if not div_discussion: return None
        div_content = div_discussion.find('div', class_='Message userContent')
        if not div_content: return None

        if div_content.find('p'):
            for paragraph in div_content.find_all('p'):
                content_p.append(paragraph.get_text(separator='\n'))
        else:
            content_p.append(div_content.get_text(separator='\n'))

        # split paragraph
        content = []
        for p in content_p:
            pattern = r'[\n\.\?\!]+'
            arr = re.split(pattern, p)
            for s in arr:
                if not s: continue
                if s.isspace(): continue
                s = s.strip()
                clean_s = self.clean_text(s)
                content.append(clean_s)

        return content

    def scrape_post_author(self, soup: BeautifulSoup) -> Author or None:
        author_div = soup.find('span', class_="Author")
        if not author_div: return None
        author_a = author_div.find('a')
        if not author_a: return None

        author_name = author_a.string
        author_id = author_a.get('data-userid')
        link = author_a.get('href')

        # get author obj
        author = Author(author_name, author_id, link)
        return author

    def scrape_post_date(self, soup: BeautifulSoup) -> str or None:
        div_discussion = soup.find('div', class_='Discussion')
        if not div_discussion: return None
        div_meta_discussion = div_discussion.find('div', class_='Meta DiscussionMeta')
        if not div_meta_discussion: return None
        time_div = div_meta_discussion.find('time')
        if not time_div: return None
        date = time_div.get('title')
        return date

    def scrape_comment_content(self, comment_div) -> list[str] or str or None:
        content_arr = []

        div_content = comment_div.find('div', class_='Message userContent')
        if not div_content: return None

        paragraphs = div_content.find_all('p')
        if len(paragraphs) == 0:
            content_arr.append(div_content.get_text(separator='\n'))

        for paragraph in paragraphs:
            content_arr.append(paragraph.get_text(separator='\n'))

        content = []
        for p in content_arr:
            pattern = r'[\n\.\?\!]+'
            arr = re.split(pattern, p)
            for s in arr:
                if not s: continue
                if s.isspace(): continue
                s = s.strip()
                clean_s = self.clean_text(s)
                content.append(clean_s)

        return content

    def scrape_comment_author(self, comment_div) -> Author or None:
        # get author data
        div_meta_comment = comment_div.find('div', class_='Meta CommentMeta CommentInfo')
        if not div_meta_comment: return None
        time_div = div_meta_comment.find('time')
        if not time_div: return None
        date = time_div.get('title')
        author_name = comment_div.find('a', class_='Username js-userCard').string
        author_id = comment_div.find('a', class_='Username js-userCard').get('data-userid')
        link = comment_div.find('a', class_='Username js-userCard').get('href')

        # get author obj
        author = Author(author_name, author_id, link)
        return author

    def scrape_comment_date(self, comment_div) -> str:
        time_div = comment_div.find('time')
        return time_div.get('title')

    def scrape_comments(self, soup: BeautifulSoup, url: str) -> list[Comment]:
        comments = []
        for comment_div in soup.find_all('div', class_='Comment'):
            # get comment
            content = self.scrape_comment_content(comment_div)
            author = self.scrape_comment_author(comment_div)
            date = self.scrape_comment_date(comment_div)
            post_id = self.scrape_post_id(url)
            if content and author and date and post_id:
                comment = Comment(url, post_id, date, author, content)
                comments.append(comment)

        return comments