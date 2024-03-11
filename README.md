# ParentText Goals API

Provides information about goals, modules and activities.

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

```
uvicorn parenttext_goals_webhooks.main:app --reload
```

## API docs

Documentation for the API endpoints can be found at '/docs' e.g. http://localhost:8000/docs .

## Recommended deployment process

1. Create a Pull Request that targets the 'master' branch
2. Unit tests will automatically run against the newly created PR; make sure they pass
3. It is highly recommended to ask someone to review your PR
4. If everything is ok, merge the PR.
5. Pushing to the 'master' branch will automatically run tests against the 'master' branch
6. When satisfied, [trigger a manual deployment] to the production environment


[trigger a manual deployment]: https://github.com/IDEMSInternational/parenttext-goals-webhooks/actions/workflows/deploy-manual.yml
