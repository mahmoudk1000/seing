
import requests
from bs4 import BeautifulSoup
import numpy as np

class PageRank:

    def __init__(self, urls=[]):
        self.urls = urls


    def page_rank(self, damping_factor=0.85, max_iterations=100, epsilon=1e-6):
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
        page_ranks = {}
        for i, url in enumerate(self.urls):
            page_ranks[url] = pi[i]
        return page_ranks
