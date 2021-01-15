import http
import json
import requests


class DbomException(Exception):
    """
    Base Class for all exceptions in this module
    """
    pass


class APIException(DbomException):
    """
    Exception that occured during an API call
    """

    def __init__(self, status_code, payload, message):
        self.status_code = status_code
        self.payload = payload
        self.message = message


class GatewayAPI:
    """
    Class for abstracting DBoM gateway operations
    Currently only supports asset creation
    """

    def __init__(self, address):
        self.address = address

    def create_asset(self, repo: str, channel: str, asset_id, payload: dict):
        print(f"Attempting to contact gateway at {self.address}")

        url = f"{self.address}/api/v1/repo/{repo}/chan/{channel}/asset/{asset_id}"

        payload = json.dumps(payload)
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code in [http.HTTPStatus.OK, http.HTTPStatus.CREATED]:
            print(f"Success Response From Gateway:\n{response.text.encode('utf8')}")
        else:
            raise APIException(response.status_code, payload, response.text.encode('utf8'))

    def retreive_asset(self, repo: str, channel: str, asset_id):
        print(f"Attempting to contact gateway at {self.address}")

        url = f"{self.address}/api/v1/repo/{repo}/chan/{channel}/asset/{asset_id}"

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers)

        if response.status_code in [http.HTTPStatus.OK, http.HTTPStatus.OK]:
            print(f"Success Response From Gateway:\n{response.text.encode('utf8')}")
            asset = json.loads(response.text.encode('utf8'))
            print(asset['standardVersion'])
            return asset
        else:
            raise APIException(response.status_code, payload, response.text.encode('utf8'))
