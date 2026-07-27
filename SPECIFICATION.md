# Abacus OAS Generator

## Project Overview

The objective of this project is to build a generic OpenAPI 3.0.3 generator that converts OData metadata (JSON CSDL format) into enterprise-grade OpenAPI connector specifications.

The first implementation target is the Abacus API metadata.

The generated OpenAPI specifications must be compatible with Seeburger Integration Workbench (IWS).

The generator must also be generic enough to support additional OData providers in the future.

Examples:

- Abacus
- SAP
- Microsoft Dynamics
- Business Central
- Custom OData Services

---

# Objectives

The generator shall:

- Read OData Metadata JSON
- Detect all entity definitions
- Detect complex types
- Detect enums
- Detect navigation properties
- Detect collections
- Build an internal metadata model
- Automatically classify business entities into connector domains
- Generate reusable OpenAPI schemas
- Generate CRUD endpoints
- Generate OAuth2 security
- Generate reusable components
- Generate Markdown documentation
- Write one OpenAPI specification per connector

---

# Target Output

The output folder shall contain

```
output/

Authentication.json

BusinessPartners.json

FinancialAccounting.json

AccountsReceivable.json

AccountsPayable.json

Payroll.json

Projects.json

Documents.json

Payments.json

Reporting.json

Authentication.md

BusinessPartners.md

...
```

---

# Technology

Language

Python 3.12+

Libraries

- orjson
- click
- rich
- inflect
- pyyaml
- jsonschema
- networkx
- jinja2

OpenAPI Version

3.0.3

Authentication

OAuth2 Client Credentials

Output

JSON

---

# Folder Structure

```
abacus-oas-generator

input/
    swagger.json

output/

templates/

src/

tests/

generate.py

requirements.txt

README.md

SPECIFICATION.md
```

---

# High Level Architecture

```
              swagger.json
                     │
                     ▼
             Metadata Parser
                     │
                     ▼
             Internal Model
                     │
         ┌───────────┴────────────┐
         ▼                        ▼
 Entity Classifier         Schema Builder
         │                        │
         └──────────┬─────────────┘
                    ▼
              Path Builder
                    │
                    ▼
           OpenAPI Builder
                    │
                    ▼
          Markdown Builder
                    │
                    ▼
                Output Files
```

---

# Source Modules

The project shall contain the following modules.

parser.py

Responsible for reading OData metadata and producing the internal metadata model.

classifier.py

Responsible for grouping entities into business connector domains.

schema_builder.py

Responsible for converting metadata entities into reusable OpenAPI schemas.

path_builder.py

Responsible for generating CRUD endpoints.

oauth_builder.py

Responsible for creating reusable OAuth2 Client Credentials security.

openapi_builder.py

Responsible for combining schemas, paths, security and metadata into a valid OpenAPI specification.

markdown_builder.py

Responsible for generating connector documentation.

generator.py

Coordinates the generation of connector files.

models.py

Contains all internal data classes used by the generator.

utils.py

Contains reusable helper methods.

---

# Design Principles

The generator must

- be provider independent
- never hardcode Abacus entities
- use reusable builders
- separate parsing from generation
- never duplicate schemas
- use reusable OpenAPI components
- generate deterministic output
- produce valid OpenAPI 3.0.3
- remain easily extensible
# Internal Data Model

The generator shall convert the source metadata into an internal object model before any OpenAPI generation begins.

No OpenAPI logic shall exist inside the parser.

The parser shall only produce an in-memory representation of the metadata.

---

## Metadata

The Metadata object represents the complete parsed OData model.

Properties

- providerName
- providerVersion
- namespaces
- entities
- complexTypes
- enums
- entitySets
- navigationProperties
- functions
- actions

---

## Entity

Represents one business object.

Properties

- name
- fullName
- namespace
- description
- entitySet
- keyProperty
- properties
- navigationProperties
- annotations

---

## Property

Represents one entity property.

Properties

- name
- type
- nullable
- collection
- reference
- defaultValue
- maxLength
- precision
- scale
- description

---

## Enum

Represents one enumeration.

Properties

- name
- namespace
- values

---

## Complex Type

Represents embedded reusable objects.

Examples

Address

Dimensions

Currency

PaymentInformation

Complex types shall never generate REST endpoints.

They only generate reusable schemas.

---

## Navigation Property

Represents relationships.

Properties

- name
- targetEntity
- collection
- nullable

Navigation properties are used only when generating schemas.

They shall not automatically generate REST endpoints.

---

# Parser

The Metadata Parser is responsible only for reading metadata.

It shall not generate OpenAPI.

It shall not classify business domains.

It shall not build schemas.

Its responsibilities are

- Read JSON
- Parse definitions
- Detect entities
- Detect complex types
- Detect enums
- Detect navigation properties
- Detect collections
- Detect inheritance
- Build Metadata object

---

## Parser Workflow

Input

```
swagger.json
```

↓

Load JSON

↓

Locate definitions

↓

Iterate over every definition

↓

Determine object type

↓

Create object model

↓

Return Metadata

---

# Object Detection Rules

If a definition contains

```
enum
```

↓

Create Enum

---

If a definition contains

```
properties
```

↓

Candidate Entity

Further inspection is required.

---

If a definition contains

```
allOf
```

↓

Resolve inheritance

Merge inherited properties.

---

If a definition references another definition

```
$ref
```

↓

Create reference property.

---

If property type is

```
array
```

↓

Mark property as Collection.

---

# Entity Detection

Not every definition is a REST entity.

The classifier shall distinguish between

Business Entity

Complex Type

Value Object

Embedded Object

Enum

Helper Type

The parser shall only mark them as candidates.

The classifier will make the final decision.

---

# Type Mapping

Primitive OData types shall map to OpenAPI.

Examples

Edm.String

↓

string

Edm.Boolean

↓

boolean

Edm.Int32

↓

integer

Edm.Int64

↓

integer

format: int64

Edm.Decimal

↓

number

Edm.Double

↓

number

Edm.Date

↓

string

format: date

Edm.DateTimeOffset

↓

string

format: date-time

Edm.Guid

↓

string

format: uuid

Edm.Binary

↓

string

format: binary

---

# Logging

The parser shall log

Metadata loaded

Definitions discovered

Entities discovered

Enums discovered

Complex Types discovered

Navigation properties discovered

Collections discovered

Warnings

Errors

---

# Validation

The parser shall validate

Definition names are unique.

Property names are unique.

References exist.

No circular inheritance.

Unknown primitive types shall produce warnings.

Generation shall continue whenever possible.

---

# Error Handling

The parser shall never terminate because one definition is invalid.

Invalid definitions shall be skipped.

Errors shall be logged.

Generation shall continue.

At the end a summary shall be displayed.

Example

Definitions processed

1572

Entities

640

Complex Types

221

Enums

37

Warnings

3

Errors

0
# Business Domain Classification

## Overview

The Domain Classifier is responsible for grouping REST entities into logical business connectors.

The objective is to keep every generated connector reasonably sized while maintaining strong business cohesion.

The classifier shall work for Abacus and remain configurable for future providers.

---

# Responsibilities

The classifier shall

- Analyse every entity
- Ignore complex types
- Ignore enums
- Ignore helper objects
- Ignore embedded value objects
- Detect business entities
- Assign every business entity to exactly one connector
- Produce deterministic output

---

# Connector Definitions

The initial connector set shall contain

Authentication

BusinessPartners

FinancialAccounting

AccountsReceivable

AccountsPayable

Payroll

Projects

Documents

Payments

Reporting

Unknown

No entity shall remain unclassified.

Unknown entities shall be placed inside the Unknown connector.

---

# Classification Strategy

Classification shall follow multiple stages.

Stage 1

Explicit Rules

↓

Stage 2

Namespace Rules

↓

Stage 3

Name Rules

↓

Stage 4

Relationship Analysis

↓

Stage 5

Fallback

---

# Explicit Rules

Configuration shall support explicit mappings.

Example

Customer

↓

BusinessPartners

Vendor

↓

BusinessPartners

Employee

↓

Payroll

Invoice

↓

AccountsReceivable

SupplierInvoice

↓

AccountsPayable

---

# Namespace Rules

If namespaces indicate a business module they should be preferred.

Examples

crm

↓

BusinessPartners

finance

↓

FinancialAccounting

payroll

↓

Payroll

project

↓

Projects

document

↓

Documents

payment

↓

Payments

---

# Name Rules

The classifier shall analyse entity names.

Contains

Customer

↓

BusinessPartners

Contains

Supplier

↓

BusinessPartners

Contains

Vendor

↓

BusinessPartners

Contains

Employee

↓

Payroll

Contains

Salary

↓

Payroll

Contains

Payroll

↓

Payroll

Contains

Invoice

↓

AccountsReceivable

Contains

CustomerInvoice

↓

AccountsReceivable

Contains

VendorInvoice

↓

AccountsPayable

Contains

PurchaseInvoice

↓

AccountsPayable

Contains

Project

↓

Projects

Contains

Activity

↓

Projects

Contains

TimeEntry

↓

Projects

Contains

Document

↓

Documents

Contains

Attachment

↓

Documents

Contains

Payment

↓

Payments

Contains

Journal

↓

FinancialAccounting

Contains

Ledger

↓

FinancialAccounting

Contains

Account

↓

FinancialAccounting

Contains

Currency

↓

FinancialAccounting

Contains

Tax

↓

FinancialAccounting

Contains

Report

↓

Reporting

Contains

Statistics

↓

Reporting

Contains

Dashboard

↓

Reporting

---

# Relationship Analysis

Relationships improve classification.

Example

CustomerAddress

references

Customer

↓

BusinessPartners

Example

InvoiceLine

references

Invoice

↓

AccountsReceivable

Example

SalaryLine

references

Salary

↓

Payroll

If parent entity already belongs to a connector

child entities should inherit that connector.

---

# Embedded Objects

Objects used only by one entity

shall never become REST endpoints.

Instead

they become reusable schemas.

Examples

Address

Coordinates

ContactInformation

PaymentTerms

ReminderConfiguration

CreditLimit

---

# Business Entity Rules

An object becomes a REST entity when

it has an identifier

AND

contains multiple business fields

AND

can logically exist independently

Examples

Customer

YES

Invoice

YES

Payment

YES

Project

YES

Employee

YES

Address

NO

CurrencyAmount

NO

ReminderSettings

NO

CreditLimit

NO

TaxRate

Depends on metadata

---

# Classification Confidence

Every classification shall receive a confidence score.

100

Explicit Rule

90

Namespace Match

80

Relationship Match

70

Name Match

50

Fallback

This allows future improvements.

---

# Unknown Connector

If no classification rule matches

the entity shall be assigned to

Unknown

Generation must continue.

---

# Output

The classifier shall produce

Connector

↓

Entity List

Example

BusinessPartners

Customer

Supplier

AddressBook

CustomerContact

VendorContact

FinancialAccounting

Ledger

Journal

Account

Currency

ExchangeRate

Payroll

Employee

PayrollRun

Salary

SalaryLine

EmployeeContract

Projects

Project

ProjectTask

TimeEntry

Milestone

Documents

Document

Attachment

Folder

Payments

Payment

PaymentBatch

PaymentMethod

Reporting

Report

Dashboard

Statistics

---

# Logging

The classifier shall display

Business entities detected

Connector count

Entities per connector

Unknown entities

Confidence summary

Example

BusinessPartners

84

FinancialAccounting

67

Payroll

52

Projects

48

Unknown

6

Classification completed successfully.
# Schema Builder

## Overview

The Schema Builder converts parsed metadata entities into reusable OpenAPI 3.0.3 schemas.

The Schema Builder shall never generate REST endpoints.

Its only responsibility is creating OpenAPI schemas.

---

# Responsibilities

The Schema Builder shall

- Generate reusable schemas
- Generate enums
- Generate complex types
- Resolve inheritance
- Resolve references
- Resolve collections
- Generate examples where possible
- Generate descriptions
- Remove duplicate schemas
- Prevent circular references

---

# Output

Every connector shall contain

components

↓

schemas

Example

components

  schemas

      Customer

      CustomerAddress

      CustomerInvoice

      Currency

      Payment

      Employee

---

# Primitive Type Mapping

The following OData primitive types shall map to OpenAPI.

Edm.String

↓

type: string

----------------------------------

Edm.Boolean

↓

type: boolean

----------------------------------

Edm.Int16

↓

type: integer

format: int32

----------------------------------

Edm.Int32

↓

type: integer

format: int32

----------------------------------

Edm.Int64

↓

type: integer

format: int64

----------------------------------

Edm.Decimal

↓

type: number

format: double

----------------------------------

Edm.Double

↓

type: number

format: double

----------------------------------

Edm.Single

↓

type: number

format: float

----------------------------------

Edm.Guid

↓

type: string

format: uuid

----------------------------------

Edm.Binary

↓

type: string

format: binary

----------------------------------

Edm.Date

↓

type: string

format: date

----------------------------------

Edm.DateTimeOffset

↓

type: string

format: date-time

----------------------------------

Edm.TimeOfDay

↓

type: string

format: time

----------------------------------

Edm.Duration

↓

type: string

---

# Nullable Fields

Nullable properties

↓

nullable: true

Non-nullable properties

↓

required

Example

CustomerName

nullable = false

↓

required

---

# Required Properties

The Schema Builder shall automatically build the required array.

Example

Customer

↓

required

- Id
- Name

---

# Collections

Collection properties shall become arrays.

Example

Invoices

↓

type: array

items

$ref

CustomerInvoice

---

# References

Entity references shall use reusable schemas.

Never duplicate schema definitions.

Correct

Customer

↓

Address

↓

$ref

Incorrect

Customer

↓

Address copied inline

---

# Enum Generation

Metadata enums shall become OpenAPI enums.

Example

Status

↓

type: string

enum

Active

Inactive

Blocked

Deleted

---

# Complex Types

Complex types shall generate reusable schemas.

They shall never generate REST endpoints.

Example

Address

↓

components.schemas.Address

---

# Inheritance

If metadata contains inheritance

allOf

↓

OpenAPI allOf

Example

Customer

extends

BusinessPartner

↓

Customer

allOf

BusinessPartner

Customer Properties

---

# Circular References

Circular references shall never cause infinite recursion.

Example

Customer

↓

Orders

↓

Customer

Use reusable

$ref

instead of recursive expansion.

---

# Duplicate Schemas

If two entities generate identical schemas

reuse

the first schema.

Never create duplicate definitions.

---

# Naming Rules

Schema names shall be

PascalCase

Remove namespace prefixes.

Correct

CustomerInvoice

Incorrect

ch.abacus.debi.CustomerInvoice

---

# Property Naming

Property names shall remain unchanged.

Do not convert to camelCase.

Do not rename metadata fields.

---

# Descriptions

Every schema shall include

title

description

Example

Customer

title

Customer

description

Represents a customer business entity.

Descriptions should be generated automatically based on metadata where available.

If no description exists

generate one.

---

# Examples

Example values should be generated for primitive properties.

Example

Id

1

Name

Example Customer

Email

john@example.com

Active

true

CreatedOn

2026-01-01T10:00:00Z

Examples are optional but recommended.

---

# ReadOnly Fields

System-managed fields

should be

readOnly

Examples

CreatedOn

CreatedBy

ModifiedOn

ModifiedBy

Version

ETag

---

# WriteOnly Fields

Sensitive fields

shall become

writeOnly

Examples

Password

Secret

AccessToken

ClientSecret

---

# Additional Properties

Generated schemas shall include

additionalProperties: false

unless metadata explicitly allows dynamic properties.

---

# Schema Validation

Every generated schema shall be valid according to

OpenAPI 3.0.3

The generator shall validate schemas before writing output.

Invalid schemas shall be logged.

Generation shall continue where possible.

---

# Schema Builder Logging

Display

Schemas Generated

Enums Generated

Complex Types

References

Collections

Duplicates Removed

Example

Schemas

184

Enums

31

Complex Types

62

Collections

95

Duplicate Schemas Removed

18

Validation Errors

0

---

# Final Output Example

components

  schemas

      Customer

      CustomerAddress

      CustomerInvoice

      Currency

      Employee

      Payment

      Journal

      Ledger

      Project

      Document

All schemas shall be reusable through

$ref

No inline duplication shall exist.
# Path Builder

## Overview

The Path Builder is responsible for generating REST endpoints for business entities.

The Path Builder shall never generate schemas.

It shall consume the classified entities and generate OpenAPI path definitions.

The generated endpoints shall follow OData REST conventions while remaining OpenAPI 3.0.3 compliant.

---

# Responsibilities

The Path Builder shall

- Generate CRUD endpoints
- Generate operationIds
- Generate tags
- Generate request bodies
- Generate responses
- Generate reusable parameters
- Generate query parameters
- Generate pagination parameters
- Generate standard error responses
- Generate security requirements

---

# Endpoint Generation

Every business entity shall generate the following endpoints.

Collection

GET

POST

Item

GET

PATCH

DELETE

Example

Customer

↓

GET

/Customers

POST

/Customers

GET

/Customers/{id}

PATCH

/Customers/{id}

DELETE

/Customers/{id}

---

# Optional Operations

If enabled by configuration

PUT

HEAD

OPTIONS

MERGE

may also be generated.

Default

Only

GET

POST

PATCH

DELETE

---

# Path Naming

Entity names shall be converted to Entity Sets.

Examples

Customer

↓

Customers

Employee

↓

Employees

Project

↓

Projects

Company

↓

Companies

Currency

↓

Currencies

The generator shall use a pluralization engine instead of hardcoded rules.

---

# Path Parameters

Single-resource operations shall include

{id}

Example

/Customers/{id}

Parameter

name

id

in

path

required

true

schema

type

string

---

# Query Parameters

Collection endpoints shall support OData query parameters.

Include

$select

$filter

$orderby

$top

$skip

$count

$expand

$search

Example

GET

/Customers?$filter=Status eq 'Active'

These parameters shall be reusable components.

---

# Pagination

Collection endpoints shall support

$top

$skip

$count

Response examples shall include pagination metadata where appropriate.

---

# Operation IDs

Operation IDs shall be deterministic.

Examples

getCustomers

createCustomer

getCustomer

updateCustomer

deleteCustomer

Never generate duplicate operationIds.

---

# Tags

Each endpoint shall contain exactly one tag.

Examples

BusinessPartners

FinancialAccounting

Payroll

Projects

Documents

Payments

Reporting

Tags shall match connector names.

---

# Request Bodies

POST

PATCH

PUT

shall use reusable request body schemas.

Example

CustomerCreateRequest

CustomerUpdateRequest

These may initially reference the main entity schema.

---

# Responses

Standard responses shall be generated.

GET Collection

200

GET Item

200

POST

201

PATCH

200

DELETE

204

Common error responses

400

401

403

404

409

429

500

Reusable responses shall be placed in

components.responses

---

# Response Schemas

GET Collection

↓

Array of entity schema

GET Item

↓

Single entity schema

POST

↓

Created entity

PATCH

↓

Updated entity

DELETE

↓

No Content

---

# Security

Every endpoint shall require OAuth2 Client Credentials.

security

- oauth2ClientCredentials

Authentication shall be inherited from components.securitySchemes.

---

# Headers

Reusable headers

Location

ETag

Request-Id

Correlation-Id

Retry-After

shall be generated where appropriate.

---

# Content Types

Supported request content types

application/json

Supported response content types

application/json

---

# Batch Operations

If enabled

Generate

POST

/$batch

using multipart/mixed.

Batch support shall be configurable.

Default

Disabled.

---

# OData Metadata Endpoints

Optionally generate

GET

/$metadata

GET

/

These endpoints shall be disabled by default.

---

# Navigation Properties

Navigation properties shall not automatically generate REST endpoints.

Instead

they shall be referenced using

$expand

Future versions may optionally expose navigation endpoints.

---

# Filtering Support

Collection endpoints shall advertise support for

$filter

using OpenAPI parameter definitions.

Examples

Status eq 'Active'

CreatedOn gt 2026-01-01

Amount gt 1000

---

# Sorting Support

Support

$orderby

Examples

Name asc

CreatedOn desc

---

# Projection

Support

$select

Examples

$select=Id,Name

---

# Expansion

Support

$expand

Examples

$expand=Addresses

$expand=Invoices

---

# Search

Support

$search

when supported by provider.

Default

Generate parameter but mark as optional.

---

# Error Model

Generate reusable schema

ApiError

Properties

code

message

details

target

traceId

All error responses shall reference this schema.

---

# Components

The Path Builder shall reuse

Parameters

Responses

Headers

RequestBodies

Schemas

Security

Never duplicate components.

---

# Logging

Display

Paths Generated

Operations Generated

Collection Endpoints

Item Endpoints

Reusable Parameters

Reusable Responses

Example

Entities

84

Paths

168

Operations

420

Parameters

8

Responses

7

Validation Errors

0

---

# Validation

Validate

Unique paths

Unique operationIds

Valid parameter references

Valid schema references

Valid response references

Generation shall continue even if one entity fails.

Failures shall be logged.

---

# Example Output

Customer

↓

GET     /Customers

POST    /Customers

GET     /Customers/{id}

PATCH   /Customers/{id}

DELETE  /Customers/{id}

CustomerInvoice

↓

GET     /CustomerInvoices

POST    /CustomerInvoices

GET     /CustomerInvoices/{id}

PATCH   /CustomerInvoices/{id}

DELETE  /CustomerInvoices/{id}

The generated OpenAPI shall be valid according to the OpenAPI 3.0.3 specification and ready for Seeburger IWS import.
# OAuth Builder

## Overview

The OAuth Builder is responsible for generating reusable OpenAPI security schemes.

The initial implementation shall support OAuth2 Client Credentials.

The design shall allow future authentication providers without changing the OpenAPI Builder.

---

## Supported Authentication

OAuth2 Client Credentials

API Key (future)

Basic Authentication (future)

Bearer Token (future)

Azure AD (future)

OpenID Connect (future)

---

## OAuth Configuration

The generated connector shall include

components

  securitySchemes

      oauth2ClientCredentials

Flow

Client Credentials

Token URL

https://{host}/oauth/token

Scopes

api.read

api.write

api.admin

The Token URL shall be configurable.

---

## Global Security

Every generated connector shall include

security

- oauth2ClientCredentials

Endpoints may override security when necessary.

---

# OpenAPI Builder

## Responsibilities

The OpenAPI Builder combines

Info

Servers

Tags

Paths

Schemas

Security

Responses

Parameters

Headers

Request Bodies

into one valid OpenAPI document.

---

## OpenAPI Version

Generate

OpenAPI 3.0.3

---

## Info Object

Generate

title

description

version

contact

license

Connector descriptions shall be generated automatically.

---

## Servers

Default server

https://{abacus-instance}

Use server variables.

Never hardcode production URLs.

---

## Tags

Generate one tag per connector.

Example

BusinessPartners

FinancialAccounting

Payroll

Projects

Payments

Documents

Reporting

---

## Components

Generate reusable

Schemas

Parameters

Headers

Responses

Request Bodies

Security Schemes

Never duplicate components.

---

## Validation

Validate generated OpenAPI using

OpenAPI 3.0.3

JSON Schema

Invalid connectors shall not be written.

---

# Markdown Builder

## Responsibilities

Generate one Markdown document for every connector.

The structure shall match the Azure DevOps connector documentation.

---

## Markdown Template

Each document shall contain

### Description

### Supported Functions

### General Information

### Prerequisites

### Configuration

### Authentication

### Additional Resources

The documentation shall be generated automatically from connector metadata.

---

# Generator

## Responsibilities

The Generator coordinates the complete workflow.

Pipeline

Read Metadata

↓

Parse

↓

Classify

↓

Generate Schemas

↓

Generate Paths

↓

Generate OAuth

↓

Generate OpenAPI

↓

Generate Markdown

↓

Validate

↓

Write Files

---

## Output

Each connector shall generate

OpenAPI JSON

Markdown Documentation

Generation Report

---

# CLI

The application shall provide the following command.

python generate.py

Optional parameters

--input

--output

--provider

--verbose

--connector

Examples

python generate.py

python generate.py --connector Payroll

python generate.py --provider Abacus

python generate.py --output output

---

# Logging

Use Rich logging.

Display progress.

Example

Loading Metadata

✓ Completed

Definitions

1572

Business Entities

643

Complex Types

221

Enums

37

Generating Connectors

BusinessPartners

✓

FinancialAccounting

✓

Payroll

✓

Projects

✓

Validation

✓

Finished

---

# Performance

Target metadata size

10,000 definitions

Generation Time

Less than 60 seconds

Memory Usage

Less than 1 GB

---

# Testing

Unit Tests

Parser

Classifier

Schema Builder

Path Builder

OAuth Builder

OpenAPI Builder

Markdown Builder

Generator

Integration Tests

Generate complete connector library.

Validate every OpenAPI file.

Validate every Markdown file.

---

# Error Handling

Generation shall continue whenever possible.

Every error shall be logged.

Failures in one connector shall not stop remaining connectors.

---

# Extensibility

The architecture shall support future providers.

Examples

Abacus

SAP

Business Central

Dynamics 365

Oracle ERP

NetSuite

Custom OData Services

No provider-specific logic shall exist outside provider configuration.

---

# Code Quality

Use

Python Type Hints

Dataclasses

PEP8

SOLID Principles

Reusable Components

Dependency Injection where appropriate

Small focused classes

Comprehensive docstrings

---

# Deliverables

The completed project shall generate

OpenAPI 3.0.3 JSON connector specifications

Markdown connector documentation

Generation reports

Reusable components

OAuth2 Client Credentials security

The output shall be compatible with Seeburger Integration Workbench (IWS).

---

# Acceptance Criteria

The project is considered complete when

✓ Metadata parses successfully

✓ Business entities are classified correctly

✓ OpenAPI validates successfully

✓ OAuth security is generated

✓ CRUD endpoints are generated

✓ Markdown documentation is generated

✓ Connector JSON imports into Seeburger IWS

✓ Generated connectors require no manual editing

✓ The generator supports future OData providers through configuration

End of Specification
