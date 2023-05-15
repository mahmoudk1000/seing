import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import tldextract
import numpy as np
from models import Seing
import re

class Helpers:

    def __init__(self, urls=[]):
        self.urls = urls


    def page_rank(self, damping_factor=0.85, max_iterations=100, epsilon=1e-6):
        '''
        Return dict of URLs with score. But dict is init with all four database model.
        '''
        # Construct the index mapping for the URLs
        index_map = {}
        for i, url in enumerate(self.urls):
            index_map[url] = i

        # Construct the adjacency matrix
        n = len(self.urls)
        adjacency_matrix = np.zeros((n, n))
        for i in range(n):
            try:
                html = requests.get(self.urls[i]).content
                soup = BeautifulSoup(html, 'html.parser')
                links = soup.find_all('a')
                for link in links:
                    href = link.get('href')
                    if href in index_map:
                        j = index_map[href]
                        adjacency_matrix[j, i] = 1    # Reverse the direction of the link
            except:
                pass

        # Construct the transition probability matrix
        P = np.zeros((n, n))
        for i in range(n):
            outgoing_links = np.where(adjacency_matrix[i] != 0)[0]
            if len(outgoing_links) > 0:
                P[i, outgoing_links] = 1 / len(outgoing_links)
            else:
                P[i, :] = 1 / n    # Handle dead ends

        # Initialize the PageRank scores
        pi = np.ones(n) / n

        # Run the PageRank algorithm
        for i in range(max_iterations):
            prev_pi = pi.copy()
            pi = (1 - damping_factor) / n + damping_factor * np.dot(P.T, pi)

            # Check for convergence
            if np.linalg.norm(pi - prev_pi) < epsilon:
                break

        # Return the PageRank scores as a dictionary of URL: score pairs
        page_ranks = []
        keys = ['site', 'url', 'score', 'desc']
        for i, url in enumerate(self.urls):
            values = [self.get_title_from_url(url), url, pi[i], self.get_url_description(url)]
            my_dict = dict(zip(keys, values))
            page_ranks.append(my_dict)
        return page_ranks


    def dicts_to_records(self, dicts):
        records = []
        for item in dicts:
            record = Seing(**item)
            records.append(record)
        return records


    def urls_list_filler(self):
        '''
        Prepare a list of URLs to the standard form of SEING.
        '''
        keys = ['site', 'url', 'score', 'desc']
        filled_list = []
        for url in self.urls:
            values = [self.get_title_from_url(url), url, -1, self.get_url_description(url)]
            my_dict = dict(zip(keys, values))
            filled_list.append(my_dict)
        return filled_list
    

    def get_title_from_url(self, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string.strip()
            clean_title = re.sub(r'[^\w\s]', '', title).strip()
            return clean_title
        except:
            netloc = urlparse(url).netloc
            extracted = tldextract.extract(netloc)
            sld = '.'.join([extracted.domain]).rstrip('.').capitalize()
            return sld


    def get_url_description(self, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            description_tag = soup.find('meta', attrs={'name': 'description'})
            if description_tag:
                description = description_tag.get('content')
            else:
                return ''
        except:
            return ''
        return description
