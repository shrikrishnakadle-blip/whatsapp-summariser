import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai

st.set_page_config(page_title="News Summarizer", page_icon="📰")

st.title("📱 WhatsApp News Summarizer")
url = st.text_input("Paste YouTube Link:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Generate Summary"):
    if url:
        try:
            with st.spinner("Extracting captions..."):
                # 1. Isolate the video ID from the URL
                if "v=" in url:
                    video_id = url.split("v=")[1].split("&")[0]
                elif "youtu.be/" in url:
                    video_id = url.split("youtu.be/")[1].split("?")[0]
                else:
                    st.error("Invalid YouTube URL.")
                    st.stop()
                
                # 2. Fetch the transcript instantly
                transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
                full_text = " ".join([segment['text'] for segment in transcript_data])
            
            with st.spinner("Writing WhatsApp summary..."):
                # 3. Pass the text to Gemini
                # The API key is securely pulled from Streamlit's hidden secrets
                client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
                
                prompt = (
                    "Summarize this news report in 3 to 4 clear, punchy WhatsApp bullet points.\n"
                    "Use *bold* for names/stats and 1-2 news emojis. No intro text.\n\n"
                    f"Transcript:\n{full_text}"
                )
                
                response = client.models.generate_content(
                    model="gemini-3.6-flash", 
                    contents=prompt
                )
                
                # 4. Display the final result
                st.success("Summary Generated!")
                st.markdown(response.text)

        except Exception as e:
            st.error(f"Could not process the video. It may not have captions enabled. Error details: {e}")
    else:
        st.warning("Please enter a URL first.")