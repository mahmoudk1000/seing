from models import Seing
from fuzzywuzzy import fuzz, process
from elasticsearch import Elasticsearch
import requests
from googleapiclient.discovery import build
from bs4 import BeautifulSoup, ResultSet
import json
from agyptinzer import Agyptinzer, re
from helpers import Helpers
from backgroud import Background
import threading
import time


es = Elasticsearch()

class Search:

    def __init__(self, query):
        self.query = query
        self.agyptinzer_instance = Agyptinzer()
        self.google_results = []
        self.bing_results = []


    def net_search(self):
        self.run_engines()
        net_results = self.google_results + self.bing_results
        results = self.remove_duplicates(net_results)
        # filterd_domains = self.agyptinzer_instance.check_egypt(results)
        # helpers = Helpers(filterd_domains)
        # results_list = helpers.urls_list_filler()
        background = Background(net_results)
        background.run_background_commiter()
        return results


    def run_engines(self):
        t1 = threading.Thread(target=self.googling)
        t2 = threading.Thread(target=self.bing)
        t1.start()
        t2.start()
        t1.join(timeout=10)
        t2.join(timeout=10)


    def googling(self):
        API_KEY = ''
        CSE_ID = ''
        service = build("customsearch", "v1", developerKey=API_KEY)
        res = service.cse().list(q=self.query, cx=CSE_ID).execute()
        for item in res['items']:
            if self.agyptinzer_instance.check_egypt(item['link']):
                result = {}
                result['site'] = item['title']
                result['url'] = item['link']
                result['score'] = 0
                result['desc'] = item['snippet']
                self.google_results.append(result)
            else:
                pass


    def bing(self):
        subscription_key = ''
        endpoint = 'https://api.bing.microsoft.com/v7.0/search'
        headers = {'Ocp-Apim-Subscription-Key': subscription_key}
        params = {'q': self.query} #, 'mkt': 'en-AR'}
        try:
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            data = json.loads(response.text)
            for result in data["webPages"]["value"]:
                if self.agyptinzer_instance.check_egypt(result['url']):
                    site = result["name"]
                    url = result["url"]
                    result['score'] = 0
                    desc = result["snippet"]
                    self.bing_results.append({"site": site, "url": url, "desc": desc})
        except Exception as ex:
            raise ex


    def search_duckduckgo(self):
        url = f'https://api.duckduckgo.com/?q={self.query}&format=json'
        response = requests.get(url)
        links = [result['url'] for result in response.json()['Results']]
        return links


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
        ranked_matches = sorted(matches, key=lambda x: getattr(x, sort_col))
        return ranked_matches


    def top_fuzzed(self):
        values = Seing.query.all()
        results = []
        for value in values:
            score = fuzz.token_sort_ratio(self.query, value.site)
            results.append((value, score))
        
        results = sorted(results, key=lambda x: x[1], reverse=True)[:10]
        results = sorted(results, key=lambda x: x[0].score)
        return [r[0] for r in results]


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


    def remove_duplicates(self, lst, key="url"):
        seen = set()
        unique_lst = []
        for d in lst:
            if d[key] not in seen:
                seen.add(d[key])
                unique_lst.append(d)
        return unique_lst
