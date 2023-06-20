import requests
import tldextract
from bs4 import BeautifulSoup
from tld import get_tld
from urllib.parse import urlparse
import geoip2.database
import socket
import re
from urllib.request import urlopen
from json import load

GEOIP_DB_PATH = './GeoLite2-Country.mmdb'

class Agyptinzer:

    def __init__(self, iterations=2):
        self.egypt_domains = []
        self.all_egypt_domains =[]
        self.iterations = iterations


    def check_egypt(self, url):
        """
        Return a list of only egypain domains, by running filter lavels.
        """
        url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
        if url_pattern.match(str(url)):
            ext = tldextract.extract(url)
            if ext.suffix in ['eg', 'com.eg', 'edu.eg', 'gov.eg', 'net.eg', 'org.eg', 'egypt']:
                return url
            else:
                parsed_url = urlparse(url)
                if 'egypt' in parsed_url.netloc or 'egy' in parsed_url.netloc or 'masr' in parsed_url.netloc or 'misr' in parsed_url.netloc:
                    return url
                elif parsed_url.netloc.endswith('.eg'):
                    return url
                else:
                    try:
                        response = requests.head(url)
                        if response.status_code == 200 and 'eg' in response.headers.get('Server', ''):
                            return urlparse(url)
                        else:
                            try:
                                ip_address = socket.gethostbyname(url)
                                with geoip2.database.Reader(GEOIP_DB_PATH) as reader:
                                    response = reader.country(ip_address)
                                    if response.country.iso_code == 'EG':
                                        return url
                                    else:
                                        ip_address = socket.gethostbyname(url)
                                        url_lookup = 'https://ipinfo.io/' + ip_address + '/json'
                                        response = urlopen(url_lookup)
                                        data = load(response)
                                        if data['country'] == "EG":
                                            return url
                                        else:
                                            pass
                            except:
                                pass
                    except:
                        pass
        else:
            pass



    def is_egyptian(self, url_list):
        """
        Returns Egyptian domains if the domain name of the given URL belongs to an Egyptian TLD, False otherwise.
        """
        if self.iterations == 0:
            return self.egypt_domains
        for url in url_list:
            url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
            if url_pattern.match(str(url)):
                ext = tldextract.extract(url)
                if ext.suffix in ['eg', 'com.eg', 'edu.eg', 'gov.eg', 'net.eg', 'org.eg']:
                    self.egypt_domains.append(url)
                else:
                    parsed_url = urlparse(url)
                    if 'egypt' in parsed_url.netloc or 'egy' in parsed_url.netloc or 'masr' in parsed_url.netloc:
                        self.egypt_domains.append(url)
                    elif parsed_url.netloc.endswith('.eg') or 'eg' in parsed_url.netloc.split('.'):
                        self.egypt_domains.append(url)
                    else:
                        self.is_hosted_in_egypt(url)
            else:
                pass
        self.collector(url_list=self.egypt_domains)
        self.iterations -= 1
        
        return self.is_egyptian(url_list=self.all_egypt_domains)


    def is_hosted_in_egypt(self, url):
        """
        Returns Egyptian domains if the given URL is hosted in Egypt.
        """
        try:
            response = requests.head(url)
            if response.status_code == 200 and 'eg' in response.headers.get('Server', ''):
                self.egypt_domains.append(urlparse(url))
            else:
                try:
                    ip_address = socket.gethostbyname(url)
                    with geoip2.database.Reader(GEOIP_DB_PATH) as reader:
                        response = reader.country(ip_address)
                        if response.country.iso_code == 'EG':
                            self.egypt_domains.append(url)
                        else:
                            self.is_hosted_in_egypt_alt(url)
                except:
                    pass
        except:
            pass
        return self.egypt_domains


    def is_hosted_in_egypt_alt(self, url):
        ip_address = socket.gethostbyname(url)
        url_lookup = 'https://ipinfo.io/' + ip_address + '/json'
        response = urlopen(url_lookup)
        data = load(response)
        if data['country'] == "EG":
            self.egypt_domains.append(url)
        else:
            pass
        return self.egypt_domains

    
    def collector(self, url_list):
        """
        Collect all sub_domains of the given URL
        """
        url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
        for url in url_list:
            try:
                reqs = requests.get(url)
                soup = BeautifulSoup(reqs.text, 'html.parser')
                for link in soup.find_all('a'):
                    if url_pattern.match(str(link.get("href"))):
                        self.all_egypt_domains.append(link.get("href"))
            except:
                pass

        return self.all_egypt_domains
