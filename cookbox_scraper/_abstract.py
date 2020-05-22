import requests

from bs4 import BeautifulSoup
from extruct import extract

from cookbox_scraper._utils import on_exception_return

# some sites close their content for 'bots', so user-agent must be supplied
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
}

# set some cookies to maneuver over:
# - EU Consent in allrecipes.com.br
COOKIES = {
    'euConsentFailed': 'true',
    'euConsentID': 'e48da782-e1d1-0931-8796-d75863cdfa15',
}

class WebsiteNotImplementedError(NotImplementedError):
    '''Error for when the website is not supported by this library.'''
    pass

class BaseScraper():
    def url(self):
        NotImplementedError("This should be implemented.")

    def host(self):
        """
        Get the host of the url, so we can use the correct scraper
        """
        raise NotImplementedError("This should be implemented.")

    def title(self):
        raise NotImplementedError("This should be implemented.")

    def description(self):
        raise NotImplementedError("This should be implemented.")

    def time_unit(self):
        return 'min'

    def time(self):
        """
        (total_time, prep_time, cook_time) it takes to prepare the recipe in minutes
        """
        raise NotImplementedError("This should be implemented.")
    
    def yield_unit(self):
        raise NotImplementedError("This should be implemented.")
    
    def yields(self):
        ''' (total yield, serving size) '''
        raise NotImplementedError("This should be implemented.")

    def ingredients(self):
        ''' [ ('Group name', [ingredients]) ] '''
        raise NotImplementedError("This should be implemented.")

    def instructions(self):
        '''
        List of instruction strings
        '''
        raise NotImplementedError("This should be implemented.")

    def notes(self):
        '''
        List of notes
        '''
        raise NotImplementedError("This should be implemented.")
 

class DOMScraper(BaseScraper):
    def __init__(self, url, test=False):
        if test:  # when testing, we load a file
            with url:
                self.soup = BeautifulSoup(
                    url.read(),
                    "html.parser"
                )
        else:
            self.soup = BeautifulSoup(
                requests.get(
                    url,
                    headers=HEADERS,
                    cookies=COOKIES
                ).content,
                "html.parser"
            )
        self.testing_mode = test
        self.url_text = url

    def links(self):
        invalid_href = ('#', '')
        links_html = self.soup.findAll('a', href=True)

        return [
            link.attrs
            for link in links_html
            if link['href'] not in invalid_href
        ]
    
class SchemaScraper(BaseScraper):
    def __init__(self, url):
        self.url_text = url
        html = requests.get(url, headers=HEADERS, cookies=COOKIES)
        data_list = extract(html.text, uniform=True)

        def _find_recipe(c):
            if isinstance(c, dict):
                if "@type" in c.keys() and c["@type"] == "Recipe":
                    return c
                for i in c.values():
                    res = _find_recipe(i)
                    if res:
                        return res
            if isinstance(c, list):
                for i in c:
                    res = _find_recipe(i)
                    if res:
                        return res
            return []

        recipe_data = _find_recipe(data_list)
        if not recipe_data:
            raise WebsiteNotImplementedError(
                "Website does not provide a schema.org Recipe schema in a json-ld format"
            )
        self.data = recipe_data

    def url(self):
        return self.url_text
