try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Otodom.pl scraper',
    'author': 'TRogalski',
    'author_email': 'tomracc@yahoo.com',
    'version': '0.1',
    'install_requires': ['nose', 'bs4', 'requests'], # external dependencies (packages)
    'packages': ['otoScraper'],
    'scripts': [],
    'name': 'otoScraper'
}

setup(**config)
