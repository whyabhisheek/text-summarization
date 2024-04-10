import streamlit as st
from openai import OpenAI
import streamlit_scrollable_textbox as stx
import os

client = OpenAI()
client.api_key = st.secrets["OPENAI_API_KEY"]
# client.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="juicer",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed",
)

logo_img = "logo.png"
st.image(logo_img, width=50)

def Summarize_text(prompt,model_name, system_content):
    if model_name == "gpt-4-turbo-2024-04-09":
        max_tokens = 4096
    else:
        max_tokens = 6000

    completion = client.chat.completions.create(
        model = model_name,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens
    )
    return completion


def main():
    st.title("juicer - Chapter writer.")

    prompt = st.text_input("Enter prompt or questions")

    uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
    if uploaded_file is not None:
        uploaded_text = uploaded_file.read().decode("utf-8")
        prompt += "\n\n" + uploaded_text


    models = ["gpt-3.5-turbo-16k","gpt-4-turbo-2024-04-09"	 ]  # Add more models if needed
    model_name = st.selectbox("Select the model", models)

    edit_system_content = st.checkbox("Edit System Content")
    default_system_content = """
When I give you a podcast transcription, with style after a British business coach, begin each Strategy Smoothie by identifying the key question or problem a business owner might be considering, to help entrepreneurs quickly determine if the strategy discussed fits their current needs. delves into key strategies extracted from interviews, offering practical insights.
explore a primary strategy in detail, include additional relevant strategies when beneficial, and provide a summary of its application along with three detailed steps for practical implementation. give Recommendations for further reading and practical tools are included, making the advice practical and relevant for a global audience of college-educated entrepreneurs. The conversational tone, akin to advice from a seasoned coach, makes complex strategies accessible and engaging.

Include useful resources e.g. books, tech stack tools, podcasts
"""
    if edit_system_content:
        system_content = st.text_area("System Content ", default_system_content, height=400)
    else:
        system_content = default_system_content

    if st.button("Generate Summary"):
        st.write("Generating...")
        loading_placeholder = st.empty()
        completion = Summarize_text(prompt, model_name, system_content)
        response_text = completion.choices[0].message.content

        if response_text:
            loading_placeholder.empty()
            st.write(response_text)
            st.download_button(
                label="Download Summary",
                data=response_text.encode("utf-8"),
                file_name="summary.txt",
                mime="text/plain"
            )


if __name__ == "__main__":
    main()
