import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504], allowed_methods=["GET"])
session.mount('https://', HTTPAdapter(max_retries=retries))
session.headers.update({'User-Agent': 'Mozilla/5.0'})

def parse_telegraph_article(url):
    try:
        res = session.get(url, timeout=10)
        res.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f'Ошибка при загрузке {url}: {e}')

    soup = BeautifulSoup(res.text, 'html.parser')
    content_div = soup.find('article')

    first_block = content_div.find(['strong', 'p', 'h1', 'h2'])
    title = first_block.text.strip() if first_block else 'Без названия'

    if first_block:
        first_block.decompose()
        
    for img in content_div.find_all('img'):
        img.decompose()
    return title, str(content_div)
