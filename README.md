# Mock FSP Portal

A simple web app for training purposes
https://fsp-portal.azurewebsites.net/

## Description
Synopsis: a [flask python app](https://flask.palletsprojects.com/en/2.0.x/) to mock a FSP portal for training purposes

Functionality:
- Upload a csv, with `id` and `amount` columns
  - If any column is missing, it will inform the user and not "do a payment"
  - If `id` contains a duplicate, it will inform the user and not "do a payment"
- Do mock payment
- Receive resulting report for reconciliation
  - A status column is added (between 1% and 5% will have status `error`, other have status `success`)
  - Between 1 and 3 rows will be deleted, and therefore "missing" from the file

The name of the portal can be set in an environment variable, if not set it will default to `Bank Payment Portal`.

## Setup

### run locally
Install requirements:

```sh
pip install -r requirements.txt
```

Copy the .env.example file

```sh
cp .env.example .env
```

Then edit the `.env` file to update the variables as needed.

Run the app:

```sh
flask run
```

### on Azure
[Deploy the web app to Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/quickstart-python)
