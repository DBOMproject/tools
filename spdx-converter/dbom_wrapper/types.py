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

"""
Python dataclasses for Gateway entities
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, TypeVar, Type, cast
import dateutil.parser

T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class GatewayAsset:
    document_name: str
    document_creator: str
    document_created_date: datetime
    asset_metadata: dict
    asset_type: str
    asset_sub_type: str
    asset_manufacturer: str
    asset_model_number: str
    asset_description: str
    manufacture_signature: str
    standard_version: int = 1

    @staticmethod
    def from_dict(obj: Any) -> 'GatewayAsset':
        assert isinstance(obj, dict)
        standard_version = from_int(obj.get("standardVersion"))
        document_name = from_str(obj.get("documentName"))
        document_creator = from_str(obj.get("documentCreator"))
        document_created_date = from_datetime(obj.get("documentCreatedDate"))
        asset_metadata = obj.get("assetMetadata")
        asset_type = from_str(obj.get("assetType"))
        asset_sub_type = from_str(obj.get("assetSubType"))
        asset_manufacturer = from_str(obj.get("assetManufacturer"))
        asset_model_number = from_str(obj.get("assetModelNumber"))
        asset_description = from_str(obj.get("assetDescription"))
        manufacture_signature = from_str(obj.get("manufactureSignature"))
        return GatewayAsset(document_name, document_creator, document_created_date, asset_metadata, asset_type,
                            asset_sub_type, asset_manufacturer, asset_model_number, asset_description,
                            manufacture_signature, standard_version)

    def to_dict(self) -> dict:
        result: dict = {"standardVersion": from_int(self.standard_version),
                        "documentName": from_str(self.document_name),
                        "documentCreator": from_str(self.document_creator),
                        "documentCreatedDate": self.document_created_date.isoformat(),
                        "assetMetadata": self.asset_metadata, "assetType": from_str(self.asset_type),
                        "assetSubType": from_str(self.asset_sub_type),
                        "assetManufacturer": from_str(self.asset_manufacturer),
                        "assetModelNumber": from_str(self.asset_model_number),
                        "assetDescription": from_str(self.asset_description),
                        "manufactureSignature": from_str(self.manufacture_signature)}
        return result


def gateway_asset_from_dict(s: Any) -> GatewayAsset:
    return GatewayAsset.from_dict(s)


def gateway_asset_to_dict(x: GatewayAsset) -> Any:
    return to_class(GatewayAsset, x)
