from django.views import View
from django.http import HttpResponse
import json

from core.utils import json_from
from core.api import exception

DEFAULT_PARAM = object()


class APIBase(View):

    def __init__(self, *args, **kwargs):
        self.header = {}
        self.cookie = {}
        self.query = {}
        self.body = {}
        self.request = None
        self.response = None
        
        super().__init__(*args, **kwargs)

    def _parser(self, request, *args, **kwargs):
        """Collect data from request

        This method will call on top of dispatch
        """

        self.request = request

        # parse header
        self.header = {k[5:]: v for k, v in request.META.items() if k.startswith('HTTP_')}
        self.header['CONTENT_TYPE'] = request.META.get('CONTENT_TYPE')

        # parse boby
        if request.method not in ['GET', 'HEAD']:

            # TODO: serve other body format
            if 'multipart/form-data' in self.header['CONTENT_TYPE']:
                self.body = request.POST.dict()

            else:
                # default: application/json
                if self.request.body:
                    try:
                        self.body = json.loads(self.request.body)
                    except Exception as e:
                        raise Exception('parse json body error')
                
        # parse query
        self.query = request.GET.dict()

        # parse cookie
        self.cookie = {k: v for k, v in request.COOKIES.items()}

    def middleware_before(self):
        """Call before handler
        
        Returns:
            mixed -- None to pass, self.res() to end request
        """
        pass
    
    def middleware_after(self):
        """Call after handler, before response request
        
        Returns:
            mixed -- None to pass, self.res() to end request
        """
        pass

    def get_param(self, key, default=DEFAULT_PARAM, convert=None):
        value = default
        
        if key in self.body:
            value = self.body[key]
        elif key in self.query:
            value = self.query[key]

        if value == DEFAULT_PARAM:
            raise Exception(u'missing param: %s' % key)

        if convert is not None:
            try:
                return convert(value)
            except Exception as ex:
                get_logger().error('api_base_convert_error', exc_info=1)

        return value

    def res(self, data=None, meta=None, error=None, raw=None, status_code=None, header=None, cookie=None,
            redirect=None, paging=None):
        """Generate response

        Keyword Arguments:
            meta {dict} -- meta key
            error {str|dict} -- error key
            status_code {init} -- http status code
            header {dict} -- response header
            cookie {dict} -- response cookie
            redirect {str} -- url to redirect
            paging {int} -- number of page

        Returns:
            HttpResponse
        """

        response = {}

        if redirect:
            return redirect_url(redirect)

        if raw is not None:
            response = raw
        elif error is not None:
            msg = ''

            if isinstance(error, str):
                msg = error

            response['error'] = {
                'message': msg,
                'full_path': self.request.path,
                'method': self.request.method,
            }

            if isinstance(error, dict):
                response['error'].update(error)

            if not status_code:
                status_code = 400
        else:
            if meta is not None:
                response['meta'] = meta

            if data is not None:
                response['data'] = data

        if not status_code:
            status_code = 200

        if paging is not None:
            if 'meta' not in response:
                response['meta'] = {}
            # response['meta']['next'] = get_next_url(self, data, paging)
        
        response = HttpResponse(json_from(response), status=status_code, content_type='application/json')

        if header:
            for k, v in header.items():
                response[k] = v

        if cookie:
            for k, v in cookie.items():
                response.set_cookie(k, v, max_age=31536000)

        return response

    def http_method_not_allowed(self):
        return self.res(error='http method not allowed')

    def options(self):
        return self.res(header={
            'Allow': ', '.join(self._allowed_methods()),
            'Content-Length': '0',
        })

    def dispatch(self, request, *args, **kwargs):

        try:
            # parse request, results will store in instance attributes
            self._parser(request, *args, **kwargs)
            
            # authenticate request, is_authenticated will assign user to self.request.user
            # if self.authentication and not self.authentication.is_authenticated(request):
            #     return self.res(error="forbidden", status_code=403)

            # call middleware_before, end request if midleware return response
            res_middleware = self.middleware_before()
            if res_middleware:
                return res_middleware

            # get right method handler and excute to get handler response
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            self.response = handler()

            # call middleware_after, end request if midleware return response
            res_middleware = self.middleware_after()
            if res_middleware:
                return res_middleware

            if not isinstance(self.response, HttpResponse):
                return self.res(error='handler method must return self.res, not %s' % type(self.response))

            return self.response

        except exception.Redirect as ex:
            return self.res(redirect=ex.message)

        except exception.Unauthorized as ex:
            return self.res(error=ex.message or "unauthorized", status_code=401)

        except exception.Forbidden as ex:
            return self.res(error=ex.message or "forbidden", status_code=403)

        except exception.NotFound as ex:
            return self.res(error=ex.message or "not found", status_code=404)
