from typing import Union

import pandas as pd
from .api import API, DataView


class WikipediaDV(DataView):

    def get_pageviews(self, article_name: str, granularity: str = 'monthly'):
        """Get pageview counts for an article

        Args:
            article_name (str): The title of any article in the specified project. Any spaces should be
                replaced with underscores. It also should be URI-encoded, so that non-URI-safe characters 
                like %, / or ? are accepted. Example: Are_You_the_One%3F
            granularity (str, optional): The time unit for the response data. As of today, the only supported granularity 
            for this endpoint is `daily` and `monthly`.

        Returns:
            dict: ageview counts for an article
        """

        return pd.DataFrame(data=self.api.get_pageviews(article_name, granularity)['items'])



def getArticleName(article_id):
    session = requests.session()    
    url ='https://en.wikipedia.org/w/api.php?action=query&pageids=%i&format=json'%(article_id)
    
    tries = 5
    while tries >= 0:
        try :
            res = session.get(url).json()
            res = res['query']['pages'][str(article_id)]['title']
            return res
        
        except (KeyError):
            if tries == 0:
                print (res)        
                print ('API call for function getArticleName was unsuccessful')
                return -1
                raise
            else:
                time.sleep(5) 
                tries -= 1
                continue
    


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


    def get_article(self, article_id: Union[int, str]) -> dict:
        """Get pageview counts for an article
        
        Args:
            article_id (int): Description
        
        Returns:
            dict: ageview counts for an article

        """

        if isinstance(article_id, int):
            url =f'{self.base}action=query&pageids={article_id}&format=json'
        elif isinstance(article_id, str):
            url =f'{self.base}action=query&titles={article_id}&format=json'


        return self.request(url)