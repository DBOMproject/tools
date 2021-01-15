#!/usr/bin/python3

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
Python script to take a SPDX KV (.tag) file and send it to an instance of the DBoM Gateway
This does not push/link any sub-asset dependencies at the moment

NOTE: This script needs Python 3.7+ since it uses dataclasses (PEP 557)
To know which arguments to specify, run this script with the --help argument
"""

import argparse
import json

from spdx.creationinfo import *
from spdx.annotation import Annotation
from spdx.document import Document
from spdx.document import License
from spdx.package import ExternalPackageRef
from spdx.package import Package
from spdx.parsers.loggers import StandardLogger
from spdx.parsers.tagvalue import Parser
from spdx.parsers.tagvaluebuilders import Builder
from spdx.review import Review
from spdx.snippet import Snippet

from dbom_wrapper.api import GatewayAPI
from dbom_wrapper.types import GatewayAsset

parser = argparse.ArgumentParser(description='Utility to convert SPDX tag-value files ')
parser.add_argument('-g', '--gateway', type=str,
                    help='The full address (with schema) at which the gateway can be reached', required=True)
parser.add_argument('-r', '--repo', type=str,
                    help='The repository ID on which the channel you want to use exists', required=True)
parser.add_argument('-c', '--channel', type=str,
                    help='The channel ID on which you want to commit the BoM', required=True)
parser.add_argument('-f', '--file', type=str,
                    help='The SPDX KV Tag that has to be sent', required=True)
parser.add_argument('-i', '--idextra', type=str,
                    help='String to append to the id. For testing purposes')

args = parser.parse_args()


def create_asset(asset_id: str, payload: dict):
    """
    Send the asset payload with the provided asset_id to the gateway
    :param asset_id: A string with assetID
    :param payload: A dict representing the payload
    :return: None
    """
    api = GatewayAPI(address=args.gateway)
    if args.idextra:
        asset_id = f"{asset_id}-{args.idextra}"
    print(f"Using channel {args.channel} on repo {args.repo}")
    api.create_asset(args.repo, args.channel, asset_id, payload)
    printsep()
    print(f"You can find the asset at {args.gateway}/api/v1/repo/{args.repo}/chan/{args.channel}/asset/{asset_id}")


def make_creator_string(creators: []):
    """
    Creates a string from the creator information in the SPDX document
    :param creators: Array of creationinfo objects
    :return: string equivalent
    """
    creator_list = []
    for creator in creators:
        if type(creator) != Tool:
            creator_list.append(f"{creator.name} <{creator.email}>" if creator.email else creator.name)
        else:
            creator_list.append(f"[Using: {creator.name}]")
    return ', '.join(creator_list)


def make_review_list(reviews: [Review]):
    """
    Make Review List from SPDX review spec

    :param reviews: SPDX review Object
    :return: List of dicts with metadata of reviews
    """
    proc_reviews = []
    for review in reviews:
        t_dict = {
            "reviewer": review.reviewer.name,
            "reviewDate": review.review_date_iso_format,
        }
        if review.has_comment:
            t_dict["comment"] = review.comment
        proc_reviews.append(t_dict)
    return proc_reviews


def make_pkgref_list(refs: [ExternalPackageRef]):
    """
      Make PkgRef List from SPDX review spec

      :param refs: SPDX ExtPkgRef Object
      :return: List of dicts with metadata of Refs
      """
    proc_refs = []
    for ref in refs:
        t_dict = {
            "category": ref.category,
            "locator": ref.locator,
            "type": ref.pkg_ext_ref_type
        }
        if ref.comment:
            t_dict["comment"] = ref.comment
        proc_refs.append(t_dict)
    return proc_refs

def rec_make_license(license):
    """
      Make PkgRef List from SPDX review spec

      :param refs: SPDX ExtPkgRef Object
      :return: List of dicts with metadata of Refs
      """

    #for attr in dir(license.license_1):
    #  print("license.license_1.%s = %r" % (attr, getattr(license.license_1, attr)))

    if type(license) == License:
      license_dict = {
        "id": license.identifier,
        "url": license.url,
        "name": license.full_name
      }
    else:
      license_dict = [rec_make_license(license.license_1), rec_make_license(license.license_2)]
    return license_dict

def make_license_list(licenses : [License]):
    """
      Make PkgRef List from SPDX review spec

      :param refs: SPDX ExtPkgRef Object
      :return: List of dicts with metadata of Refs
      """

    license_list = []
    for license in licenses:
      license_list.append({
        "id": license.identifier,
        "url": license.url,
        "name": license.full_name
      })
    return license_list

def make_license(package):
    """
      Make PkgRef List from SPDX review spec

      :param refs: SPDX ExtPkgRef Object
      :return: List of dicts with metadata of Refs
      """
    license_dict = {
      "comment" : package.license_comment,
      "declared": rec_make_license(package.license_declared),
      "concluded": rec_make_license(package.conc_lics),
      "fromFile": make_license_list(package.licenses_from_files)
    }
    return license_dict

def make_license_file(file):
    """
      Make PkgRef List from SPDX review spec

      :param refs: SPDX ExtPkgRef Object
      :return: List of dicts with metadata of Refs
      """
    license_dict = {
      "comment" : file.license_comment,
      "concluded": rec_make_license(file.conc_lics),
      "fromFile": make_license_list(file.licenses_in_file)
    }
    return license_dict

def make_license_snippet(snippet):
    """
      Make PkgRef List from SPDX review spec

      :param refs: SPDX ExtPkgRef Object
      :return: List of dicts with metadata of Refs
      """
    license_dict = {
      "comment" : snippet.license_comment,
      "concluded": rec_make_license(snippet.conc_lics),
      "inSnippet": make_license_list(snippet.licenses_in_snippet)
    }
    return license_dict

def make_files(package):
    """
      Make PkgRef List from SPDX review spec

      :param refs: SPDX ExtPkgRef Object
      :return: List of dicts with metadata of Refs
      """
    files = []
    for file in package.files:
      files.append({
        "name": file.name,
        "type": file.type,
        "id": file.spdx_id,
        "license": make_license_file(file),
        "copyright": file.copyright,
        "comment": file.comment,
        "checksum": file.chk_sum.value,
        "checksumAlgorithm": file.chk_sum.identifier,
      })
    return files

def make_annotation_list(annotations : [Annotation]):

    annotation_list = []
    for annotation in annotations:
      annotation_list.append({
        "id": annotation.spdx_id,
        "comment": annotation.comment,
        "type": annotation.annotation_type,
        "date": annotation.annotation_date_iso_format,
        "annotator" : {
          "name": annotation.annotator.name,
          "email": annotation.annotator.email
        }
      })
    return annotation_list

def make_snippet_list(snippets : [Snippet]):

    snippet_list = []
    for snippet in snippets:
      snippet_list.append({
        "id": snippet.spdx_id,
        "name": snippet.name,
        "comment": snippet.comment,
        "copyright": snippet.copyright,
        "license": make_license_snippet(snippet),
        "fromFileID" : snippet.snip_from_file_spdxid
      })
    return snippet_list

def make_package(package):
    """
      Make PkgRef List from SPDX review spec

      :param refs: SPDX ExtPkgRef Object
      :return: List of dicts with metadata of Refs
      """
    
    package_dict = {
      "name" : package.name,
      "id": package.spdx_id,
      "version": package.version,
      "downloadLocation": package.download_location,
      "summary": package.summary,
      "sourceInfo": package.source_info,
      "fileName": package.file_name,
      "supplierName": package.supplier.name,
      "supplierEmail": package.supplier.email,
      "originatorName": package.originator.name,
      "originatorEmail": package.originator.email,
      "checksum": package.check_sum.value,
      "checksumAlgorithm": package.check_sum.identifier,
      "verificationCode": package.verif_code,
      "description": package.description,
      "comment": package.comment,
      "copyright": package.cr_text,
      "license": make_license(package),
      "files": make_files(package)
    }
    return package_dict


def create_dbom_asset_payload(spdx_document: Document):
    """
    Creates a payload that the gateway would accept using ONLY package information from spdx_document

    :param spdx_document: An SPDX document object generated by the SPDX Python SDK
    :return: A valid asset payload for the gateway
    """
    metadata_dict = {
        "reviews": make_review_list(spdx_document.reviews),
        "license": document.package.license_declared.identifier,
        "extrefs": make_pkgref_list(spdx_document.package.pkg_ext_refs),
        "package": make_package(spdx_document.package),
        "id": spdx_document.spdx_id,
        "namespace": spdx_document.namespace,
        "comment": spdx_document.comment,
        "dataLicense": rec_make_license(spdx_document.data_license),
        "annotations": make_annotation_list(spdx_document.annotations),
        "snippets": make_snippet_list(spdx_document.snippet)
    }

    payload = GatewayAsset(
        document_name=spdx_document.name,
        document_creator=make_creator_string(document.creation_info.creators),
        document_created_date=document.creation_info.created,
        asset_type="SoftwareComponent",
        asset_sub_type="BuildArtifact",
        asset_manufacturer=f"{document.package.originator.name} [{document.package.supplier.name}]",
        asset_description=document.package.description,
        asset_model_number=document.package.version,
        asset_metadata=metadata_dict,
        manufacture_signature="NOT SIGNED (DEMO)"
    )
    return payload.to_dict()


def printsep():
    """
    Print Separator
    :return: None
    """
    print("=" * 80)


if __name__ == '__main__':
    p = Parser(Builder(), StandardLogger())
    p.build()
    file = args.file
    print(f"Attempting to parse file {file}")
    with open(file) as f:
        data = f.read()
        document, error = p.parse(data)
        if not error:
            print('Parsing Successful. Summary:')
            printsep()
            print('Document Version {0}.{1}'.format(document.version.major,
                                                    document.version.minor))
            print('Package name : {0}'.format(document.package.name))
            print('Creators : ')
            for creator in document.creation_info.creators:
                print(creator.name)
            printsep()

            print("Creating DBOM Asset Payload")
            asset_payload = create_dbom_asset_payload(document)
            print("Success. Payload:")
            printsep()
            print(json.dumps(asset_payload, indent=True))
            printsep()

            print("Sending BoM to gateway")
            create_asset(document.package.spdx_id, asset_payload)
        else:
            print('Errors encountered while parsing')
