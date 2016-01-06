# -*- coding:utf-8 -*-

import urllib2
import urllib
import json


class RequestClient():
    def __init__(self, base_url=None):
        self.base_url = 'http://127.0.0.1:8080/v1.0/'

    def request(self, url, method='GET', headers={}, data=None, isJson=True):

        if isJson:
            headers['Content-Type'] = 'application/json'
        else:
            data = urllib.urlencode(data)

        req = urllib2.Request(url, headers=headers)

        if method in ['PUT', 'DELETE']:
            req.get_method = lambda: method

        response = urllib2.urlopen(req, data)

        return response


def request(url, method='POST', headers={}, data=None, isJson=True):
    request_Client = RequestClient()
    return json.loads(request_Client.request(request_Client.base_url+url, method, headers, data, isJson=True).read())


if __name__ == "__main__":
    pass
    data={'account_id': '406b3857-969c-4795-ace1-524888075d75'}
    data = json.dumps(data)
    response = request('book/becomeprojectadmin', method='POST', data=data)
    print response

