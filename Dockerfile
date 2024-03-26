# # Use the official Python image as the base image
# FROM python:3.9-slim

# # Set the working directory in the container
# WORKDIR /app

# # Copy the poetry files to the working directory
# COPY poetry.lock pyproject.toml ./

# # Install Poetry
# RUN pip install poetry

# # Install the project dependencies
# RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

# RUN pip install streamlit fastapi

# # Copy the rest of the application code to the working directory
# COPY fastapi_app.py .
# COPY streamlit_app.py .

# # Copy the necessary directories
# COPY src src/
# COPY configs configs/




# # Expose the ports for FastAPI and Streamlit
# EXPOSE 8000
# EXPOSE 8501

# # Set the entrypoint to run both FastAPI and Streamlit
# CMD ["bash", "-c", "poetry run uvicorn fastapi_app:app --host 0.0.0.0 --port 8000 & poetry run streamlit run streamlit_app.py --server.port 8501"]
# Build stage
FROM python:3.9-slim as build

WORKDIR /app

# Copy the poetry files to the working directory
COPY poetry.lock pyproject.toml ./

# Install Poetry
RUN pip install poetry

# Install the project dependencies
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

# Production stage
FROM python:3.9-slim

WORKDIR /app

# Copy only the necessary files from the build stage
COPY --from=build /app/.venv/lib/python3.9/site-packages /app/.venv/lib/python3.9/site-packages
COPY fastapi_app.py streamlit_app.py ./
COPY src src/
COPY configs configs/

# Install FastAPI and Streamlit
RUN pip install streamlit fastapi

# Expose the ports for FastAPI and Streamlit
EXPOSE 8000
EXPOSE 8501

# Set the entrypoint to run both FastAPI and Streamlit
CMD ["bash", "-c", "poetry run uvicorn fastapi_app:app --host 0.0.0.0 --port 8000 & poetry run streamlit run streamlit_app.py --server.port 8501"]
