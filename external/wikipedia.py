"""Summary
"""
from typing import Union

import pandas as pd
from .api import API, DataView


class WikipediaDV(DataView):

    """Summary
    """

    def get_page(self, page: Union[int, str]) -> pd.Series:
        """Get pageview counts for an page

        Args:
            page (Union[int, str]): Description

        Returns:
            pd.Series: info of the page

        Deleted Parameters:
            page_id (Union[int, str]): Description

        Raises:
            Exception: Description

        """

        res = self.api.get_page(page)

        pages = res['query']['pages']
        if len(pages) == 0:
            raise Exception('Article Not Found')

        elif len(pages) > 1:
            raise Exception('Several Pages Found')

        page_dict = next(iter(pages.values()))

        return pd.Series({
            'page_id': page_dict['pageid'],
            'title': page_dict['title'],
            'ns': page_dict['ns'],
        })

    def get_editor(self, editor: Union[int, str]) -> pd.Series:
        """Summary

        Args:
            editor (Union[int, str]): Description

        Returns:
            pd.Series: Description
        """
        res = self.api.get_editor(editor)

        editors = res['query']['users']
        if len(editors) == 0:
            raise Exception('Editor Not Found')

        elif len(editors) > 1:
            raise Exception('Several Editors Found')

        return pd.Series(editors[0])


class WikipediaAPI(API):

    """Summary

    Attributes:
        base (TYPE): Description

    Deleted Attributes:
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
            api_username (str, optional): WikiWho API username
            api_password (str, optional): WikiWho API password
            api_key (str, optional): WikiWho API key
            protocol (str, optional): the protocol of the url
            attempts (int, optional): the number of attempts before giving up trying to connect

        Deleted Parameters:
            project (str, optional): e.g. en.wikipedia.org
            version (str, optional): version of the API (e.g. rest_v1)
        """
        super().__init__(protocol=protocol,
                         domain=domain,
                         api_username=api_username,
                         api_password=api_password,
                         api_key=api_key,
                         attempts=attempts)
        self.base = f'{self.base}w/api.php?'

    def get_page(self, page: Union[int, str]) -> dict:
        """Get pageview counts for an page

        Args:
            page (Union[int, str]): Description

        Returns:
            dict: ageview counts for an page

        """

        if isinstance(page, int):
            url = f'{self.base}action=query&pageids={page}&format=json'
        elif isinstance(page, str):
            url = f'{self.base}action=query&titles={page}&format=json'

        return self.request(url)

    def get_editor(self, editor: Union[int, str]) -> dict:
        """Get pageview counts for an page

        Args:
            editor (Union[int, str]): Description

        Returns:
            dict: ageview counts for an page

        """

        # if isinstance(editor, int):
        #     url = f'{self.base}action=query&list=users&ususerids={editor}&format=json'
        # elif isinstance(editor, str):
        # url =
        # f'{self.base}action=query&list=users&ususers={editor}&format=json'

        if isinstance(editor, int):
            url = f'{self.base}action=query&list=users&ususerids={editor}&usprop=blockinfo|editcount|registration|gender&format=json'
        elif isinstance(editor, str):
            url = f'{self.base}action=query&list=users&ususers={editor}&usprop=blockinfo|editcount|registration|gender&format=json'

        return self.request(url)
