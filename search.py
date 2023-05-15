from models import Seing
from fuzzywuzzy import fuzz, process
from elasticsearch import Elasticsearch
import requests
from bs4 import BeautifulSoup, ResultSet
from agyptinzer import Agyptinzer, re
from helpers import Helpers
from backgroud import Background

es = Elasticsearch()

class Search:

    def __init__(self, query):
        self.query = query
        self.agyptinzer_instance = Agyptinzer()


    def web_search(self):
        duckduckgo_results = self.duckduckgo_search()
        results = duckduckgo_results
        filterd_domains = self.agyptinzer_instance.check_egypt(results)
        helpers = Helpers(filterd_domains)
        results_list = helpers.urls_list_filler()
        background = Background(results_list)
        background.run_background_commiter()
        return results_list


    def google_search(self):
        url = f"https://www.google.com/search?q={self.query}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        results = []
        for g in soup.find_all('div', class_='r'):
            anchors = g.find_all('a')
            if anchors:
                title = anchors[0].text
                link = anchors[0]['href']
                description = g.find('span', class_='st').text
                result = {'title': title, 'link': link, 'description': description}
                results.append(result)
        return results


    def duckduckgo_search(self):
        url = f"https://duckduckgo.com/html/?q={self.query}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        results = []
        for result in soup.find_all('div', class_='result'):
            # title = result.find('a', class_='result__url__headline').text
            link = result.find('a', class_='result__url')['href']
            # description = result.find('a', class_='result__snippet').text
            # result = {'site': title, 'url': link, 'desc': description}
            results.append(link)
        return results


    def you_search(self):
        url = f"https://www.yousearchengine.com/search?q={self.query}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        results = []
        for i in range(20):
            result = soup.find_all('div', class_='result')[i]
            title = result.find('a').text
            link = result.find('a')['href']
            snippet = result.find('p').text
            results.append({'title': title, 'link': link, 'snippet': snippet})
        return results


    def search_db(self):
        results = Seing.query
        results = results.filter(Seing.site.ilike('%' + self.query + '%'))
        results_list = results.order_by(Seing.site).all()
        return results_list


    def fuzz_db(self, sort_col="score"):
        results = Seing.query.all()
        matches = []
        for result in results:
            ratio = fuzz.token_sort_ratio(self.query, result.site)
            if ratio >= 35:
                matches.append(result)
        if len(matches) <= 2:
            results = self.search_db()
            return results
        ranked_matches = sorted(matches, key=lambda x: getattr(x, sort_col))
        return ranked_matches


    def index_model(self):
        for obj in Seing.query.all():
            es.index(index='my_index', doc_type='my_type', body={
                'site': obj.site,
                'url': obj.url,
                'score': obj.score,
                'description': obj.desc,
            })


    def es_search(self):
        self.index_model()
        body = {
            'query': {
                'multi_match': {
                    'query': self.query,
                    'fields': ['site', 'description', 'url'],
                }
            },
            "sort": {
                "score": {"order": "desc"}
            }
        }
        results = es.search(index='my_index', body=body)
        hits = results['hits']['hits']
        return hits


    def fetch_suggestions(self):
        choices = Seing.query.all()
        suggestions = process.extractBests(self.query, [choice.site for choice in choices], scorer=fuzz.token_sort_ratio,  
      limit=10)
        return [suggestion[0] for suggestion in suggestions]
