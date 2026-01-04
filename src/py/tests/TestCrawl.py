from py.model.ScrapingPipeline import ALZConnectedScrapingPipeline


# test crawling

def test_crawl(url_base: str, seed_path: str, num_pages: int, crawl_path: str, start: int = 2, limit: int = None):
    pipeline = ALZConnectedScrapingPipeline()

    print("GENERATING SEEDS")
    seeds = pipeline.generate_seeds(url_base=url_base, num_pages=num_pages, start=start, limit=limit)
    pipeline.save_seeds(seed_path, seeds)

    print('CRAWLING')
    crawl_result = pipeline.generate_crawl_result(seed_path, limit)
    pipeline.save_crawl_results(crawl_path, crawl_result)