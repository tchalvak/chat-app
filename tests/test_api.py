import requests
import configparser
import json
import pprint
#from lxml.html import fromstring

CONFIG_PATH = r'./CONFIG'

with open(CONFIG_PATH, 'r') as f:
    config_string = '[chat-config]\n' + f.read()
config = configparser.ConfigParser()
config.read_string(config_string)


class TestApi:
    ''' Hits the api endpoints while logged out, and checks whether anything 
        like json comes back.
    '''

    def api_root(self):
        '''Get the API root and version parts from the config'''
        return (
            config.get('chat-config', 'API_DOMAIN') + 
            config.get('chat-config', 'API_BASE')
            )

    def status_code(self, url):
        ''' Gets http status codes of pages/urls '''
        try:
            r = requests.head(url)
            return r.status_code
        except requests.ConnectionError:
            return None

    def pull_json(self, url, endpoint):
        ''' Get a page to parse as json, for the api 
            there may be better ways to do this later'''
        params = dict()
        resp = requests.get(url=url, params=params)
        return resp.text


    def test_root_url_config_works(self):
        ''' Ensure root is configured '''
        assert (self.api_root() is not None and
                len(str(self.root())) > 5)


    def test_api_urls(self):
        root = self.api_root()
        endpoints = ['chats', 'chats/1']
        for endpoint in endpoints:
            data = self.pull_json(root, endpoint)
            assert (data is not None and 
                    json.loads(data) is not False and
                    len(json.loads(data)) > 0
                    )
