# Deploy to Google Cloud Run using Github Actions

Github Actions can be used to deploy the Goals API to Cloud Run when goals data is updated.

## Setup

### GCP

Create a service account that will be used for the deployment. In your project, go to _IAM and admin_ > _Service accounts_. Click on _CREATE SERVICE ACCOUNT_. Give the account an appropriate name and ID. Click _CREATE AND CONTINUE_.

Add the following roles to the service account:

- Cloud Run Admin
- Service Account User

Click _CONTINUE_, then click _DONE_.

Create service account keys. Go to _IAM and admin_ > _Service accounts_; view details for the newly created service account. On the details page, select the _KEYS_ tab. Click _ADD KEY_ > _Create new key_. Make sure the _JSON_ option is selected, then click the _CREATE_ button. The new keys should be automatically downloaded.

Reformat the contents of the credentials file so that they occupy only a single line. A tool called `jq` can be used to accomplish this.

```
jq -c . {credentials_file} > single_line_credentials.json
```

The credentials will be required when the Github Actions workflow is set up.

### Github

Create a new workflow for the deployment.

```
name: Deploy goals API

on:
  workflow_dispatch:

jobs:
  pipeline:
    uses: IDEMSInternational/parenttext-goals-webhooks/.github/workflows/deploy.yml@c1db31107c4898ace2813f63ab504afe4b5c5a68
    secrets:
      credentials: ${{ secrets.GCP_CREDENTIALS }}
    with:
      image: ${{ vars.GOALS_API_IMAGE }}
      region: ${{ vars.GCP_REGION }}
      service_env: ${{ vars.GCP_SERVICE_ENV }}
      service_identity: ${{ vars.GCP_SERVICE_IDENTITY }}
      service_name: ${{ vars.GCP_SERVICE_NAME }}
```

Create repository variables to give the deployment action the information it needs. Go to _Settings_ > _Secrets and variables_ > _Actions_; select the _Variables_ tab. Create each variable by clicking on the _New repository variable_ button. Create the following variables.

- GOALS\_API\_IMAGE: the container image to deploy e.g. `idems/parenttext-goals-webhooks:0.6.0`
- GCP_REGION: Google Cloud region to deploy to e.g. `europe-west1`
- GCP\_SERVICE\_ENV: Settings for the API i.e. the contents of the `.env` file, but with newlines replaced with commas.
- GCP\_SERVICE\_IDENTITY: The service account under which the API will be run.
- GCP\_SERVICE\_NAME: Name of the Cloud Run service e.g. `pt-goals-example`

Create a repository secret to store the Google Cloud service account credentials. Go to _Settings_ > _Secrets and variables_ > _Actions_; select the _Secrets_ tab. Click on the _New repository secret_ button. Create the secret as follows:

- GCP_CREDENTIALS: Contents of the credentials file `single_line_credentials.json`, from above.


## Deploy

Convert the spreadsheet(s) with goal data to JSON format. The JSON file can be saved anywhere in the repository, under any name.

```
rpft convert -f google_sheets {sheet_id} content/localized.json
```

Commit JSON file to ParentText deployment repository.

Navigate to _Actions_ > _Deploy goals API_ page. Click the _Run workflow_ button, then the green _Run workflow_ button.

Wait for the job to complete. The service URL of the API can be found in the logs at the end of the _Deploy to environment_ step. It should not change after the first deployment.
