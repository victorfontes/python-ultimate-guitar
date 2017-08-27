from bs4 import BeautifulSoup


""" UI """
def parse_text_from_tag(tag, default=None):
    if tag is None:
        return default
    return tag.getText().replace('\n','').replace(u'\xa0', '').strip()


def find_tag_and_class(el, tag, class_name, first=True):
    results = el.findAll(tag, attrs={'class': class_name})
    
    if len(results) == 0:
        return None if first else list()
    
    return results[0] if first else results


def get_soup(obj):
	#if isinstance(obj, str, unicode):
	#	return BeautifulSoup(obj, 'html.parses')
	txt = getattr(obj, 'content', obj)
	return BeautifulSoup(txt, 'html.parser')



""" CLI """
import os
def make_shure_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
