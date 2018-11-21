import pandas as pd

from .api import API, DataView

class XtoolsDV(DataView):

    def get_page_info(self, page: str) -> pd.Series:
        """Get pageview counts for an page

        Args:
            page_id (str): Description

        Returns:
            pd.Series: info of the page

        """

        res = self.api.get_page_info(page)

        return pd.Series(res)



class XtoolsAPI(API):

    """Summary

    Attributes:
        project (TYPE): Description
    """

    def __init__(self,
                 domain: str='xtools.wmflabs.org',
                 project: str='en.wikipedia.org',
                 api_username: str=None,
                 api_password: str=None,
                 api_key: str=None,
                 protocol: str='https',
                 attempts: int=2):
        """Constructor of the WikiWhoAPI

        Args:
            domain (str, optional): the domain that hosts the api
            project (str, optional): e.g. en.wikipedia.org
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
        self.project = project
        self.base = f"{self.base}api/"

    def get_page_info(self, page_name: str) -> dict:
        """Get basic information about the history of a page.

        Args:
            page_name (str): Full page title.

        Returns:
            dict: basic information about the history of a page.
        """

        return self.request(f'{self.base}page/articleinfo/{self.project}/{page_name}')
