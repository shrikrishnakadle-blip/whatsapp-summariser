import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="News Summarizer", page_icon="📰")

st.title("📱 WhatsApp News Summarizer")
url = st.text_input("Paste YouTube Link:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Generate Summary"):
    if url:
        try:
            with st.spinner("Analyzing YouTube video directly..."):
                client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
                
                prompt = (
                    "Summarize this news report in 3 to 4 clear, punchy WhatsApp bullet points.\n"
                    "Use *bold* for names/stats and 1-2 news emojis. No intro text."
                )
                
                # Gemini natively extracts the video context directly from the URL
                response = client.models.generate_content(
                    model="gemini-3.6-flash", 
                    contents=types.Content(
                        parts=[
                            types.Part(file_data=types.FileData(file_uri=url)),
                            types.Part(text=prompt)
                        ]
                    )
                )
                
                st.success("Summary Generated!")
                st.markdown(response.text)

        except Exception as e:
            st.error(f"Error details: {e}")
    else:
        st.warning("Please enter a URL first.")
