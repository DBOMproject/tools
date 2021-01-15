# DBoM SDPX Convert

Contains a utility for creating dbom assets from spdx documents and another utility for reading them back into spdx format.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

  - [Usage](#usage)
  - [Docker](#docker)
  - [Development](#development)
- [DBoM To SPDX Converter](#dbom-to-spdx-converter)
  - [Usage](#usage-1)
  - [Docker](#docker-1)
  - [Jenkins](#jenkins)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## SPDX To DBoM Converter
A python wrapper that can convert SPDX 2.1 KeyValue files (.tag) to the format expected by the gateway. It can also send this converted payload to a specified Gateway URI, Repository ID and Channel ID

### Python Usage

    spdx_to_dbom.py [-h] -g GATEWAY -r REPO -c CHANNEL -f FILE [-i IDEXTRA]
    
      -h, --help            show this help message and exit
      -g GATEWAY, --gateway GATEWAY
                            The full address (with schema) at which the gateway
                            can be reached
      -r REPO, --repo REPO  The repository ID on which the channel you want to use
                            exists
      -c CHANNEL, --channel CHANNEL
                            The channel ID on which you want to commit the BoM
      -f FILE, --file FILE  The SPDX KV Tag that has to be sent
      -i IDEXTRA, --idextra IDEXTRA
                            String to append to the id. For testing purposes

### Docker Usage

    mkdir input

    cp sbom.tag input/sbom.tag

    docker build -t spdx_to_dbom ./ -f ./spdx_to_dbom/Dockerfile

    docker run -e "GATEWAY=$GATEWAY" -e "REPO=$REPO" -e "CHANNEL=$CHANNEL" -e "FILE=$FILE" -e "ASSET=$ASSET" -e "ID=$ID" -v "$(pwd)"/input:/input spdx_to_dbom
    
      GATEWAY
                            The full address (with schema) at which the gateway
                            can be reached
      REPO  The repository ID on which the channel you want to use
                            exists
      CHANNEL
                            The channel ID on which you want to commit the BoM
      FILE                  The SPDX KV Tag that has to be sent
      IDEXTRA
                            String to append to the id. For testing purposes

### Development

You will need Python 3.7+ to run this utility as it utilities dataclasses.

 - Create a virtualenv: `python3 -m venv venv`
 - Activate the virtualenv using the appropriate activate file in the `venv/Scripts` folder
 - Install requirements: `pip install -r requirements.txt`

## DBoM To SPDX Converter
A python wrapper that can read a DBoM and convert it to a SPDX 2.1 KeyValue files (.tag) 

### Python Usage

    dbom_to_spdx.py [-h] -g GATEWAY -r REPO -c CHANNEL -a ASSET -f FILE 
    
      -h, --help            show this help message and exit
      -g GATEWAY, --gateway GATEWAY
                            The full address (with schema) at which the gateway
                            can be reached
      -r REPO, --repo REPO  The repository ID on which the channel you want to use
                            exists
      -c CHANNEL, --channel CHANNEL
                            The channel ID on which you want to retrieve the BoM
      -a ASSET, --asset ASSET
                            The asset ID on which you want to retrieve the BoM
      -f FILE, --file FILE  The SPDX KV Tag that has to be created

### Docker Usage

    mkdir output

    docker build -t dbom_to_spdx ./ -f ./dbom_to_spdx/Dockerfile

    docker run -e "GATEWAY=$GATEWAY" -e "REPO=$REPO" -e "CHANNEL=$CHANNEL" -e "FILE=$FILE" -e "ASSET=$ASSET"  -v "$(pwd)"/output:/output dbom_to_spdx
    
      GATEWAY
                            The full address (with schema) at which the gateway
                            can be reached
      REPO  The repository ID on which the channel you want to use
                            exists
      CHANNEL
                            The channel ID on which you want to retrieve the BoM
      ASSET
                            The asset ID on which you want to retrieve the BoM
      FILE                  The SPDX KV Tag that has to be created

## Getting Help

If you have any queries on spdx converter util, feel free to reach us on any of our [communication channels](https://github.com/DBOMproject/community/blob/master/COMMUNICATION.md) 

If you have questions, concerns, bug reports, etc, please file an issue in this repository's [issue tracker](https://github.com/DBOMproject/tools/issues).

## Getting Involved

Find the instructions on how you can contribute in [CONTRIBUTING](CONTRIBUTING.md).