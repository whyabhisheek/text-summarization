import streamlit as st 
import assemblyai as aai
import streamlit_scrollable_textbox as stx




st.title("Transcription")
file_url = st.text_input("Enter the URL of the audio file:")
if st.button("Transcribe"):
        if file_url:
            transcript = transcribe_audio(file_url)
            
            for chapter in transcript.chapters:
                st.write("Chapter Start Time: ", chapter.start)
                st.write("Chapter End Time: ", chapter.end)
                st.write("Chapter Gist: ", chapter.gist)
                st.write("Chapter Headline: ", chapter.headline)
                st.write("Chapter Summary: ", chapter.summary)
        else:
            st.warning("Please enter the URL of the audio file.")