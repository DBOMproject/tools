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
Python script to take a read a DBoM asset and write it to a SPDX KV (.tag) file
This does read any sub-asset dependencies at the moment

NOTE: This script needs Python 3.7+ since it uses dataclasses (PEP 557)
To know which arguments to specify, run this script with the --help argument
"""

import argparse
import json

from spdx.creationinfo import *
from spdx.annotation import Annotation
from spdx.creationinfo import CreationInfo
from spdx.document import Document
from spdx.document import License
from spdx.document import LicenseConjunction
from spdx.file import File
from spdx.creationinfo import Person
from spdx.creationinfo import Organization
from spdx.creationinfo import Tool
from spdx.package import Package
from spdx.package import ExternalPackageRef
from spdx.parsers.loggers import StandardLogger
from spdx.parsers.tagvalue import Parser
from spdx.parsers.tagvaluebuilders import Builder
from spdx.review import Review
from spdx.creationinfo import Organization
from spdx.checksum import Algorithm
import spdx.writers.tagvalue as tvwriter
import codecs
from dateutil.parser import parse
from spdx.snippet import Snippet

from dbom_wrapper.api import GatewayAPI
from dbom_wrapper.types import GatewayAsset

parser = argparse.ArgumentParser(description='Utility to create SPDX tag-value files from a DBoM ')
parser.add_argument('-g', '--gateway', type=str,
                    help='The full address (with schema) at which the gateway can be reached', required=True)
parser.add_argument('-r', '--repo', type=str,
                    help='The repository ID on which the channel you want to use exists', required=True)
parser.add_argument('-c', '--channel', type=str,
                    help='The channel ID on which you want to retreive the BoM', required=True)
parser.add_argument('-a', '--asset', type=str,
                    help='The asset ID on which you want to retreive the BoM', required=True)
parser.add_argument('-f', '--file', type=str,
                    help='The SPDX KV Tag that has to be created', required=True)
parser.add_argument('-i', '--idextra', type=str,
                    help='String to append to the id. For testing purposes')

args = parser.parse_args()


def retrieve_asset(asset_id: str):
    """
    Send the asset payload with the provided asset_id to the gateway
    :param asset_id: A string with assetID
    :param payload: A dict representing the payload
    :return: None
    """
    api = GatewayAPI(address=args.gateway)
    if args.idextra:
        asset_id = f"{asset_id}-{args.idextra}"
    print(f"Retrieve asset {args.asset} on channel {args.channel} on repo {args.repo}")
    return  api.retreive_asset(args.repo, args.channel, asset_id)

def parse_creator_string(creator):
    """
    Creates a string from the creator information in the SPDX document
    :param creators: Array of creationinfo objects
    :return: string equivalent
    """
    print('Begin Parsing Creator')
    creators = []
    creator_list = creator.replace(" ", "").split(',')
    for c in creator_list:
        if c[0] != '[':
            creators.append(c)
        else:
            c = c[7:]
            c = c[:-1]
            creators.append(c)
    print('Completed Parsing Creator')
    return creators

def parse_review_list(reviews: []):
    """
    Make Review List from SPDX review spec

    :param reviews: SPDX review Object
    :return: List of dicts with metadata of reviews
    """
    print("Begin Parsing Review List")
    proc_reviews = []
    for review in reviews:
        proc_review = Review()
        proc_review.reviewer = Person(review['reviewer'],'')
        proc_review.review_date = datetime.strptime(review['reviewDate'], '%Y-%m-%dT%H:%M:%fZ')
        if review['comment']:
          # proc_review.has_comment = True
          proc_review.comment = review['comment']
        proc_reviews.append(proc_review)
    print("Completed Parsing Review List")
    return proc_reviews

def parse_pkgref_list(refs: []):
    """
      Make PkgRef List from SPDX review spec

      :param refs: SPDX ExtPkgRef Object
      :return: List of dicts with metadata of Refs
      """
    print("Begin Parsing Ref List")
    proc_refs = []
    for ref in refs:
        proc_ref = ExternalPackageRef()
        proc_ref.category = ref["category"]
        proc_ref.locator = ref["locator"]
        proc_ref.pkg_ext_ref_type = ref["type"]
        if ref["comment"]:
            proc_ref.comment = ref["comment"]
        proc_refs.append(proc_ref)
    print("Completed Parsing Ref List")
    return proc_refs

def rec_parse_license(license):
    if type(license) == dict:
      p_license = License(license["name"],license["id"])
    else:
      p_license = LicenseConjunction(rec_parse_license(license[0]), rec_parse_license(license[1]))

    #  license_dict = [rec_make_license(license.license_1), rec_make_license(license.license_2)]
    return p_license

def parse_license_list(licenses : []):
    license_list = []
    for lic in licenses:
      license = License(lic["name"], lic["id"])
      license_list.append(license)

    return license_list

def parse_license(package, package_dict):

    package.license_comment = package_dict["comment"]
    package.license_declared = rec_parse_license(package_dict["declared"])
    package.conc_lics = rec_parse_license(package_dict["concluded"])
    package.licenses_from_files = parse_license_list(package_dict["fromFile"])

    return package

def parse_license_file(file, package_dict):

    file.license_comment = package_dict["comment"]
    file.conc_lics = rec_parse_license(package_dict["concluded"])
    file.licenses_in_file = parse_license_list(package_dict["fromFile"])

    return file

def parse_license_snippet(snippet, snippet_dict):

    snippet.license_comment = snippet_dict["comment"]
    snippet.conc_lics = rec_parse_license(snippet_dict["concluded"])
    snippet.licenses_in_snippet = parse_license_list(snippet_dict["inSnippet"])

    return snippet

def parse_files(package_dict):

    files = []
    for f in package_dict["files"]:
      file = File(f['name'])
      file.type = f['type']
      file.spdx_id = f['id']
      file = parse_license_file(file, f['license'])
      file.copyright = f['copyright']
      file.comment = f['comment']
      file.chk_sum = Algorithm(f["checksumAlgorithm"], f["checksum"])
      files.append(file)
    return files

def parse_annotation_list(annotations : []):

    annotation_list = []
    for a in annotations:
      annotation = Annotation()
      annotation.spdx_id = a['id']
      annotation.comment = a['comment']
      annotation.annotation_type = a['type']
      annotation.annotation_date = datetime.strptime(a['date'], '%Y-%m-%dT%H:%M:%fZ') 
      annotation.annotator = Person(a['annotator']['name'], a['annotator']['email'])
      annotation_list.append(annotation)
    return annotation_list

def parse_snippet_list(snippets : []):

    snippet_list = []
    for s in snippets:
      snippet = Snippet()
      snippet.spdx_id = s['id']
      snippet.name = s['name']
      snippet.comment = s['comment']
      snippet.copyright = s['copyright']
      snippet.snip_from_file_spdxid = s['fromFileID']
      snippet = parse_license_snippet(snippet, s['license'])
      snippet_list.append(snippet)
    return snippet_list

def parse_package(package_dict):
    """
      Make PkgRef List from SPDX review spec

      :param refs: SPDX ExtPkgRef Object
      :return: List of dicts with metadata of Refs
      """
    package = Package()
    package.name = package_dict["name"] 
    package.spdx_id = package_dict["id"]
    package.version = package_dict["version"]
    package.download_location = package_dict["downloadLocation"]
    package.summary = package_dict["summary"]
    package.source_info = package_dict["sourceInfo"]
    package.file_name = package_dict["fileName"]
    package.supplier =  Organization( package_dict["supplierName"], package_dict["supplierEmail"])
    package.originator =  Organization( package_dict["originatorName"], package_dict["originatorEmail"])
    package.check_sum = Algorithm( package_dict["checksumAlgorithm"],package_dict["checksum"])
    package.files = parse_files(package_dict)
    package.verif_code = package_dict["verificationCode"]
    package.description = package_dict["description"]
    package.comment = package_dict["comment"]
    package.cr_text = package_dict["copyright"]
    package = parse_license(package, package_dict["license"])
    return package

def create_dbom_asset_payload(spdx_document: Document):
    """
    Creates a payload that the gateway would accept using ONLY package information from spdx_document

    :param spdx_document: An SPDX document object generated by the SPDX Python SDK
    :return: A valid asset payload for the gateway
    """
    metadata_dict = {
        "reviews": make_review_list(spdx_document.reviews),
        "license": document.package.license_declared.identifier,
        "extrefs": make_pkgref_list(spdx_document.package.pkg_ext_refs)
    }

    payload = GatewayAsset(
        document_name=spdx_document.package.name,
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

def create_sbom(asset):
    """
    Creates a payload that the gateway would accept using ONLY package information from spdx_document

    :param spdx_document: An SPDX document object generated by the SPDX Python SDK
    :return: A valid asset payload for the gateway
    """

    document = Document()
    creator = parse_creator_string(asset['documentCreator'])
    document.creation_info = CreationInfo()
    document.creation_info.created = datetime.strptime(asset['documentCreatedDate'], '%Y-%m-%dT%H:%M:%f')
    document.creation_info.creators.append(Person( name= creator[0], email= ''))
    document.creation_info.creators.append(Organization( name= creator[1], email= ''))
    document.creation_info.creators.append(Tool (name= creator[2]))
    document.reviews = parse_review_list(asset['assetMetadata']['reviews'])
    document.package = parse_package(asset['assetMetadata']['package'])
    document.annotations = parse_annotation_list(asset['assetMetadata']['annotations'])
    document.snippet = parse_snippet_list(asset['assetMetadata']['snippets'])
    document.package.pkg_ext_refs = parse_pkgref_list(asset['assetMetadata']['extrefs'])

    document.version = 'SPDX-2.1'
    document.data_license = rec_parse_license(asset['assetMetadata']['dataLicense'])
    document.name = asset['documentName']
    document.spdx_id = asset['assetMetadata']['id']
    document.namespace = asset['assetMetadata']['namespace']
    document.comment = asset['assetMetadata']['comment']
    return document


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
    print("Retrieving BoM from gateway")
    asset = retrieve_asset(args.asset)
    while asset is None:
        pass
    sbom = create_sbom(asset)

    print('Begin Write SBoM')
    with codecs.open(file, mode='w', encoding='utf-8') as out:
      tvwriter.write_document(sbom, out)
    print('Completed Write SBoM')
    