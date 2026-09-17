"""
Utilities to work with html
"""

from bs4 import BeautifulSoup

def cleanse(html:str) -> str:
    """Cleanse the Canvas HTML strings of script and link tags.

    Parameters
    ----------
    html : str
        The HTML string from Canvas

    Returns
    -------
    str
        The cleansed version of the HTML string
    """
    soup = BeautifulSoup(html, 'html.parser')

    for tag in soup.find_all('link') + soup.find_all('script'):
        tag.decompose()

    return str(soup)


def deTeX(html:str) -> str:
    soup = BeautifulSoup(html, 'html.parser')

    for tag in soup.find_all('img', class_="equation_image"):
        tex = tag.get('alt')[7:]
        tag.replace_with(f'${tex}$')

    return str(soup)
