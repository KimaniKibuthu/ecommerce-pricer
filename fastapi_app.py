import os
import json
import base64
from PIL import Image
from io import BytesIO
from fastapi import FastAPI, Request
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from src.utils import logger, load_config
from src.agents import Agent
from src.prompts import prompt_template
from src.tools import tools
from dotenv import load_dotenv


# Load configuration and environment variables
config = load_config()
load_dotenv()

# Create the FastAPI app
app = FastAPI(
    title="Product Discovery Server",
    version="1.0",
    description="A server to calculate the price range of products",
)


# Create an instance of the Agent class
agent = Agent(
    llm_name=config["agents"]["llm_name"],
    tools=tools,
    prompt=prompt_template,
)

# Initialize the agent
agent_executor = agent.initialize()

# Set up the components for the search logic
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
gemini_vision = ChatGoogleGenerativeAI(
    model="gemini-pro-vision",
    google_api_key=GOOGLE_API_KEY,
    temperature=config["agents"]["temperature"],
)
parser = JsonOutputParser()


@app.post("/invoke")
async def generate_price_range(request: Request) -> dict:
    """
    FastAPI endpoint to generate the price range of a product based on the provided input data.

    Args:
        request (Request): The HTTP request containing input data.

    Returns:
        dict: A dictionary containing the estimated price range, or an error message if an exception occurs.
    """
    try:
        data = await request.json()
        user_text = data.get("user_text")
        image = data.get("image")

        if image and user_text:
            logger.info("Image and text exist")
            bytes_data = base64.b64decode(image)
            image = Image.open(BytesIO(bytes_data))
            chat_template = HumanMessage(
                content=[
                    {
                        "type": "text",
                        "text": f"""Your task is to generate a searchable prompt about the product in the image that I can feed to Google to find this exact product. You should:

                                    1. Given the description {user_text}, extract relevant details about the product from the image, such as brand, color, and your thoughts on quality and create a description based off your observations from the image and the description offered by the user.

                                    2. Use these details to generate a concise searchable prompt that would allow me to find this exact product on Google.

                                    3. Return ONLY the searchable prompt in the following JSON format: {{"search_prompt": "<YOUR_SEARCHABLE_PROMPT>}}. Do not include any other information or text.

                                    Please strictly follow these instructions and provide your response in the specified JSON format.""",
                    },
                    {"type": "image_url", "image_url": image},
                ]
            )

            # create a chain
            chain = gemini_vision | parser

            response = chain.invoke([chat_template])

            search_prompt = response["search_prompt"]

            response = agent_executor.invoke(
                {
                    "input": f"what is the estimated, accurate and compact price range of a/an {search_prompt}. Return ONLY the price range"
                }
            )
            output_str = response["output"]

            try:
                # Try parsing the response as JSON
                price_dict = json.loads(output_str)
                price_range = price_dict.get("price_range")
                if price_range:
                    return {"price_range": price_range}
                else:
                    return {"error": "Price range not found in response"}

            except json.JSONDecodeError:
                # If parsing as JSON fails, check if the response is a string
                if isinstance(output_str, str):
                    return {"price_range": output_str}
                else:
                    # If not a string, try to extract the substring containing the dictionary
                    start_index = output_str.find("{")
                    end_index = output_str.find("}") + 1
                    price_range_str = output_str[start_index:end_index]
                    try:
                        price_dict = json.loads(price_range_str)
                        price_range = price_dict.get("price_range")
                        if price_range:
                            return {"price_range": price_range}
                        else:
                            return {"error": "Price range not found in response"}
                    except json.JSONDecodeError:
                        return {"error": "Unable to parse price range from response"}

        else:
            logger.error(
                "Error generating price range: Please provide an image and text description."
            )
            return {"error": "Please provide an image and text description."}

    except Exception as e:
        logger.error(f"Error generating price range: {e}")
        return {"error": "An error occurred while generating the price range."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=config["fastapi"]["host"], port=config["fastapi"]["port"])
