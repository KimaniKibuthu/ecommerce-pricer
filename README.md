# Price Discovery

This branch contains the modularized code and the implementation of the fastapi app and the streamlit app.

## Introduction

Price Discovery is a project aimed at implementing a modularized system using FastAPI and Streamlit for efficient price discovery using a VLLM and an agent to get the price range of a product using its image and text description. This README provides an overview of the project structure and instructions on how to use it.

## Directory Structure

```plaintext
|-- configs
    |-- __init__.py
    |-- config.yaml

|-- data
    |-- databases
        |-- text_db
        |-- image_db
    |-- images
    |-- test_data
    |-- text_data

|-- notebooks
    |-- agents.ipynb
    |-- plan_and_execute_using_rewoo.ipynb

|-- src
    |-- __init__.py
    |-- agents.py
    |-- db.py
    |-- prompts.py
    |-- tools.py
    |-- utils.py

|-- poetry.lock
|-- .pre-commit-config.yaml
|-- pyproject.toml
|-- fastapi_app.py
|-- streamlit_app.py
|-- Dockerfile
|-- Makefile
|-- README.md
```

NOTE: The data folder will not be present in the repo. The one above is in place so as to showcase the immplementation of the database.

## Data implementation
To implement the database, you have several options available which you can choose from the `agents.ipynb` notebook.

You can choose to use the remote db already created. All you need is access which can be granted when you reach out [here](yunmokoo7@gmail.com)

You can also choose to recreate your own database ( Which will take quite some time) but for that you will need the data. Which is detailed below:

### Data Preparation

The source of our dataset: [Amazon Products Dataset 2023 (1.4M Products)](https://www.kaggle.com/datasets/asaniczka/amazon-products-dataset-2023-1-4m-products?select=amazon_products.csv)

There are two csv files in the dataset: amazon_products.csv (the main dataset) and amazon_categories.csv (description of each categories)

Download both files into your local machine

Data preparation script: `get_apparel_data.ipynb`

- This script first filter a particular number of products from each specified category from the main dataset. In this case, the script is choosing 5000 products from each of the ten apparel category, which results in sample dataset of 50000 products
- Then the image of each product is downloaded (it will take a long time, so downloading them in batch may be useful)
- Finally, we can choose to shuffle the dataset, choose which columns to keep, or split it into training or testing set. In this case, the list of columns is ```['asin', 'title', 'imgName', 'price', 'category_id', 'imgUrl', 'productURL']```

You can also opt to use the preprocessed datasets of size 20k or 50k which can be found [here](https://drive.google.com/drive/folders/17C-s4r774ons6z3CtCDsh8jH47p4_4PK?usp=sharing)

## Usage

The `notebooks` folder contains the notebooks which were used for experimentation with the agents as well as experimentation during the project.

The `src` folder contains the modularized code from the notebook `agents.ipynb`.

The `fastapi_app.py`  contains the FastApi app code.

The `streamlit_app.py` contains the streamlit app code.

The `Dockerfile` contains the Dockerfile used to build the Docker image for the project.

The `Makefile` contains the instructions to run the project.

To implement this,first clone the repo and navigate to this branch. Then:

### Option 1: Without Docker

1. Create a .env file and prepopulate the following environment variables:

    ```plaintext
    LANGCHAIN_API_KEY=""
    LANGCHAIN_PROJECT="price-discovery"
    LANGCHAIN_TRACING_V2="true"
    HUGGINGFACEHUB_API_TOKEN=""
    GOOGLE_API_KEY=""
    SERPAPI_API_KEY=""
    VECTORSTORE_API_KEY=""
    ```

    For the vectorstore api key, request for access from:

    Unless you want to create your own vectorstore. For this follow the following steps:


2. Install poetry using pip:

     ```bash
    pip install poetry
    ```

3. Configure poetry

    Set the configuration

     ```bash
    poetry config virtualenvs.in-project true
    ```

    Install dependencies

     ```bash
    poetry install
    ```

    Navigate to the venv

    ```bash
    poetry shell
    ```

    Install fastapi and streamlit

    ```bash
    pip install streamlit fastapi
    ```

4. Open two terminals

    - In one start the fastapi server:

        ```bash
      poetry run uvicorn fastapi_app:app --reload
      ```

    - In the second one start the sreamlit app:

        ```bash
      poetry run streamlit run streamlit_app.py
      ```

5. Open the app via the link provided once the streamlit app is running.

### Option 2: With Docker

1. Create a `.env` file and prepopulate the following environment variables (same as in Option 1)


2. Pull the Docker image from Docker hub:
     ```bash
    make pull
    ```

3. Run the Docker image:
    ```bash
    make run
    ```

4. In the config.yaml file, change the endpoint url under streamlit to:
    ```yaml
    streamlit_app:
        endpoint_url: "http://localhost:8000"
    ```

5. Access the applications:
    - FastAPI app: <http://localhost:8000>

    - Streamlit app: <http://localhost:8501>
