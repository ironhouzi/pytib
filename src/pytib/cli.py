import click
import logging
import os
import sys
import webbrowser
import json

from pathlib import Path

import pytib
from pytib.exceptions import InvalidConfig


log_level = logging.DEBUG if os.getenv('DEBUG') in ('1', 'on') else logging.INFO
logger = logging.getLogger('pytib')
logger.setLevel(log_level)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


@click.command()
@click.option('--input-file', '-i', help='Specify file to read',
              type=click.File('r'), nargs=1, default='-')
@click.option('--config', '-c', help='Config JSON file path',
              type=click.File('r'), nargs=1, envvar='PYTIB_CONFIG')
@click.option('--preserve-input', '-p', is_flag=True,
              help='Preserve wylie in Unicode output')
@click.option('--unicode-points', '-u', is_flag=True,
              help='Print Unicode values')
@click.option('--html', help='Output as basic HTML document', is_flag=True)
@click.argument('wylie', required=False)
def ptib(input_file, wylie, preserve_input, unicode_points, html, config):
    """
    WYLIE can be either a string literal or a file.
    The file can be read from STDIN, or from a filepath using the -i parameter.
    """

    if wylie:
        content = wylie
    else:
        content = input_file.read()
        input_file.close()

    if config:
        try:
            cfg = json.load(config)
        except ValueError:
            raise InvalidConfig('Invalid JSON config file!', 'JSON decoding')
        finally:
            config.close()
    else:
        cfg = {}

    tables = pytib.tables.generate_tables(cfg)

    if unicode_points:
        content = content.split('\n')
        result = tuple(
            f'U+{ord(char):04X}'
            for line in content for word in line.split()
            for char in pytib.parse(word, tables)
        )
    else:
        result = ''.join(pytib.read(content, tables)).rstrip()

    if preserve_input:
        print(content)

    if html:
        cwd = Path(__file__).absolute().parent
        web_dir = cwd / '.web_tmp/'
        web_dir.mkdir(exist_ok=True)
        index_html = web_dir / 'index.html'

        with open(index_html, 'w') as f:
            f.write(to_web(result))

        webbrowser.open_new_tab(index_html.as_uri())
    else:
        print(result)


def to_web(result):
    tibetan = result.replace('\n\n', '</p><p>').replace('\n', '</br>')
    tibetan = f'<p>{tibetan}</p>'
    return f'''<!DOCTYPE html>
    <html>
      <head>
        <title>PyTib</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <style type="text/css">
            .tibetan {{
                font-family: Noto Sans Tibetan, Noto Sans Regular;
                font-size: 48px;
            }}
        </style>
      </head>
      <body>
      <div class="tibetan">{tibetan}</div>
      </body>
    </html>
    '''


if __name__ == '__main__':
    try:
        ptib()
    except InvalidConfig as e:
        print(f'Error in {e.config_item}! ({e.msg})')
        sys.exit(1)
