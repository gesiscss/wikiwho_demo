from typing import Union

import pandas as pd
from .api import API, DataView



class WikipediaDV(DataView):

    def get_page(self, page: Union[int, str]) -> pd.Series:
        """Get pageview counts for an page

        Args:
            page_id (Union[int, str]): Description

        Returns:
            pd.Series: info of the page

        """

        res = self.api.get_page(page)

        pages = res['query']['pages']
        if len(pages) == 0:
            raise Exception('Article Not Found')

        elif len(pages) > 1:
            raise Exception('Several pages found')

        page_dict = next(iter(pages.values()))

        return pd.Series({
            'page_id': page_dict['pageid'],
            'title': page_dict['title'],
            'ns': page_dict['ns'],
            'to': res['query']['normalized'][0]['to'],
            'from': res['query']['normalized'][0]['from'],
        })



class WikipediaAPI(API):

    """Summary

    Attributes:
        project (TYPE): Description
    """

    def __init__(self,
                 domain: str='en.wikipedia.org',

                 api_username: str=None,
                 api_password: str=None,
                 api_key: str=None,
                 protocol: str='https',
                 attempts: int=2):
        """Constructor of the WikiWhoAPI

        Args:
            domain (str, optional): the domain that hosts the api
            project (str, optional): e.g. en.wikipedia.org
            version (str, optional): version of the API (e.g. rest_v1)
            api_username (str, optional): WikiWho API username
            api_password (str, optional): WikiWho API password
            api_key (str, optional): WikiWho API key
            protocol (str, optional): the protocol of the url
            attempts (int, optional): the number of attempts before giving up trying to connect
        """
        super().__init__(protocol=protocol,
                         domain=domain,
                         api_username=api_username,
                         api_password=api_password,
                         api_key=api_key,
                         attempts=attempts)
        self.base = f'{self.base}w/api.php?'

    def get_page(self, page_id: Union[int, str]) -> dict:
        """Get pageview counts for an page

        Args:
            page_id (int): Description

        Returns:
            dict: ageview counts for an page

        """

        if isinstance(page_id, int):
            url = f'{self.base}action=query&pageids={page_id}&format=json'
        elif isinstance(page_id, str):
            url = f'{self.base}action=query&titles={page_id}&format=json'


        return self.request(url)
