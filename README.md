# Price Discovery
This branch contains the modularized code and the implementation of the fastapi app and the streamlit app.


## Directory Structure
```
|-- README.md

|-- configs
    |-- __init__.py
    |-- config.yaml

|-- data
    |-- databases
        |-- clip_textdb
        |-- db
        |-- image_db
    |-- images
    |-- test_data
    |-- text_data

|-- fastapi_app.py
|-- logs
    |-- logs.log

|-- notebooks
    |-- agents.ipynb
    |-- plan_and_execute_using_rewoo.ipynb

|-- poetry.lock
|-- pyproject.toml
|-- src
    |-- __init__.py
    |-- agents.py
    |-- db.py
    |-- prompts.py
    |-- tools.py
    |-- utils.py

|-- streamlit_app.py
```

NOTE: The data folder will not be present in the repo. The one above is in place so as to showcase the immplementation of the database.

## Usage

The `notebooks` folder contains the `agents.ipynb` notebook which is used for experimentation with the agents.

The `src` folder contains the modularized code from the notebook.

The `fastapi_app.py`  contains the fastapi app code.

The `streamlit_app.py` contains the streamlit app code.

To implement this, first clone the repo and navigate to this branch. Then:
1. Create a .env file and prepopulate the following environment variables:

    ```
    LANGCHAIN_API_KEY=""
    LANGCHAIN_PROJECT="price-discovery"
    LANGCHAIN_TRACING_V2="true"
    HUGGINGFACEHUB_API_TOKEN=""
    GOOGLE_API_KEY=""
    SERPAPI_API_KEY=""
    ```

2. Install poetry using pip:

    `pip install poetry`

3. Configure poetry

    Set the configuration

    `poetry config virtualenvs.in-project=true`

    Install dependencies

    `poetry install`

    Navigate to the venv

    `poetry shell`

    Install fastapi and streamlit

    `pip install streamlit fastapi`

4. Open two terminals

    In one start the fastapi server:

    `poetry run uvicorn fastapi_app:app --reload`

    In the second one start the sreamlit app:

    `poetry run streamlit run streamlit_app.py`

5. Open the app via the link provided once the streamlit app is running.
