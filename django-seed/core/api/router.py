import imp
import os
from glob import glob

from django.conf import settings
from django.urls import include, re_path
from django.urls.resolvers import URLPattern, URLResolver


class Router:

    def __init__(self, name):
        # router name, will use to add prefix api
        self._name = name

        # store list of RegexURLPattern, RegexURLResolver
        self._urls = []

    def add(self, target):
        """Add api to router
        
        Arguments:
            target {mixed} -- folder_path, Router, URLPattern, URLResolver
        """

        if isinstance(target, str):
            # add urls from folder path
            apis = self._load_apis(target)
            self._urls += self._gen_urls(apis)

        elif isinstance(target, self.__class__):
            # add urls from other Router
            self._urls.append(target.url())

        elif isinstance(target, (URLPattern, URLResolver)):
            # add url from url()
            self._urls.append(target)

        else:
            raise Exception('api_router_add_invalid')
        
            
    def _load_apis(self, api_path):
        """Load list of api from dir path

        Returns:
            [list] -- [{ 'url': url, 'module': module }]
        """

        api_path_absolute = os.path.join(settings.BASE_DIR, api_path)
        path_apis = [y for x in os.walk(api_path_absolute) for y in glob(os.path.join(x[0], '*.py'))]

        apis = []

        for path in path_apis:

            # ignore module start with underscore
            if path.split('/')[-1].find('_') == 0:
                continue

            # remove api_path_absolute and extension python
            url = path.replace(api_path_absolute, '')[:-3]

            # strip / and convert kebab-case
            url = url.strip('/').replace('_', '-')

            # load module from path
            module = imp.load_source('module_api' + url, path)

            apis.append({ 'url': url, 'module': module })
        return apis

    def _gen_urls(self, apis):
        """Gen list url
        
        Arguments:
            apis {list} -- list api, RegexURLPattern
        
        Returns:
            list -- list RegexURLPattern
        """

        urls = []

        for api in apis:
            u = None
            
            if isinstance(api, dict) and 'url' in api and 'module' in api:
                u = re_path(r'^%s/?$' % api['url'], api['module'].Main.as_view())
            elif isinstance(api, URLPattern):
                u = api
            
            urls.append(u)

            print(u)

        return urls

    def url(self):
        # return url pattern with name prefix
        prefix = self._name.strip('^/')
        return re_path('^{name}/'.format(name=self._name), include(self._urls))
