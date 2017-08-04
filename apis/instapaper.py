from ast import literal_eval
from urllib import urlencode

import urlparse

import oauth2 as oauth

from utilities.utility_common import print_colour


class Instapaper(object):
    ############################################################
    # Definitions #
    ############################################################
    class Account(object):
        class Endpoints(object):
            def __init__(self):
                self.verify_credentials = "Account: Verify Credentials"
        class Urls(object):
            def __init__(self):
                self.verify_credentials = "https://www.instapaper.com/api/1/account/verify_credentials"
        def __init__(self, _query):
            self._query = _query
            self.endpoints = self.Endpoints()
            self.urls = self.Urls()
        def verify_credentials(self):
            endpoint = self.endpoints.verify_credentials
            url = self.urls.verify_credentials
            params = None
            success, content = self._query(endpoint, url, params)
            if not success:
                pass
            else:
                return literal_eval(content)

    class Bookmarks(object):
        class Endpoints(object):
            def __init__(self):
                self.add = "Bookmarks: Add"
        class Urls(object):
            def __init__(self):
                self.add = "https://www.instapaper.com/api/1/bookmarks/add"
        def __init__(self, _query):
            self._query = _query
            self.endpoints = self.Endpoints()
            self.urls = self.Urls()
        def add(self, new_url, folder_id, content):
            endpoint = self.endpoints.add
            url = self.urls.add
            params = {}
            params['url'] = new_url
            if folder_id:
                params['folder_id'] = folder_id
            if content:
                params['content'] = content
            success, content = self._query(endpoint, url, params)
            if not success:
                return False, literal_eval(content)
            else:
                return True, literal_eval(content)

    class Folders(object):
        class Endpoints(object):
            def __init__(self):
                self.add = "Folders: Add"
                self.list = "Folders: List"
                self.set_order = "Folders: Set Order"
        class Urls(object):
            def __init__(self):
                self.add = "https://www.instapaper.com/api/1/folders/add"
                self.list = "https://www.instapaper.com/api/1/folders/list"
                self.set_order = "https://www.instapaper.com/api/1/folders/set_order"
        def __init__(self, _query):
            self._query = _query
            self.endpoints = self.Endpoints()
            self.urls = self.Urls()
        def add(self, title):
            endpoint = self.endpoints.add
            url = self.urls.add
            params = {
                'title': title
            }
            success, content = self._query(endpoint, url, params)
            if not success:
                pass
            else:
                return literal_eval(content)
        def list(self):
            endpoint = self.endpoints.list
            url = self.urls.list
            params = None
            success, content = self._query(endpoint, url, params)
            if not success:
                pass
            else:
                return literal_eval(content)
        def set_order(self, order):
            endpoint = self.endpoints.list
            url = self.urls.list
            params = {
                'order': order
            }
            success, content = self._query(endpoint, url, params)
            if not success:
                pass
            else:
                return literal_eval(content)

    class OAuth(object):
        class Endpoints(object):
            def __init__(self):
                self.access_token = "OAuth: Access Token"
        class Urls(object):
            def __init__(self):
                self.access_token = "https://www.instapaper.com/api/1/oauth/access_token"
        def __init__(self, _query):
            self._query = _query
            self.endpoints = self.Endpoints()
            self.urls = self.Urls()
        def access_token(self, username, password):
            endpoint = self.endpoints.access_token
            url = self.urls.access_token
            params = {
                "x_auth_username" : username,
                "x_auth_password" : password,
                "x_auth_mode"     : "client_auth",
            }
            success, content = self._query(endpoint, url, params, True)
            if not success:
                print_colour('Instapaper', 'Failed', "Login failed, wrong username or password", 'error')
                exit()
            else:
                print_colour('Instapaper', 'Success', "Login successful", 'success')
                tokens = dict(urlparse.parse_qsl(content.decode('utf-8')))
                return tokens
    ############################################################


    def __init__(self, key, secret):
        self.consumer = oauth.Consumer(key, secret)
        self.client = oauth.Client(self.consumer)
        self.tokens = None
        self.http = None

        self.account = self.Account(self._query)
        self.bookmarks = self.Bookmarks(self._query)
        self.folders = self.Folders(self._query)
        self.oauth = self.OAuth(self._query)

        self.username = None
        self.userid = None
        self.token = None

    def _query(self, endpoint, url, params, get_token=False):
        if isinstance(params, dict):
            params = urlencode(params)
        if get_token:
            response, content = self.client.request(url, "POST", params)
        else:
            response, content = self.http.request(url, "POST", params)
        if response.status != 200:
            print_colour('Instapaper', 'Failed', endpoint, 'debug')
            print_colour('Instapaper', 'Failed', "Status: " + str(response.status), 'debug')
            print_colour('Instapaper', 'Failed', content, 'debug')
            return False, content
        else:
            print_colour('Instapaper', 'Success', endpoint, 'debug')
            return True, content

    def login(self, username, password):
        token = self.oauth.access_token(username, password)
        self.token = oauth.Token(token['oauth_token'], token['oauth_token_secret'])
        self.http = oauth.Client(self.consumer, self.token)
        creds = self.account.verify_credentials()[0]
        self.username = creds['username']
        self.userid = creds['user_id']

    def bookmark_add(self, url, folder_id=None, content=None):
        return self.bookmarks.add(url, folder_id, content)

    def folders_find(self, folder_name):
        folders_list = self.folders.list()
        for folder in folders_list:
            if folder['title'] == folder_name:
                return True, folder['folder_id']
        return False, 0

    def container_find_or_create(self, folder_name):
        success, folder_id = self.folders_find(folder_name)
        if success:
            return folder_id
        new_folder = self.folders.add(folder_name)
        return new_folder[0]['folder_id']

    def folders_sort(self):
        # This api call returns successfully but doesn't actually work...
        folders_list = self.folders.list()
        folders_list.sort(key=lambda x: x['title'])
        new_folders = []
        set_order = ""
        for i, folder in enumerate(folders_list):
            new_folders.append({'title': folder['title'], 'folder_id': folder['folder_id']})
            set_order += str(folder['folder_id']) + ':' + str(i + 1) + ','
        set_order = set_order[:-1]
        print new_folders
        print set_order
        new_order = self.folders.set_order(unicode(set_order, 'utf-8'))
        folders = []
        for folder in new_order:
            folders.append(folder['title'])
        print folders
