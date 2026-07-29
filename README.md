# Advisory Feed Demo

## Setup
1) Install [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
2) Run `conda env create -f environment.yml`
3) Run `conda activate advisory-feed-demo`
4) Run `cp example.env .env`
5) Create [service account token](https://www.anaconda.com/docs/anaconda-platform/admin/service-accounts)
6) Copy service account CLIENT_ID and CLIENT_SECRET to `.env` file
7) Run `alembic upgrade head` to create the database schema

## Usage

### Pull From Advisory Feed
1) Ensure that environment is activated `conda activate advisory-feed-demo`
2) Run `python main.py`

Each run will use the latest watermark out of previous runs

### Query Results
1) Run `sqlite3 advisories.db`
2) Run any sql query e.g. `select advisory_id from advisories;`
