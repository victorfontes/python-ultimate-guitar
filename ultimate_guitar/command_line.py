import click

from . import UltimateGuitarScraper
from tabulate import tabulate
import utils

@click.group()
def cli():
    pass

from collections import OrderedDict
def filter_dict(d, keys):
    d = OrderedDict(d)
    _d = OrderedDict()
    for key in keys:
        _d[key] = d[key]
    return _d



@cli.command('search')
@click.option('--query', '-q', prompt='Your search query', help='The person to greet.')
@click.option('-t', '--filter-type', default=None, help='Filter results by type')
@click.option('--limit', '-l', default=5, help='Limit first N results')
@click.option('--path', '-p', default='', help='Path to downloaded files')
@click.option('--download/--no-download', default=False)
def search(query, filter_type, download, limit, path):
    filter_msg = ""
    if filter_type is not None:
        filter_msg = "using filter %s" % filter_type

    ug = UltimateGuitarScraper()
    rs = ug.search('paranoid android', filter_type=filter_type)

    header_message = "\nFound %d results for %s %s " % (len(rs), rs.query, filter_msg) 

    
    click.echo(click.style(header_message, bold=True, fg='white'))
    click.echo()


    TABLE_KEYS = ('rating', 'artist_name', 'title', 'result_type', 'link')
    table_results = map(lambda x: filter_dict(x, TABLE_KEYS), rs.results[:limit])

    print tabulate(table_results, headers='keys', tablefmt="grid")
    
    
    
    if download:
        utils.make_shure_path_exists(path)
        with click.progressbar(rs.results[:limit], label='Downloading guitar pro files', length=limit) as progress_list:
            for result in progress_list:
                if result.result_type == 'TAB':
                    ug.download_tab(result.link, path=path)
                elif result.result_type == 'PRO':
                    ug.download_guitar_pro(result.link, path=path)

    
    click.echo('Done!')


@cli.command('hello2')
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello2(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo('Hello %s!' % name)


#cli = click.CommandCollection(sources=[cli_goals, cli_entries])
