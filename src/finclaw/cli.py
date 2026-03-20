import logging
import os

import typer

from .social import trump_utils
from .finance import yfinance_utils

log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

app = typer.Typer(help='Finclaw', context_settings={'help_option_names': {'-h', '--help'}})
app.add_typer(trump_utils.app, name='trump')
app.add_typer(yfinance_utils.app, name='yfinance')


if __name__ == '__main__':
    app()
