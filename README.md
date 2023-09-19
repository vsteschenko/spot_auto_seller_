# Installation

Clone the repo, create .env file in the project root directory, and fill it with required variables \
(can be found in /app/src/config.py:Settings)

### Run with poetry (dev)
Make sure you have poetry installed

Enter root project dir from the terminal, execute `poetry install`, \
and select created venv as project default in the terminal

You can run the project with `poetry run python app` from project root directory, \
or with ide run configuration using poetry venv

### Run with docker (prod)
Make sure you have docker installed

Build an image with `docker build -t test_spot_auto_seller .` from the project root directory

Run from the project root directory with 
```
docker run -d --name=spot_auto_seller_container --env-file=.env test_spot_auto_seller
``` 

# Deploy 

Image builds automatically with gha, autodeploy might be later
