<p align="center">
  <img src="logo.png" alt="Logo">

  <p align="center">
    API service for BA Torment
    <br>
    <br>
    <a href="https://github.com/BeaverHouse/aecheck-data/issues">Bug Report</a>
    |
    <a href="https://github.com/BeaverHouse/aecheck-data/issues">Request</a>
  </p>

  <p align="center">
    <a href="https://fastapi.tiangolo.com/">
      <img src="https://img.shields.io/badge/FastAPI-005571?logo=fastapi&logoColor=fff&style=flat" alt="FastAPI">
    </a>
    <a href="https://www.python.org/">
      <img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
    </a>
    <a href="https://python-poetry.org/">
      <img src="https://img.shields.io/badge/Poetry-60A5FA.svg?style=flat&logo=Poetry&logoColor=white" alt="Poetry">
    </a>
    <a href="https://supabase.com/">
      <img src="https://img.shields.io/badge/Supabase-3FCF8E?logo=supabase&logoColor=fff&style=flat" alt="Supabase">
    </a>
  </p>
</p>

<!-- Content -->

<br>

## Overview

API service for [BA Torment].  
It is deployed on my Mac mini server.  
Most of the data is stored in [Oracle Object Storage] because it is static data. 
This service is used to access a small dataset in the [Supabase](https://supabase.com/) and to manage the user-uploaded YouTube links.

<br>

## History

Please see the [README of the ba-torment-batch folder](../ba-torment-batch/README.md).

## Major data reference

For main data sources, please see the [README of the ba-torment-batch folder](../ba-torment-batch/README.md).  
In addition, the user-uploaded YouTube links are stored in the PostgreSQL database.

<br>

## Prerequisites

1. You need to install [Python 3.12] and [Poetry] to manage the packages.
2. You need to set environment variables to run the script.

   ```env
   POSTGRES_HOST=
   POSTGRES_PORT=
   POSTGRES_USER=
   POSTGRES_PASSWORD=
   POSTGRES_DBNAME=
   BATORMENT_UPLOAD_URL="presigned-url-to-upload-images"
   ```

<br>

## Run the script locally

**Activate the virtual environment**

```
poetry shell
```

**Install packages**  
This will install the required packages in the whole repository.

```
poetry install
```

**Run the script**  
- You can run the FastAPI application with `uvicorn api.main:app --reload`.
- Otherwise, you can run the API service with `run.py` in the root directory.

<br>

## Contributing

See the [CONTRIBUTING.md](./CONTRIBUTING.md).

<br>
<br>

[BA Torment]: https://bluearchive-torment.netlify.app/
[Oracle Object Storage]: https://www.oracle.com/cloud/storage/object-storage/
[Poetry]: https://python-poetry.org/
[Python 3.12]: https://www.python.org/downloads/release/python-3120/
