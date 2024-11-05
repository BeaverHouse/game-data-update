<p align="center">
  <img src="logo.png" alt="Logo">

  <p align="center">
    Data processing code for AE Check
    <br>
    <br>
    <a href="https://github.com/BeaverHouse/game-data-update/issues">Bug Report</a>
    |
    <a href="https://github.com/BeaverHouse/game-data-update/issues">Request</a>
  </p>

  <p align="center">
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

Data processing code for [AE Check].  
It is processed manually on my local machine.  
The processed data is updated to the PostgreSQL database powered by [Supabase](https://supabase.com/).

<br>

## History

| **Period**        | **Description**                                                           |
| :---------------- | :------------------------------------------------------------------------ |
| 2021.02 ~ 2022.09 | Manually processed the JSON data                                          |
| 2022.09 ~ 2023.09 | Used python script to process data (v2)                                   |
| 2023.09 ~ 2024.10 | Changed the data schema, configured auto-migration via GitHub Actions (v3) |
| 2024.10 ~         | Migrated data to Supabase, deployed the backend (v3.1)                     |

## Major data reference

| **Data source** | **Description**                                       |
| :-------------- | :---------------------------------------------------- |
| Raw application | I'm using mobile emulator to extract images directly. |
| [altema.jp]     | To scrape japanese data                               |
| [AE wiki]       | To scrape english data                                |
| [Seesaa Wiki]   | For additional information                            |

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
   AECHECK_UPLOAD_URL="presigned-url-to-upload-images"
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
If you want to update the character data, run `aecheck/update.py`.  
Otherwise, if you want to compare the processed character data with the database, run `aecheck/compare.py`.

[AE Check]: https://aecheck.com/
[AE wiki]: https://anothereden.wiki/
[altema.jp]: https://altema.jp/anaden/
[Seesaa Wiki]: https://anothereden.game-info.wiki
[Poetry]: https://python-poetry.org/
[Python 3.12]: https://www.python.org/downloads/release/python-3120/

<br>

## Contributing

See the [CONTRIBUTING.md](./CONTRIBUTING.md).
