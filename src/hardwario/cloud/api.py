import requests

DEFAULT_API_URL = 'https://api.hardwario.cloud'


class ApiException(Exception):
    pass


class Api:

    def __init__(self, url=DEFAULT_API_URL, token=None):
        self._headers = {}
        self._url = url
        if token:
            self.set_token(token)

    def set_token(self, token):
        self._headers['Authorization'] = 'Bearer ' + token

    def request(self, method, expect_code, url, **kwargs):
        try:
            self._response = requests.request(
                method, self._url + url, headers=self._headers, **kwargs)
        except ConnectionError:
            raise ApiException('Cannot connect to cloud service')

        if expect_code and expect_code != self._response.status_code:
            text = self._response.text.strip('"')
            raise ApiException(f'{self._response.status_code}: {text}')

        return self._response.json()

    def _list(self, url, params: dict, offset=0, limit=None):
        if params is None:
            params = {}

        cnt = 0
        params['offset'] = offset

        while True:
            params['limit'] = 2 if limit is None else limit

            for row in self.request('GET', 200, url, params=params):
                cnt += 1
                yield row

            if limit is not None and limit >= cnt:
                break

            x_total = int(self._response.headers['x-total'])
            params['offset'] = offset + cnt

            if params['offset'] >= x_total:
                break

    def codec_create(self, name, note=None):
        body = {'name': name}
        if note:
            body['note'] = note
        return self.request('POST', 200, '/v1/codecs', json=body)

    def codec_update(self, id: str, name: str = None, note: str = None, decoder_type: str = None, decoder: str = None):
        body = {}
        if name:
            body['name'] = name
        if note:
            body['note'] = note
        if decoder_type:
            body['decoder_type'] = decoder_type
        if decoder:
            body['decoder'] = decoder

        return self.request('PUT', 200, f'/v1/codec/{id}', json=body)

    def codec_list(self, fields: list = None, offset: int = 0, limit: int = None):
        params = {}
        if fields:
            params['fields'] = ','.join(fields)
        return self._list('/v1/codecs', params, offset, limit)

    def codec_detail(self, id):
        return self.request('GET', 200, f'/v1/codec/{id}')

    def codec_delete(self, id):
        return self.request('DELETE', 200, f'/v1/codec/{id}')

    def codec_attach_to_device(self, id, device_id):
        return self.request('PUT', 200, f'/v1/device/{device_id}', json={'codec_id': id})

    def codec_attach_to_group(self, id, group_id):
        return self.request('PUT', 200, f'/v1/group/{group_id}', json={'codec_id': id})
