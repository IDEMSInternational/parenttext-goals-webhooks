# ParentText Goals Webhooks

A chatbot for recording climate data in a database.

## Functionality

https://docs.google.com/document/d/1so5KrKuHwFyoLVpis2isWIh2eo0n4f90dPeqVIaKMqw/edit

Query URLs support the following paths:

- `get_goals_list`: #1 from above
	Get list of goal IDs, filtered by `filter_expression` and sorted by `sort_columns`.
- `get_modules_list`: #2 from above
	Description: see [here](https://docs.google.com/document/d/1so5KrKuHwFyoLVpis2isWIh2eo0n4f90dPeqVIaKMqw/edit)
- `get_goal_name`: #3 from above
- `get_module_name`: #4 from above
- `get_numbered_goal_names`: #6 from above
- `get_numbered_module_names`: #7 from above
- `get_ltp_activities`: #5 from above
	Get list of LTP activity IDs, filtered by `filter_expression` and sorted by `sort_columns`.

For examples, see `tests.py`

Each webhook returns a json with the main results in the `text` field.

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