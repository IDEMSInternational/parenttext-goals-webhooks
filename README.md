# ParentText Goals Webhooks

Webhooks for parent text to compose lists of goals and
modules satisfying certain criteria.

## Setup

### Development

`pip install -r requirements.txt`

To run tests: `python -m unittest`

### Deployment on Google Cloud Platform

- Install `gcloud`:
    - https://cloud.google.com/sdk/docs/install
    - https://cloud.google.com/sdk/docs/initializing
- Ensure you have access to the correct GCP project
    (IDEMS General, a.k.a `glossy-attic-237012`)
    - Including permissions to deploy cloud functions
- Run `deploy.sh`
    - On windows, you may have to create a batch file containing something like

    ```
    gcloud config set project glossy-attic-237012
    gcloud functions deploy parenttext-individualize-module-list \
    --gen2 \
    --region=europe-west2 \
    --runtime=python311 \
    --source=. \
    --entry-point=serve \
    --trigger-http
    ```

    Also see: https://cloud.google.com/functions/docs/deploy

## Recommended Deployment Process

After making any changes, it is recommended to run tests to ensure
nothing is broken.

1. Run tests: `python -m unittest`. This runs
    - `tests.py`: Functionality tests with `test_data`
    - `test_integrity.py`: Runs integrity checks for the data in the `data` folder
2. Run `./deploy-testing.sh` to deploy to testing server
3. Execute `python run_webhooks.py --testing` and ensure that all calls succeed
4. Run `./deploy.sh` to deploy to production server
5. Execute `python run_webhooks.py` and ensure that all calls succeed

## Functionality

https://docs.google.com/document/d/1so5KrKuHwFyoLVpis2isWIh2eo0n4f90dPeqVIaKMqw/edit

Each webhook returns a json with the main results in the `text` field.

Query URLs support the following paths:

### `get_goals_list`: #1 from above

Get list of goal IDs, filtered by `filter_expression` and sorted by `sort_columns`.

**Example.**

Input:

```
{
    "filter_expression": "'no' in relationship"
}
```

Output:

```
{"text" : "relation develop learning structure behave safety budget wellbeing"}
```

### `get_modules_list`: #2 from above

Description: see [here](https://docs.google.com/document/d/1so5KrKuHwFyoLVpis2isWIh2eo0n4f90dPeqVIaKMqw/edit)

**Example.**

Input:

```
{
    "goal_id_column": "goal_id_c",
    "goal_priority_column": "priority_in_goal_c",
    "goal_id": "relation",
    "filter_expression": "'female' in child_gender and 7 in age",
    "sort_columns": ["priority_in_topic"]
}
```

Output:

```
{"text" : "one_on_one_yc kind_to_myself_yc give_praise_yc talk_feelings_yc spirituality_yc"}
```

### `get_goal_name`: #3 from above

Given an ID of a goal, and a language and column, look up the translated name in the respective column.

**Example.**

Input:

```
{
    "column": "name_c",
    "language": "eng",
    "id": "safety"
}
```

Output:

```
{"text" : "Keep My Child Safe & Healthy"}
```

### `get_module_name`: #4 from above

Given an ID of a module, and a language and column, look up the translated name in the respective column.

**Example.**

Input:

```
{
    "column": "name",
    "language": "zul",
    "id": "take_a_pause"
}
```
Output:

```
{"text" : "yyy"}
```

### `get_numbered_goal_names`: #6 from above

Given a space separated list of ID of goals, and a language and column, look up the translated name in the respective column, and produce a numbered list of the names.

**Example.**

Input:

```
{
    "column": "name_c",
    "language": "eng",
    "ids": "safety learning develop"
}
```

Output:

```
{"text" : "1. Keep My Child Safe & Healthy\n2. Prepare My Child for Success in School\n3. Support My Child's Development"}
```

### `get_numbered_module_names`: #7 from above

Given a space separated list of ID of modules, and a language and column, look up the translated name in the respective column, and produce a numbered list of the names.

**Example.**

Input:

```
{
    "column": "name",
    "language": "eng",
    "ids": "take_a_pause one_on_one_yc"
}
```

Output:

```
{"text" : "1. xxx\n2. One on One"}
```

### `get_ltp_activities_list`: #5 from above

Get list of LTP activity IDs, filtered by `filter_expression` and sorted by `sort_columns`.

**Example.**

Input:

```
{
    "filter_expression": "'Calm' in act_type and 17 in act_age"
}
```

Output:

```
{"text" : "friendly_chat reflect_positive checkin_chat"}
```

For up-to-date examples, see `tests.py`
