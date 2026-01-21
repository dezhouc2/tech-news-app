# ⚡ Tech Pulse - Tech News Summarizer

A modern web application that aggregates the hottest tech news from multiple sources and provides AI-powered summaries using OpenAI's GPT-4o-mini.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.37-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🎯 Features

- **Real-time News Aggregation**: Fetches top stories from Hacker News and optionally NewsAPI
- **AI-Powered Summaries**: Generate concise, insightful summaries using OpenAI's GPT-4o-mini
- **Beautiful Dark UI**: Custom-styled interface with smooth animations
- **Smart Filtering**: Filter by score, number of stories, and data sources
- **Caching**: 5-minute cache to reduce API calls and improve performance
- **Responsive Design**: Works well on desktop and mobile

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd tech_news_app
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example.txt .env
   ```
   Then edit `.env` and add your API keys.

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open in browser**
   The app will automatically open at `http://localhost:8501`

## 🔑 API Keys Setup

### Required: OpenAI API Key (for AI summaries)

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create an account or sign in
3. Generate a new API key
4. Add it to your `.env` file or paste it in the sidebar

**Cost**: GPT-4o-mini is very affordable (~$0.15 per 1M input tokens)

### Optional: NewsAPI Key (for additional news sources)

1. Go to [NewsAPI](https://newsapi.org/register)
2. Create a free account
3. Copy your API key
4. Add it to your `.env` file or paste it in the sidebar

**Note**: The app works without any API keys! Hacker News is free and doesn't require authentication. API keys are only needed for AI summaries and additional news sources.

## 📁 Project Structure

```
tech_news_app/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── env.example.txt        # Example environment variables
├── README.md              # This file
└── .streamlit/
    └── config.toml        # Streamlit theme configuration
```

## 🏗️ Approach & Architecture

### Design Decisions

1. **Streamlit Framework**: Chosen for rapid development and built-in UI components. It allows building a full web app in a single Python file with minimal boilerplate.

2. **Data Sources**:
   - **Hacker News API**: Free, no authentication required, high-quality tech-focused content
   - **NewsAPI**: Optional, provides mainstream tech news coverage

3. **AI Summarization**: Uses OpenAI's GPT-4o-mini for cost-effective, high-quality summaries. The model is prompted to explain why each story matters for the tech industry.

4. **Caching Strategy**: 5-minute TTL cache using Streamlit's `@st.cache_data` decorator to minimize API calls while keeping content relatively fresh.

### Tradeoffs

| Decision | Pros | Cons |
|----------|------|------|
| **Streamlit** | Fast development, Python-only, easy deployment | Limited UI customization, not ideal for complex interactions |
| **Client-side API keys** | Simple setup, no backend needed | Keys visible in browser (mitigated by password input) |
| **On-demand summaries** | Saves API costs, user control | Requires click per article |
| **Hacker News as primary** | Free, high quality, tech-focused | May miss mainstream tech news |

### What I'd Build Next (with more time)

1. **Backend API**: Move API keys server-side for better security
2. **Summary Caching**: Cache AI summaries in a database to avoid regenerating
3. **More Sources**: Add Reddit r/technology, TechCrunch RSS, The Verge
4. **Scheduled Updates**: Background job to pre-fetch and summarize top stories
5. **User Preferences**: Save filters and favorite topics
6. **Email Digest**: Daily/weekly email with top summarized stories
7. **Sentiment Analysis**: Add sentiment badges to stories
8. **Search & History**: Search past stories and view reading history

## 🤖 AI Tools Used

This project was built with assistance from **Claude (Anthropic)** - an AI assistant. Here's how AI was used:

1. **Architecture Planning**: Discussed tech stack options (Next.js vs Streamlit vs FastAPI) and chose Streamlit for rapid development
2. **Code Generation**: AI helped write the initial codebase including:
   - Streamlit app structure
   - API integration functions
   - Custom CSS styling
   - OpenAI integration
3. **Documentation**: AI helped draft this README
4. **Debugging**: AI assisted with troubleshooting and code improvements

**Note**: All code was reviewed and the final implementation decisions were made by the developer.

## 🎨 Customization

### Changing the Theme

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#00d4aa"      # Accent color
backgroundColor = "#0e1117"    # Main background
secondaryBackgroundColor = "#1a1f2e"  # Card background
textColor = "#fafafa"         # Text color
```

### Adding More News Sources

You can extend the app by adding new fetch functions in `app.py`. Follow the pattern of `fetch_hackernews_top_stories()`:

```python
@st.cache_data(ttl=300)
def fetch_your_source() -> list[dict]:
    # Fetch and return stories in the standard format
    return [{
        "id": ...,
        "title": ...,
        "url": ...,
        "score": ...,
        "author": ...,
        "time": ...,
        "comments": ...,
        "source": "Your Source",
    }]
```

## 🚢 Deployment

### Streamlit Cloud (Recommended - Free)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Add your API keys in Streamlit Cloud's secrets management
5. Deploy!

### Other Options

- **Railway**: `railway up`
- **Render**: Connect GitHub, auto-deploys
- **Heroku**: Standard Python deployment

## 📝 Assumptions Made

1. **Target Audience**: Developers and tech enthusiasts who want quick access to trending tech news
2. **News Freshness**: 5-minute cache is acceptable; real-time updates not critical
3. **Summary Quality**: AI summaries based on headlines are sufficient (full article scraping would require more complex implementation)
4. **Browser Environment**: Users have modern browsers with JavaScript enabled

## 📄 License

MIT License - feel free to use this code for your own projects!

---

Built with ❤️ using Python, Streamlit, and OpenAI
