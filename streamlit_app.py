import streamlit as st
import PIL
import base64
import asyncio
import aiohttp
import random
import json


async def fetch_data(url, payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            return await response.json()


async def process_response(url, payload):
    try:
        response = await fetch_data(url, payload)
        if isinstance(response, dict):
            try:
                price_range = response.get("price_range")
                if price_range:
                    if "</s>" in price_range:
                        # Case 1: Price range contains "<s>"
                        temp_price_range = price_range.split("</s>")[0]
                        price_range = json.loads(temp_price_range).get(
                            "price_range", ""
                        )
                    elif '"' in price_range:
                        # Case 2: Price range is enclosed in double quotes
                        price_range = json.loads(price_range).get("price_range", "")
                    # Format and display the price range
                    price_range = price_range.replace("−", "-")
                    st.success(f"**Price Range in Dollars:**  {price_range}")
                else:
                    st.write("Price range not found in response")
            except Exception as e:
                st.write(f"Error processing response: {e}")
        else:
            st.write("Invalid response format")
    except Exception as e:
        st.write(f"Error processing response: {e}")


def main() -> None:
    """
    Main function to create the Streamlit app for generating a price range based on user input.
    """
    st.set_page_config(
        page_title="Price Range Predictor, powered by gemini",
        page_icon="🔋",
        layout="centered",
        initial_sidebar_state="auto",
        menu_items=None,
    )

    st.title("Price Range Generator 🧠")

    st.info(
        "An app that takes in the product image and the description and outouts a price range",
        icon="💰",
    )

    spinner_messages = [
        "Maybe it's worth a million unicorns? Just kidding about the unicorns. (Unless...?) 🤸",
        "This image is a contender for 'The Most Awesome Thing Ever' award... 🤸",
        "Pssst... don't tell the other images, but yours is our favorite...Working to give you that price 🤸",
        "We're feeling the pressure to give you a great price. (Don't worry, be appy!) 🤸",
        "Shhh, we're crunching numbers! Don't want to wake the price gnomes... 🤸",
        "Making sure your price is fair. We wouldn't want to underpay a masterpiece (or overpay a potato...) 🤸",
        "Hang tight! We're working faster than a squirrel with a nut stash full of caffeine. 🤸",
        "Coffee break? Nah, gotta get this price estimate done for you, champ! 🤸",
    ]

    # User input components
    uploaded_image = st.file_uploader(
        "Upload a product image", type=["jpg", "jpeg", "png"]
    )
    user_text = st.text_input("Enter product description")

    if uploaded_image and user_text:
        with st.container(height=300):
            image = PIL.Image.open(uploaded_image)
            st.image(image, caption=user_text, use_column_width=True)

    # Button to trigger response generation
    if st.button("Get Price range"):
        with st.spinner(text=random.choice(spinner_messages)):
            bytes_data = uploaded_image.getvalue()
            encoded_image_str = base64.b64encode(bytes_data).decode("utf-8")
            asyncio.run(
                process_response(
                    "http://localhost:8000/invoke",
                    {"user_text": user_text, "image": encoded_image_str},
                )
            )


if __name__ == "__main__":
    main()
