# Abacus OAS Generator

Automatically generates OpenAPI 3.0.3 connector specifications from Abacus OData metadata.

## Features

- Parses Abacus OData metadata
- Detects business entities
- Groups entities into business domains
- Generates CRUD endpoints
- Generates reusable schemas
- Adds OAuth2 Client Credentials security
- Produces connector specific OpenAPI JSON files
- Generates Markdown documentation

## Usage

```bash
python generate.py
```

Input

```
input/swagger.json
```

Output

```
output/*.json
```
