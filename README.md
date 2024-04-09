# ParentText Goals API

Provides information about goals, modules and activities.

# Getting started

```
# Clone this repository.
git clone https://github.com/IDEMSInternational/parenttext-goals-webhooks.git

# Change into the project dir
cd parenttext-goals-webhooks

# Copy the example environment variables file
cp env.example .env

# Build the app container
docker compose build

# Run the app
docker compose up -d
```

View the API docs in your browser at http://localhost:8000/docs .

# Settings

The API is configured via environment variables.

- `REPO_URL`: URL of git repository containing data files
- `REPO_REF`: Reference to repository branch or tag to use
- `REPO_PATH`: Path from repository root where data files are located. Defaults to repository root.
- `CONFIG_FILE`: Name of main data file. Defaults to 'api.json'.
- `CSV_MODE`: Indicates that data files are in CSV format. Enable by setting value to 'on'. Defaults to 'off'.

## Data from Git repository

Files must be in JSON format. Set `REPO_URL` and `REPO_REF` as a minimum. The specified repository will be shallow cloned at the specified ref. The [main data file] will be loaded from `REPO_PATH`/`CONFIG_FILE`.

## Data from local filesystem

Files can be in JSON or CSV format. Files will be loaded from a directory called 'data' in the same directory that the app is running from. In the docker container, this will be located at '/opt/idems/api/data'.

JSON mode is the default. The [main data file] must be called 'api.json'.

CSV mode can be enabled via the `CSV_MODE` setting. A main data file is not required, instead, four CSV files need to be present in the data directory.

- goal\_data.csv
- goal\_topic\_data.csv
- ltp\_activities\.csv
- module\_data\.csv

CSV mode is provided for backward compatibility and should be considered deprecated. Use JSON format data files instead.

# Main data file

The purpose of this file is to locate other data files that the app needs to load. See the [example api.json](data/api.json) for reference.

There must be a sheet called "goals\_api\_sources". Each source must define the following keys.

- `book`: location of data file relative to main data file
- `model`: name of data model to populate
- `resource`: name of the resource this source applies to; can be one of `goals`, `goal_topic_links`, `ltp_activities` or `modules`
- `sheet`: name of sheet, within the book, to load data from

There should be at least one source for each resource type. If more than one source exists for a particular resource, the data from each source will be concatenated.

# Development

## Setup

Clone this repository.

Setup a Python virtual environment and install dependencies.
```
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e '.[dev]'
```

## Test

```
python -m unittest
```

## Run

Create env file.
```
cp env.example .env
```

Start.
```
env $(cat .env) uvicorn parenttext_goals_webhooks.main:app --reload
```

## API docs

Documentation for the API endpoints can be found at '/docs' e.g. http://localhost:8000/docs .


[main data file]: #main-data-file
