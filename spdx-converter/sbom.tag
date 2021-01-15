SPDXVersion: SPDX-2.1
DataLicense: CC0-1.0
DocumentName: ExampleDBoM
SPDXID: SPDXRef-DOCUMENT
DocumentNamespace: https://spdx.org/spdxdocs/-example-444504E0-4F89-41D3-9A0C-0305E82C3301
DocumentComment: <text>This is a sample spreadsheet</text>

## Creation Information
Creator: Person: Bob Creator
Creator: Organization: Example Inc
Creator: Tool: Jenkins Build Pipeline
Created: 2020-02-03T00:00:00Z
CreatorComment: <text>This is an example of an SPDX spreadsheet format</text>

## Review Information
Reviewer: Person: Joe Reviewer
ReviewDate: 2020-02-10T00:00:00Z
ReviewComment: <text>This has been reviewed by Joe. Joe Approves</text>

Reviewer: Person: Adam Reviewer
ReviewDate: 2020-03-13T00:00:00Z
ReviewComment: <text>Another example reviewer. Adam Approves</text>

## Annotation Information
Annotator: Person: Jim Annotator
AnnotationType: REVIEW
AnnotationDate: 2020-03-11T00:00:00Z
AnnotationComment: <text>An example annotation comment.</text>
SPDXREF: SPDXRef-45

## Package Information
PackageName: Example Package
SPDXID: SPDXRef-Example-Core-2.2.1-B45
PackageVersion: Version 2.2.1
PackageDownloadLocation: http://org1.com/example
PackageSummary: <text>Example</text>
PackageSourceInfo: <text>Version 2.2.1 of Example</text>
PackageFileName: example-2.2.1-install.iso
PackageSupplier: Organization: org1
PackageOriginator: Organization: Example Team
PackageChecksum: SHA1: 2fd4e1c67a2d28fced849ee1bb76e7391b93eb12
PackageVerificationCode: 4e3211c67a2d28fced849ee1bb76e7391b93feba (SpdxTranslatorSpdx.rdf, SpdxTranslatorSpdx.txt)
PackageDescription: <text>This package contains the bootable image for the Example</text>
PackageComment: <text>This package includes several sub-packages.</text>

PackageCopyrightText: <text> Copyright 2019,20 org1 Inc</text>

PackageLicenseDeclared: (Apache-2.0 AND MPL-1.1)
PackageLicenseConcluded: (Apache-1.0 AND Apache-2.0 AND MPL-1.1)

PackageLicenseInfoFromFiles: Apache-1.0
PackageLicenseInfoFromFiles: Apache-2.0
PackageLicenseInfoFromFiles: MPL-1.1
PackageLicenseComments: <text>The declared license information can be found in the NOTICE file at the root of the archive file</text>

ExternalRef: SECURITY cpe23Type cpe:2.3:a:pivotal_software:spring_framework:4.1.0:*:*:*:*:*:*:
ExternalRefComment: <text>NIST National Vulnerability Database (NVD) describes security vulnerabilities (CVEs) which affect Vendor Product Version acmecorp:acmenator:6.6.6.</text>

## File Information
FileName: src/org/org1/example/exec.java
SPDXID: SPDXRef-File1
FileType: SOURCE
FileChecksum: SHA1: 2fd4e1c67a2d28fced849ee1bb76e7391b93eb12
LicenseConcluded: Apache-2.0
LicenseInfoInFile: Apache-2.0
FileCopyrightText: <text>Copyright 2010, 2011 Source Auditor Inc.</text>

FileName: Test-2.6.3/test-2.6.3-sources.jar
SPDXID: SPDXRef-File2
FileType: ARCHIVE
FileChecksum: SHA1: 3ab4e1c67a2d28fced849ee1bb76e7391b93f125
LicenseConcluded: Apache-1.0
LicenseInfoInFile: Apache-1.0
LicenseComments: <text>This license is used by Jena</text>
FileCopyrightText: <text>(c) Copyright 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009 Hewlett-Packard Development Company, LP</text>
ArtifactOfProjectName: Jena
ArtifactOfProjectHomePage: http://www.openjena.org/
ArtifactOfProjectURI: UNKNOWN
FileComment: <text>This file belongs to Jena</text>

## Snippet Information
SnippetSPDXID: SPDXRef-Snippet
SnippetFromFileSPDXID: SPDXRef-DoapSource
SnippetLicenseComments: <text>The concluded license was taken from package xyz, from which the snippet was copied into the current file. The concluded license information was found in the COPYING.txt file in package xyz.</text>
SnippetCopyrightText: <text> Copyright 2008-2010 John Smith </text>
SnippetComment: <text>This snippet was identified as significant and highlighted in this Apache-2.0 file, when a commercial scanner identified it as being derived from file foo.c in package xyz which is licensed under GPL-2.0-or-later.</text>
SnippetName: from linux kernel
SnippetLicenseConcluded: Apache-2.0
LicenseInfoInSnippet: Apache-2.0
