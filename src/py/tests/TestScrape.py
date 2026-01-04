from py.model.ScrapingPipeline import ALZConnectedScrapingPipeline


# test crawling

def test_scrape(url_base: str, seed_path: str, num_pages: int, crawl_path: str, scrape_path: str, start: int = 2, seed_limit: int = None, crawl_limit: int = None):
    pipeline = ALZConnectedScrapingPipeline()

    scrape_data = pipeline.scrape(crawl_path)
    pipeline.save_scrape_results(scrape_path, scrape_data)

