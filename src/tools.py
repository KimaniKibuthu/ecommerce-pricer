"""
Contains tools to be used by the agent
"""

import os
from typing import List, Optional, Type
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from langchain.agents import Tool
from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from langchain_community.utilities import SerpAPIWrapper
from langchain_experimental.open_clip import OpenCLIPEmbeddings
from src.utils import load_config, logger

# Load configuration and environment variables
config = load_config()
load_dotenv()

# Set up logging
logger.info("Setting up components for product price searching...")

# Instantiate the OpenCLIP embeddings
logger.info("Instantiating OpenCLIP embeddings...")
embeddings = OpenCLIPEmbeddings(
    model_name=config["vector_database"]["embedding_model_name"],
    checkpoint=config["vector_database"]["embedding_model_checkpoint"],
)

# Instantiate the VectorStore
logger.info("Instantiating VectorStore...")

client = QdrantClient(
    config["vector_database"]["url"], api_key=os.getenv("VECTORSTORE_API_KEY")
)
# Create search function
logger.info("Creating search wrapper...")
search = SerpAPIWrapper()

# Create tools
logger.info("Creating tools...")

# Create custom tools for retrieval
class Input(BaseModel):
    query: str = Field(description="should be a search query")


class CustomTextRetrieverTool(BaseTool):
    name = "text db retriever"
    description = "useful for retrieving from a text database"
    args_schema: Type[BaseModel] = Input
    return_direct: bool = True

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        query_vector = embeddings.embed_query(query)
        return client.search("apparel-collection", query_vector=query_vector, limit=3)


class CustomImageRetrieverTool(BaseTool):
    name = "image db retriever"
    description = "useful for retrieving from an image database"
    args_schema: Type[BaseModel] = Input
    return_direct: bool = True

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        query_vector = embeddings.embed_query(query)
        return client.search("img-collection", query_vector=query_vector, limit=3)


img_db_search = CustomImageRetrieverTool()
text_db_search = CustomTextRetrieverTool()

# Tool for retrieving product information from the text database based on the product description
tool_search_item = Tool(
    name="search internet",
    description="Searches the internet for the price of a product by using its description.",
    func=search.run,
    handle_tool_error=True,
)

tool_image_retriever = Tool(
    name="search image db",
    description="Searches for the price of a product using its description in the image db",
    func=img_db_search.run,
    handle_tool_error=True,
)

tool_text_retriever = Tool(
    name="search text db",
    description="Searches for the price of a product using its description in the text db",
    func=text_db_search.run,
    handle_tool_error=True,
)

# List of all tools
tools: List[Tool] = [tool_search_item, tool_image_retriever, tool_text_retriever]

logger.info("Setup completed successfully.")
