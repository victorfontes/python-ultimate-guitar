import pytest

def get_html_fixture(name):
	return open('tests/fixtures/%s.html' % name, 'rb').read()


@pytest.fixture
def resultset():
	from .context import ResultSet
	content = get_html_fixture('search-paranoid-android')
	return ResultSet.parse('paranoid android', content)


def test_resultset(resultset):
	assert len(resultset) == 28
	assert len(resultset) == len(resultset.results)
	assert resultset.query == 'paranoid android'
	assert str(resultset) == "<ResultSet: paranoid android returned 28 results>"

def test_result_behavior(resultset):
	first = resultset.results[0]
	assert first.rating == first['rating']


def test_result_content(resultset):
	results = resultset.results
	first = results[0]

	assert first.rating == 269
	assert first.artist_link == '/tabs/radiohead_tabs.htm'
	assert first.title == 'Paranoid Android (ver5)'
	assert first.artist_name == 'Radiohead'
	assert first.link == 'https://tabs.ultimate-guitar.com/r/radiohead/paranoid_android_ver5_tab.htm'
	assert first.result_type == 'TAB'


