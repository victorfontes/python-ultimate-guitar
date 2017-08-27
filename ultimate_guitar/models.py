#coding: utf-8
#from constants import ADVERTISING_TYPES
from utils import find_tag_and_class, parse_text_from_tag
from bs4 import BeautifulSoup




class UGTypes:
    """
    Helper to handle Ultimate Guitar's result types. 
    The value of a type is a tuple with html class and querystring param value

    Valid Types are:
        - guitar_pro
        - video
        - bass
        - tab
        - chords
        - drums
        - ukulele
        - power
    
    """
    class UGType(object):
        def __init__(self, name, code, ug_id):
            self.name = name
            self.code = code 
            self.ug_id = ug_id
    
    tab = UGType('tab', 'TAB', 200)
    ukulele =  UGType('ukulele', 'UKU', 800)
    video = UGType('video','VID', 100)
    chords = UGType('chords','CRD', 300)
    bass =  UGType('bass','BASS', 400)
    guitar_pro = UGType('guitar_pro','PRO', 500)
    power =  UGType('power','PWR', 600)
    drums = UGType('drums','DRM', 700)
    

    ADVERTISING_TYPES = ('TAB PRO', 'CRD PRO')
    
    @classmethod
    def get(cls, name):
        return getattr(cls, name, None)
    

class SearchResult(dict):
    def __init__(self, **kwargs):
        dict.__init__(self)
        self['title'] = kwargs.get('title', '')
        self['link'] = kwargs.get('link', '')
        self['artist_name'] = kwargs.get('artist_name', '')
        self['artist_link'] = kwargs.get('artist_link', '')
        self['result_type'] = kwargs.get('result_type', '') 
        self['rating'] = kwargs.get('rating', 0)

    def __getattr__(self, attr):
        try:
            return self.__getitem__(attr)
        except:
            return self.__getattribute__(attr)

    @classmethod
    def parse(cls, article_soup):
        data = dict()

        song_tag = article_soup.findAll('a')[0]
        data['title'] = parse_text_from_tag(song_tag)
        data['link'] = song_tag.get('href')

        artist_tag = article_soup.findAll('a')[1]       
        data['artist_name'] = parse_text_from_tag(artist_tag)
        data['artist_link'] = artist_tag.get('href')

        type_tag = find_tag_and_class(article_soup, 'div', 'ugm-list--type')
        data['result_type'] = parse_text_from_tag(type_tag)

        rating_tag = find_tag_and_class(article_soup, 'span', 'ig-list--rating')
        data['rating'] = int(parse_text_from_tag(rating_tag, '-1'))

        return SearchResult(**data)


class ResultSet(object):
    """ 
        The results that are ads are always removed
    """
    def __init__(self, query, results_found, results_list, pagination):
        self.query = query
        self.results_found = results_found
        self.results = results_list
        self.pagination = pagination

    def __len__(self):
        return len(self.results)

    def __repr__(self):
        return "<%s: %s returned %d results>" % (self.__class__.__name__, self.query, len(self.results))
    
    @classmethod
    def parse(cls, query, response_content):
        #TODO: tirar daqui
        soup = BeautifulSoup(response_content, 'html.parser')
        
        stats_tag = find_tag_and_class(soup, 'p', 'ugm-tab-stats')
        results_found = int(list(stats_tag.children)[1].text)

        articles = soup.findAll('article', attrs={'class':'ugm-list--link'})
        
        pagination = find_tag_and_class(soup, 'ul', 'pagination')
        has_pagination = bool(pagination)


        results = map(SearchResult.parse, articles)
        results = filter(lambda x: x.result_type not in UGTypes.ADVERTISING_TYPES, results)
        results = sorted(results, key=lambda x: x.rating, reverse=True)

        return cls(query, results_found, results, pagination)