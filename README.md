# 🎬 YouTube Video Summarizer

An AI-powered YouTube Video Summarizer that automatically extracts transcripts and generates comprehensive summaries. Built with **LangChain LCEL**, **yt-dlp**, and **Streamlit**.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/LangChain-LCEL-green.svg" alt="LangChain">
  <img src="https://img.shields.io/badge/Streamlit-1.28+-red.svg" alt="Streamlit">
  <img src="https://img.shields.io/badge/OpenAI-GPT--4o-purple.svg" alt="OpenAI">
  <img src="https://img.shields.io/badge/yt--dlp-Latest-orange.svg" alt="yt-dlp">
</p>

---

## ✨ Features

- 🔗 **Paste YouTube URL** - Just paste any YouTube video link
- 📥 **Auto Transcript Extraction** - Uses yt-dlp with browser cookies
- 🤖 **AI-Powered Summary** - GPT-4o generates comprehensive summaries
- 📌 **Structured Output** - Brief summary, key points & takeaways
- 🌐 **Multi-language Support** - Supports English, Hindi, Tamil & more
- 📥 **Download Options** - Download summary & transcript as text files
- 🍪 **Browser Cookies** - Bypasses YouTube restrictions automatically
- ⚡ **Built with LCEL** - Modern LangChain Expression Language

---

## 🎯 What You Get

| Section | Description |
|---------|-------------|
| 📌 **Brief Summary** | 2-3 sentence overview of the video |
| 🎯 **Key Points** | 5-7 important bullet points |
| 💡 **Main Takeaways** | 3-4 actionable insights |

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | LangChain (LCEL) |
| LLM | OpenAI GPT-4o |
| UI | Streamlit |
| Transcript | yt-dlp |
| Language | Python 3.9+ |

---

## 📦 Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/youtube-summarizer.git
cd youtube-summarizer

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and add your OpenAI API key
```

---

## ⚙️ Configuration

Create a `.env` file:

```env
OPENAI_API_KEY=sk-your-api-key-here
```

---

## 🚀 Usage

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Steps:
1. 🔗 Paste YouTube video URL
2. 🌐 Select browser for cookies (Chrome recommended)
3. 🚀 Click "Summarize"
4. 📝 View AI-generated summary
5. 📥 Download summary or transcript

---

## 🔗 Supported URL Formats

```
✅ https://www.youtube.com/watch?v=VIDEO_ID
✅ https://youtu.be/VIDEO_ID
✅ https://www.youtube.com/watch?v=VIDEO_ID&t=123
✅ https://youtube.com/watch?v=VIDEO_ID
```

---

## 📝 Example

### Input:
```
YouTube URL: https://www.youtube.com/watch?v=O2gerCxEXvc
```

### Output:
```
📌 Brief Summary
This video explains the key differences between Generative AI 
and Agentic AI, covering their architectures, use cases, and 
future implications in the AI landscape.

🎯 Key Points
• Generative AI creates content (text, images, code)
• Agentic AI can take autonomous actions
• Both have different architectural approaches
• Use cases vary based on requirements
• Future AI systems may combine both approaches

💡 Main Takeaways
• Understand the distinction for better AI implementation
• Choose the right approach based on your use case
• Stay updated as both fields evolve rapidly
```

---

## 📁 Project Structure

```
youtube-summarizer/
├── app_auto.py              # Main Streamlit application
├── requirements.txt    # Dependencies
├── .env.example        # Environment template
├── .gitignore          # Git ignore file
└── README.md           # This file
```

---

## 📸 Screenshot

```
┌─────────────────────────────────────────────────┐
│  🎬 YouTube Video Summarizer                    │
├─────────────────────────────────────────────────┤
│                                    ⚙️ Settings  │
│  🔗 Enter YouTube URL:             Browser:     │
│  ┌─────────────────────────────┐  [Chrome ▼]   │
│  │ https://youtube.com/watch?  │               │
│  └─────────────────────────────┘               │
│                                                 │
│  [🚀 Summarize]                                 │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │         🎥 Video Preview                │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ✅ Transcript fetched! (Source: yt-dlp)       │
│                                                 │
│  📝 Video Summary                               │
│  ┌─────────────────────────────────────────┐   │
│  │ 📌 Brief Summary                        │   │
│  │ This video explains...                  │   │
│  │                                         │   │
│  │ 🎯 Key Points                           │   │
│  │ • Point 1                               │   │
│  │ • Point 2                               │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  [📥 Download Summary] [📜 Download Transcript] │
└─────────────────────────────────────────────────┘
```

---

## 🔑 Key Concepts

### yt-dlp with Browser Cookies
```python
ydl_opts = {
    'skip_download': True,
    'writeautomaticsub': True,
    'subtitleslangs': ['en', 'hi', 'ta'],
    'subtitlesformat': 'json3',
    'cookiesfrombrowser': ('chrome',),  # Uses Chrome cookies
}
```

### LCEL Chain
```python
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

chain = prompt | llm | parser
summary = chain.invoke({"transcript": transcript})
```

### Video ID Extraction
```python
def get_video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:].split('?')[0]
    elif parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        query = parse_qs(parsed_url.query)
        return query.get("v", [None])[0]
    return None
```

---

## 📋 Requirements

```
streamlit>=1.28.0
langchain>=0.1.0
langchain-core>=0.1.0
langchain-openai>=0.0.5
python-dotenv>=1.0.0
openai>=1.0.0
yt-dlp>=2024.1.0
```

---

## 🌐 Supported Browsers (for Cookies)

| Browser | Status |
|---------|--------|
| Chrome | ✅ Recommended |
| Firefox | ✅ Supported |
| Safari | ✅ Supported |
| Edge | ✅ Supported |
| Brave | ✅ Supported |

---

## ⚠️ Limitations

| Limitation | Description |
|------------|-------------|
| No captions | Some videos don't have subtitles enabled |
| Private videos | Cannot access private content |
| Age-restricted | May not work for restricted videos |
| Very long videos | Transcript truncated to 15k chars |

---

## 🔧 Troubleshooting

### Error: "No subtitle files found"
- Video doesn't have captions/CC enabled
- Try a different video with subtitles

### Error: "Could not extract cookies"
- Make sure the selected browser is installed
- Try logging into YouTube in that browser
- Try selecting a different browser

### Error: API related
- Check your OpenAI API key in `.env` file
- Ensure you have API credits

---

## 💡 Tips for Best Results

1. **Videos with CC** - Works best with videos that have captions
2. **Educational content** - Better summaries for structured content
3. **English videos** - Best transcript accuracy
4. **Chrome browser** - Recommended for cookie extraction

---

## 📚 Learning Resources

- [LangChain LCEL Docs](https://python.langchain.com/docs/concepts/lcel/)
- [yt-dlp Documentation](https://github.com/yt-dlp/yt-dlp)
- [Streamlit Docs](https://docs.streamlit.io/)
- [OpenAI API](https://platform.openai.com/docs/)

---

## 🆕 How It Works

```
┌─────────────────┐
│  YouTube URL    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Extract Video  │
│  ID from URL    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  yt-dlp         │
│  (with browser  │◄── Browser Cookies
│   cookies)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Download       │
│  Subtitles      │
│  (json3/vtt)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Parse & Clean  │
│  Transcript     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  LangChain LCEL │
│  Chain          │
│  (Prompt→LLM→   │
│   Parser)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AI Summary     │
│  • Brief        │
│  • Key Points   │
│  • Takeaways    │
└─────────────────┘
```

---

## 👨‍💻 Author

**Sathish**  

---

## 📄 License

MIT License

---

## ⭐ Show Your Support

If you found this helpful, give it a ⭐!

---

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - For reliable YouTube downloads
- [LangChain](https://langchain.com/) - For the amazing LCEL framework
- [OpenAI](https://openai.com/) - For GPT-4o
- [Streamlit](https://streamlit.io/) - For the beautiful UI framework
