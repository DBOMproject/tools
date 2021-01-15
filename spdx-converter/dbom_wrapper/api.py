"""
Copyright 2020 Unisys Corporation

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

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
