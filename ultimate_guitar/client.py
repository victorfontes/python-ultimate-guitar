#coding: utf-8
import requests
from bs4 import BeautifulSoup

from models import ResultSet, SearchResult, UGTypes
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from utils import get_soup
from constants import USER_AGENT



class UltimateGuitarScraper(object):
    """ 
    This is the client class and it doesnt hold any state
    
    """
    def __init__(self):
        self._search_url = 'https://www.ultimate-guitar.com/search.php'
        self._headers = {'User-Agent': USER_AGENT }
        
    def _search(self, params={}):
        response = requests.get(self._search_url, headers=self._headers, params=params)
        return response


    def search(self, query, filter_type=None, fetch_all=False):
        """ This function does the same as using the site search bar 
        
        Args:
           query (str):  The text you want to search, it can be the artist, 
           album, song or any combination of that

        Kwargs:
           filter_type (str): Filter results by type, valid options are:
                - guitar_pro
                - video
                - bass
                - tab
                - chords
                - drums
                - ukulele
                - power

           fetch_all (bool): If the search returns multiple pages, will fetch all before 
            any result is returned

        Returns:
           :class:`ultimate_guitar.ResultSet`: a result object with the results, see :class:`ultimate_guitar.ResultSet`.



        Raises:
           AttributeError, KeyError

        Usage:
            >>> client = UltimateGuitarScraper()
            >>> client.search('paranoid android')
            <ResultSet: paranoid android returned 28 results>

            >>> client.search('paranoid android', filter_type='guitar_pro')
            <ResultSet: paranoid android returned 9 results>
        
        """

        if fetch_all:
            raise NotImplemented()

        payload = {'search_type': 'title', 'value': query}
        
        if filter_type:
            payload['type'] = UGTypes.get(filter_type).code

        response = self._search(params=payload) 
        open(query, 'wb').write(response.content)
        result_set = ResultSet.parse(query, response.content)
        return result_set 

    def _get_file_name(self, url, extension, path=''):
        name = url.split('/')[-1].split('.')[0]
        return name + extension

    
    def _save_file(self, content, url, extension, path='', encode=None):
        fname = self._get_file_name(url, extension, path)
        with open(path+fname, 'wb') as f:
            if encode:
                content = content.encode(encode)
            f.write(content)

    def download_guitar_pro(self, url, path=''):
        r1 = requests.get(url)
        soup = get_soup(r1)
        
        frm = soup.find('form', attrs=dict(name='tab_download'))
        action = frm.get('action')

        payload = {
            'id': frm.find(attrs=dict(name='id')).get('value'),
            'session_id': frm.find(attrs=dict(name='session_id')).get('value')
        }

        r2 = requests.post(action, payload)

        
        self._save_file(r2.content, url, '.gp4', path=path)
        

    def download_tab(self, url, path=''):
        r1 = requests.get(url, headers=self._headers)
        soup = get_soup(r1)

        text = soup.find('pre').text
        self._save_file(text, url, '.txt', path=path, encode='utf-8')


    def download(self, result, path=''):
        if result.result_type == UGTypes.tab.code:
            self.download_tab(result.link, path=path)
        if result.result_type == UGTypes.guitar_pro.code:
            self.download_guitar_pro(reuslt.link, path=path)
