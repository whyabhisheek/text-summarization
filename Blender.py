import streamlit as st
from openai import OpenAI
import os
import yaml
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader

st.set_page_config(
    page_title="Blender",
    page_icon="✍️",
    layout="centered",
    initial_sidebar_state="auto",
)

logo_img = "logo.png"
st.image(logo_img, width=50)

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

authenticator.login()

if st.session_state["authentication_status"]:
    authenticator.logout(location='sidebar')
    st.write(f'Welcome *{st.session_state["name"]}* 👋')
    client = OpenAI()
    client.api_key = st.secrets["OPENAI_API_KEY"]
    # client.api_key = os.getenv("OPENAI_API_KEY")

    def Summarize_text(prompt, model_name, system_content):
        if model_name == "gpt-4-turbo-2024-04-09" or "gpt-4o-2024-05-13":
            max_tokens = 4096
        else:
            max_tokens = 6000

        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens
        )
        return completion

    def main():
        st.title("Blender - Chapter writer.")
        prompt = st.text_input("Enter prompt or questions", help="This prompt will be specific to this article.")

        uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
        if uploaded_file is not None:
            uploaded_text = uploaded_file.read().decode("utf-8")
            prompt += "\n\n" + uploaded_text

        models = ["gpt-4-turbo-2024-04-09", "gpt-3.5-turbo-16k", "gpt-4o-2024-05-13"] 
        model_name = st.selectbox("Select the model", models)

        edit_system_content = st.checkbox("Edit System Content", help="This is the default system prompt. Edits will only be applied to this article")
        default_system_content = """When I give you a podcast transcript Based on the provided transcript, craft a comprehensive chapter that distils the essence of the conversation for our book targeted at entrepreneurs worldwide. This chapter, ideally 1,500 words or up to 10 minutes of reading time, should be presented in a professional tone reminiscent of a British journalist. It aims to cater to college-educated entrepreneurs seeking actionable solutions to their business challenges. Your narrative should summarise and transform the conversation into an engaging, standalone piece that outlines key insights, strategies, and personal stories the interviewee shares.

Additionally, enrich the chapter by incorporating one piece of relevant industry research supporting the discussed marketing strategy or business solution. This research should be contemporary and applicable, enhancing the credibility and depth of the advice given.

Ensure to include a citation link for the research in the notes, adhering to proper academic standards.

The chapter should weave together practical advice, inspiration, and actionable strategies, rendered in a style consistent with The Economist, to ensure coherence and uniformity across our publication. This article aims to give the impression that the reader is conversing with the speaker.

Use the following structure with 4 sections.

- think of a title
- Prologue - subtitle: [150 words]
- The Opportunity - subtitle (150 - 200 words)
- Crossing the chasm - subtitle: [800 words]
- Epilogue - Reflections - subtitle: [150 words]

Include at least one quote from the interviewee in each section, and also include their country name, city ot where they are from in Prologue section

Do not mention that the interviewee is a guest on the podcast.

This service is provided by UnNoticed Ventures Ltd., focusing on transforming insightful conversations into impactful written content for entrepreneurs."""
        if edit_system_content:
            system_content = st.text_area("System Content ", default_system_content, height=400)
        else:
            system_content = default_system_content

        if "response_text" not in st.session_state:
            st.session_state["response_text"] = ""

        generate_summary_button = st.button("Generate Summary")

        output_container = st.container()

        if generate_summary_button:
            st.write("Generating...")
            loading_placeholder = st.empty()
            completion = Summarize_text(prompt, model_name, system_content)
            response_text = completion.choices[0].message.content

            loading_placeholder.empty()

            if response_text:
                st.download_button(
                    label="Download Summary",
                    data=response_text.encode("utf-8"),
                    file_name="summary.txt",
                    mime="text/plain"
                )
            else:
                st.write("No summary generated. Please try again.")

            st.session_state["response_text"] = response_text

            with output_container:
                output_container.empty()  
                st.write(response_text)

        else:
            with output_container:
                output_container.empty()  
                if st.session_state["response_text"]:
                    st.write(st.session_state["response_text"])

    if __name__ == "__main__":
        main()


elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')