# # Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the poetry files to the working directory
COPY poetry.lock pyproject.toml ./

# Install Poetry
RUN pip install poetry

# Install the project dependencies
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

RUN pip install streamlit fastapi

# Copy the rest of the application code to the working directory
COPY fastapi_app.py .
COPY streamlit_app.py .

# Copy the necessary directories
COPY src src/
COPY configs configs/
COPY logs logs/
# Expose the ports for FastAPI and Streamlit
EXPOSE 8000
EXPOSE 8501

# Set the entrypoint to run both FastAPI and Streamlit
CMD ["bash", "-c", "poetry run uvicorn fastapi_app:app --host 0.0.0.0 --port 8000 & poetry run streamlit run streamlit_app.py --server.port 8501"]
