<p align="center">
  <img src="logo.png" alt="Logo">

  <p align="center">
    Data processing code for BA Torment
    <br>
    <br>
    <a href="https://github.com/BeaverHouse/aecheck-data/issues">Bug Report</a>
    |
    <a href="https://github.com/BeaverHouse/aecheck-data/issues">Request</a>
  </p>

  <p align="center">
    <a href="https://www.python.org/">
      <img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
    </a>
    <a href="https://python-poetry.org/">
      <img src="https://img.shields.io/badge/Poetry-60A5FA.svg?style=flat&logo=Poetry&logoColor=white" alt="Poetry">
    </a>
    <a href="https://pola.rs/">
      <img src="https://img.shields.io/badge/Polars-CD792C?logo=polars&logoColor=fff&style=flat" alt="Polars">
    </a>
    <a href="https://supabase.com/">
      <img src="https://img.shields.io/badge/Supabase-3FCF8E?logo=supabase&logoColor=fff&style=flat" alt="Supabase">
    </a>
  </p>
</p>

<!-- Content -->

<br>

## Overview

Data processing code for [BA Torment].  
It is processed on my local machine in schedule.  
Most of the processed data is updated to the [Oracle Object Storage], and the rest is updated to the PostgreSQL database powered by [Supabase](https://supabase.com/).

<br>

## History

| **Period**        | **Description**                                                                                   |
| :---------------- | :------------------------------------------------------------------------------------------------ |
| 2023.07 ~ 2024.03 | Used python script to process data                                                                |
| 2024.03 ~ 2024.10 | Extended the data schema to serve more information,<br>configured auto-migration via GitHub Actions |
| 2024.10 ~         | Migrated data to Oracle Object Storage & Supabase,<br>deployed the backend                         |

## Major data reference

| **Data source**      | **Description**                                   |
| :------------------- | :------------------------------------------------ |
| [Schale DB]          | To extract character data                         |
| [info.herdatasam.me] | To extract party data                             |
| [Arona.AI] [^1]      | To validate the data + get additional information |

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
If you want to run the script manually, run `ba-torment-batch/main.py`.

<br>

## Contributing

See the [CONTRIBUTING.md](./CONTRIBUTING.md).

<br>
<br>

[^1]: The developer of [Arona.AI] is same as the developer of [info.herdatasam.me].

[BA Torment]: https://bluearchive-torment.netlify.app/
[Oracle Object Storage]: https://www.oracle.com/cloud/storage/object-storage/
[Schale DB]: https://schaledb.com/
[info.herdatasam.me]: https://storage.googleapis.com/info.herdatasam.me
[Arona.AI]: https://arona.ai/
[Poetry]: https://python-poetry.org/
[Python 3.12]: https://www.python.org/downloads/release/python-3120/
