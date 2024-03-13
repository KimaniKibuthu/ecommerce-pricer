import os
from typing import List
from langchain.agents import Tool
from langchain.tools.retriever import create_retriever_tool
from langchain_community.utilities import SerpAPIWrapper
from src.db import VectorStore
from langchain_experimental.open_clip import OpenCLIPEmbeddings
from src.utils import logger, load_config
from dotenv import load_dotenv

# Load configuration and environment variables
config = load_config()
load_dotenv()

# Set up logging
logger.info("Setting up components for product price searching...")

# Instantiate the OpenCLIP embeddings
logger.info("Instantiating OpenCLIP embeddings...")
open_clip_embeddings = OpenCLIPEmbeddings(
    model_name=config["vector_database"]["embedding_model_name"],
    checkpoint=config["vector_database"]["embedding_model_checkpoint"],
)

# Instantiate the VectorStore
logger.info("Instantiating VectorStore...")
vector_store = VectorStore(
    persist_directory=config["vector_database"]["existing_text_db_directory"],
    embedding_function=open_clip_embeddings,
    collection_name=config["vector_database"]["text_collection_name"],
    remote=config["vector_database"]["is_remote"],
    url=config["vector_database"]["url"],
    api_key=os.getenv("VECTORSTORE_API_KEY"),
)

# Instantiate the Chroma vector store
logger.info("Instantiating Chroma vector store...")
db = vector_store.instantiate()

# Create a retriever from the vector store
logger.info("Creating text retriever...")
text_retriever = vector_store.create_retriever(db)

# Create search function
logger.info("Creating search wrapper...")
search = SerpAPIWrapper()

# Create tools
logger.info("Creating tools...")
tool_search_item = Tool(
    name="search internet",
    description="Searches the internet for the price of a product by using its description.",
    func=search.run,
    handle_tool_error=True,
)

tool_search_image = Tool(
    name="search image",
    description="Searches for the price of a product using the image.",
    func=search.run,
    handle_tool_error=True,
)

tool_retrieve_from_text_db = create_retriever_tool(
    text_retriever,
    "search text db",
    "Query a retriever for product price using its product description.",
)

# List of all tools
tools: List[Tool] = [tool_search_item, tool_search_image, tool_retrieve_from_text_db]

logger.info("Setup completed successfully.")
