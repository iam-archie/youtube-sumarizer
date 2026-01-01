import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o", temperature=0.5)

summary_prompt = PromptTemplate(
    input_variables=["transcript"],
    template= """
    You are an expert summarizer.
    Here is the video transcript:

    {transcript}

    please generate a clear, concise summary of the main points and topics.
    """
)

summary_chain = summary_prompt | llm 

st.title("You tube video summarizer")

video_url = st.text_input("Enter youtube video URL")

def get_video_id(url):
    """
    Extract video id from youtube URL
    """
    parsed_url = urlparse(url)
    if parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]
    elif parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        query = parse_qs(parsed_url.query)
        return query.get("v", None)[0]
    return None

if st.button("Summarize"):
    if not video_url:
        st.warning("Please enter a video URL:")
    else:
        video_id = get_video_id(video_url)
        if not video_id:
            st.error("Invalid video URL")
        else:
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                full_text = " ".join([t['text']for t in transcript_list])
                summary = summary_chain.invoke({"transcript": full_text})
                st.subheader("Video Summary")
                st.write(summary)
            except Exception as e:
                st.error(f"Error: {str(e)}")

