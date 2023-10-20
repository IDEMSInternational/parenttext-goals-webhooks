# ParentText Goals Webhooks

A chatbot for recording climate data in a database.

## Functionality

https://docs.google.com/document/d/1so5KrKuHwFyoLVpis2isWIh2eo0n4f90dPeqVIaKMqw/edit

Each webhook returns a json with the main results in the `text` field.

Query URLs support the following paths:

- `get_goals_list`: #1 from above

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

- `get_modules_list`: #2 from above

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

- `get_goal_name`: #3 from above

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

- `get_module_name`: #4 from above

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
- `get_numbered_goal_names`: #6 from above

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

- `get_numbered_module_names`: #7 from above

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

- `get_ltp_activities`: #5 from above
	
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

## How to deploy

https://cloud.google.com/functions/docs/deploy

Two options: 

- Either edit the code directly via the UI
- Or deploy via console (recommended).

### Console deployment

#### First-time setup

Follow these steps:
- https://cloud.google.com/sdk/docs/install
- https://cloud.google.com/sdk/docs/initializing

#### Deploy after code/spreadsheet changes

```
gcloud config set project <id of your project>
gcloud functions deploy record-climate-data \
--gen2 \
--region=<region of your cloud function> \
--runtime=python311 \
--source=. \
--entry-point=serve \
--trigger-http
```

(Or simply run `deploy.sh`)