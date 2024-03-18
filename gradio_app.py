import gradio as gr


def discover(Description, Image):
    return "Hello"


desc = (
    "This app **Price Discovery** takes a *image and description of a product as input* and creates "
    "a price range of the given product."
)

article = (
    "<h3>How to Use:</h3> "
    "<ul><li>Open the Price Discovery app.</li> "
    "<li>Type product description in the provided description box.</li>"
    "<li>Attach product image in the provided image box.</li>"
    "<li>Click on the 'Submit' button. <strong>Voila!</strong>, An accurate price range "
    "of the product will appear on the screen.</li></ul>"
)


demo = gr.Interface(
    fn=discover,
    inputs=["textbox", "image"],
    outputs=[gr.Textbox(label="Price Range")],
    title="Price Discovery",
    description=desc,
    article=article,
    theme=gr.Theme.from_hub("HaleyCH/HaleyCH_Theme"),
    allow_flagging="never",
)

if __name__ == "__main__":
    demo.launch(share=True)
