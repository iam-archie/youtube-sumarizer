"""
YouTube Video Summarizer - Automatic Version (Fixed)
====================================================
Uses yt-dlp with browser cookies

Author: Sathish Suresh
"""

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from urllib.parse import urlparse, parse_qs
import os
import re
import tempfile
import json
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o", temperature=0.5)

summary_prompt = PromptTemplate(
    input_variables=["transcript"],
    template="""
    You are an expert summarizer.
    Here is the video transcript:

    {transcript}

    Please generate a clear, concise summary with:
    1. **📌 Brief Summary** (2-3 sentences)
    2. **🎯 Key Points** (5-7 bullet points)
    3. **💡 Main Takeaways** (3-4 insights)
    """
)

parser = StrOutputParser()
summary_chain = summary_prompt | llm | parser


def get_video_id(url):
    """Extract video ID from YouTube URL"""
    parsed_url = urlparse(url)
    if parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:].split('?')[0]
    elif parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        query = parse_qs(parsed_url.query)
        return query.get("v", [None])[0]
    return None


def get_transcript_yt_dlp(video_id, browser="chrome"):
    """Get transcript using yt-dlp with cookies"""
    
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    
    try:
        import yt_dlp
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, "subs")
            
            # FIXED OPTIONS - No format, just subtitles
            ydl_opts = {
                'skip_download': True,           # Don't download video
                'writeautomaticsub': True,       # Get auto-generated subs
                'writesubtitles': True,          # Get manual subs too
                'subtitleslangs': ['en', 'en-orig', 'en-US', 'hi', 'ta'],
                'subtitlesformat': 'json3',      # Easy to parse format
                'outtmpl': output_path,
                'quiet': True,
                'no_warnings': True,
                'cookiesfrombrowser': (browser,),  # Use browser cookies
                'ignoreerrors': True,
                # Remove format-related options that cause conflicts
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            
            # Find and parse subtitle file
            for file in os.listdir(temp_dir):
                if file.endswith('.json3'):
                    file_path = os.path.join(temp_dir, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Extract text from json3 format
                    texts = []
                    if 'events' in data:
                        for event in data['events']:
                            if 'segs' in event:
                                for seg in event['segs']:
                                    if 'utf8' in seg:
                                        text = seg['utf8'].strip()
                                        if text and text != '\n':
                                            texts.append(text)
                    
                    if texts:
                        # Remove consecutive duplicates
                        unique_texts = []
                        prev = ""
                        for t in texts:
                            if t != prev:
                                unique_texts.append(t)
                                prev = t
                        
                        return ' '.join(unique_texts), "yt-dlp (auto)", None
            
            # Try VTT format as fallback
            for file in os.listdir(temp_dir):
                if file.endswith('.vtt'):
                    file_path = os.path.join(temp_dir, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Parse VTT
                    lines = content.split('\n')
                    texts = []
                    for line in lines:
                        line = line.strip()
                        if not line or line.startswith('WEBVTT') or '-->' in line:
                            continue
                        if line.startswith('Kind:') or line.startswith('Language:'):
                            continue
                        if re.match(r'^\d+$', line):
                            continue
                        # Remove HTML tags
                        line = re.sub(r'<[^>]+>', '', line)
                        if line:
                            texts.append(line)
                    
                    if texts:
                        return ' '.join(texts), "yt-dlp (vtt)", None
            
            return None, None, "No subtitle files found"
            
    except ImportError:
        return None, None, "yt-dlp not installed"
    except Exception as e:
        return None, None, str(e)


# Streamlit UI
st.set_page_config(page_title="🎬 YouTube Summarizer", page_icon="🎬")

st.title("🎬 YouTube Video Summarizer")
st.markdown("*Automatic transcript extraction & AI summary*")

# Sidebar settings
with st.sidebar:
    st.header("⚙️ Settings")
    browser = st.selectbox(
        "🌐 Browser (for cookies):",
        ["chrome", "firefox", "safari", "edge", "brave"],
        index=0
    )
    st.info("Make sure you're logged into YouTube in this browser!")

st.divider()

# Main input
video_url = st.text_input(
    "🔗 Enter YouTube URL:",
    placeholder="https://www.youtube.com/watch?v=..."
)

if st.button("🚀 Summarize", type="primary"):
    if not video_url:
        st.warning("⚠️ Please enter a YouTube URL")
    else:
        video_id = get_video_id(video_url)
        
        if not video_id:
            st.error("❌ Invalid YouTube URL")
        else:
            # Show video
            st.video(f"https://www.youtube.com/watch?v={video_id}")
            
            # Get transcript
            with st.spinner("📥 Fetching transcript using yt-dlp..."):
                transcript, source, error = get_transcript_yt_dlp(video_id, browser)
            
            if not transcript:
                st.error(f"""
                ❌ **Could not fetch transcript**
                
                Error: {error}
                
                **Try:**
                1. Make sure Chrome is closed (not running)
                2. Select different browser in sidebar
                3. Check if video has subtitles
                """)
            else:
                st.success(f"✅ Transcript fetched! (Source: {source})")
                
                # Show transcript length
                st.info(f"📝 Transcript length: {len(transcript)} characters")
                
                # Truncate if needed
                if len(transcript) > 15000:
                    transcript = transcript[:15000] + "..."
                    st.warning("⚠️ Transcript truncated to 15000 chars")
                
                with st.spinner("🤖 Generating summary..."):
                    summary = summary_chain.invoke({"transcript": transcript})
                
                st.subheader("📝 Video Summary")
                st.markdown(summary)
                
                # Download
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="📥 Download Summary",
                        data=summary,
                        file_name=f"summary_{video_id}.txt",
                        mime="text/plain"
                    )
                with col2:
                    st.download_button(
                        label="📜 Download Transcript",
                        data=transcript,
                        file_name=f"transcript_{video_id}.txt",
                        mime="text/plain"
                    )
                
                # Show transcript
                with st.expander("📜 View Full Transcript"):
                    st.text_area("Transcript", transcript, height=200)

st.divider()
st.caption("Built with LangChain LCEL + Streamlit | Social Eagle AI")
