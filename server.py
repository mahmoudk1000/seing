from agyptinzer import Agyptinzer
from rank import PageRank
from models import db, Seing
from sqlalchemy import create_engine
from sqlalchemy.orm import query, sessionmaker
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
# from googlesearch import search

engine = create_engine('sqlite:///seing.db')
Session = sessionmaker(bind=engine)
session = Session()

class Server:

    def __init__(self):
        self.agyptinzer_instance = Agyptinzer()
        self.page_rank_instance = PageRank()

    
    def data_list_handler(self, urls_list=[]):
        if urls_list:
            filterd_list = self.filter_urls(urls_list)
            print(filterd_list)
            domain_generator = self.agyptinzer_instance.is_egyptian(filterd_list)
            print(domain_generator)
            if domain_generator:
                ranked_domains = self.page_rank_instance.page_rank(domain_generator)
                self.add_and_commit(ranked_domains)
                return ranked_domains
            else:
                return []
        else:
            return []


    def data_query_hanlder(self, query=''):
        if query:
            google_results = self.google_search(query)
            filterd_list = self.filter_urls(google_results)
            domain_generator = self.agyptinzer_instance.is_egyptian(filterd_list)
            if domain_generator:
                ranked_domains = self.page_rank_instance.page_rank(domain_generator)
                self.add_and_commit(ranked_domains)
                return ranked_domains
            else:
                return []
        else:
            return []


    # def google_search_alt(self, query):
    #     results = search(query, num_results=10)
    #     return results


    def google_search(self, query):
        url = f"https://www.google.com/search?q={query}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        google_search_results = []
        for result in soup.find_all("div", class_="g"):
            link = result.find("a")["href"]
            google_search_results.append(link)

        return google_search_results


    def add_and_commit(self, db_records):
        for item in db_records:
            instance = session.query(Seing).filter_by(site=item['site']).first()
            if instance:
                continue
            domain = Seing(**item)
            session.add(domain)
        session.commit()
        return True


    def is_url(self, item):
        try:
            result = urlparse(item)
            return all([result.scheme, result.netloc])
        except:
            return None


    def filter_urls(self, url_list):
        return [item for item in url_list if self.is_url(item)]
