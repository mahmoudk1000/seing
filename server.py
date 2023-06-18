from agyptinzer import Agyptinzer
from helpers import Helpers
from models import db, Seing
from urllib.parse import urlparse
from search import Search
from backgroud import Background

class Server:

    def __init__(self, query):
        self.query = query
        self.agyptinzer_instance = Agyptinzer()
        self.page_rank_instance = Helpers()
        self.search_instance = Search(query)

    
    def data_list_handler(self):
        urls_list = self.query.split(",")
        if urls_list:
            filterd_list = self.filter_urls(urls_list)
            domain_generator = self.agyptinzer_instance.is_egyptian(filterd_list)
            if domain_generator:
                print("Here!")
                print(domain_generator)
                ranked_domains = self.page_rank_instance.page_rank(domain_generator)
                background = Background(ranked_domains)
                background.add_and_commit()
                return ranked_domains
            else:
                return []
        else:
            return []


    def data_query_hanlder(self):
        if self.query:
            web_results = self.search_instance.net_search()
            if web_results:
                # filterd_list = self.agyptinzer_instance.check_egypt(web_results)
                # ranked_domains = self.page_rank_instance.page_rank(web_results)
                background = Background(web_results)
                background.add_and_commit()
                return web_results
            else:
                return []
        else:
            return []


    def is_url(self, item):
        try:
            result = urlparse(item)
            return all([result.scheme, result.netloc])
        except:
            return None


    def filter_urls(self, url_list):
        return [item for item in url_list if self.is_url(item)]
