"""
Tech news aggregator with AI summaries.
Pulls from HN and NewsAPI, uses GPT-4o-mini for summaries.
"""

import streamlit as st
import requests
from datetime import datetime
from typing import Optional
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

st.set_page_config(
    page_title="Tech Pulse | Hot Tech News",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS for a polished look
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Global styles */
    .stApp {
        font-family: 'Space Grotesk', sans-serif;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #1a1f2e 0%, #0e1117 100%);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 1px solid #2d3748;
        text-align: center;
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00d4aa, #00b4d8, #9b5de5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        color: #a0aec0;
        font-size: 1.1rem;
    }
    
    /* News card styling */
    .news-card {
        background: linear-gradient(145deg, #1a1f2e 0%, #151922 100%);
        border: 1px solid #2d3748;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .news-card:hover {
        border-color: #00d4aa;
        box-shadow: 0 4px 20px rgba(0, 212, 170, 0.15);
        transform: translateY(-2px);
    }
    
    .news-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #f7fafc;
        margin-bottom: 0.75rem;
        line-height: 1.4;
    }
    
    .news-title a {
        color: #f7fafc;
        text-decoration: none;
    }
    
    .news-title a:hover {
        color: #00d4aa;
    }
    
    .news-meta {
        display: flex;
        gap: 1rem;
        color: #718096;
        font-size: 0.875rem;
        margin-bottom: 1rem;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .news-summary {
        color: #a0aec0;
        font-size: 0.95rem;
        line-height: 1.6;
        padding: 1rem;
        background: rgba(0, 212, 170, 0.05);
        border-left: 3px solid #00d4aa;
        border-radius: 0 8px 8px 0;
    }
    
    .source-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background: rgba(155, 93, 229, 0.2);
        color: #9b5de5;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    
    .score-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background: rgba(0, 212, 170, 0.2);
        color: #00d4aa;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    
    /* Stats cards */
    .stat-card {
        background: linear-gradient(145deg, #1a1f2e 0%, #151922 100%);
        border: 1px solid #2d3748;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #00d4aa;
    }
    
    .stat-label {
        color: #718096;
        font-size: 0.875rem;
    }
    
    /* Loading animation */
    .loading-pulse {
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.6; }
        50% { opacity: 1; }
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #00d4aa, #00b4d8);
        color: #0e1117;
        font-weight: 600;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        box-shadow: 0 4px 15px rgba(0, 212, 170, 0.4);
        transform: translateY(-1px);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: #1a1f2e;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=300)
def fetch_hackernews_top_stories(limit: int = 30) -> list[dict]:
    """Fetch top stories from HN."""
    try:
        # Get top story IDs
        response = requests.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json",
            timeout=10
        )
        story_ids = response.json()[:limit]
        
        stories = []
        for story_id in story_ids:
            story_response = requests.get(
                f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                timeout=10
            )
            story = story_response.json()
            
            if story and story.get("type") == "story" and story.get("title"):
                stories.append({
                    "id": story_id,
                    "title": story.get("title", ""),
                    "url": story.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                    "score": story.get("score", 0),
                    "author": story.get("by", "anonymous"),
                    "time": datetime.fromtimestamp(story.get("time", 0)),
                    "comments": story.get("descendants", 0),
                    "source": "Hacker News",
                })
        
        return stories
    except Exception as e:
        st.error(f"Error fetching Hacker News: {e}")
        return []


@st.cache_data(ttl=300)
def fetch_newsapi_tech_news(api_key: str, limit: int = 20) -> list[dict]:
    """Fetch from NewsAPI (needs key)."""
    if not api_key:
        return []
    
    try:
        response = requests.get(
            "https://newsapi.org/v2/top-headlines",
            params={
                "category": "technology",
                "language": "en",
                "pageSize": limit,
                "apiKey": api_key,
            },
            timeout=10
        )
        data = response.json()
        
        if data.get("status") != "ok":
            return []
        
        stories = []
        for article in data.get("articles", []):
            if article.get("title") and article.get("title") != "[Removed]":
                stories.append({
                    "id": hash(article.get("url", "")),
                    "title": article.get("title", ""),
                    "url": article.get("url", ""),
                    "description": article.get("description", ""),
                    "score": 0,
                    "author": article.get("author", article.get("source", {}).get("name", "Unknown")),
                    "time": datetime.fromisoformat(article.get("publishedAt", "").replace("Z", "+00:00")) if article.get("publishedAt") else datetime.now(),
                    "comments": 0,
                    "source": article.get("source", {}).get("name", "NewsAPI"),
                    "image": article.get("urlToImage"),
                })
        
        return stories
    except Exception as e:
        st.error(f"Error fetching NewsAPI: {e}")
        return []


def summarize_with_ai(title: str, url: str, openai_api_key: str) -> Optional[str]:
    """Call GPT to summarize the article."""
    if not openai_api_key:
        return None
    
    try:
        client = OpenAI(api_key=openai_api_key)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are a tech news summarizer. Given a news headline and URL, provide a brief, 
                    insightful 2-3 sentence summary explaining why this news matters for the tech industry. 
                    Be concise, factual, and highlight the key implications. If you don't have enough context 
                    from just the title, make reasonable inferences about why it might be trending."""
                },
                {
                    "role": "user",
                    "content": f"Headline: {title}\nURL: {url}\n\nProvide a brief summary:"
                }
            ],
            max_tokens=150,
            temperature=0.7,
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Summary unavailable: {str(e)[:50]}"


def render_header():
    st.markdown("""
    <div class="main-header">
        <h1>⚡ Tech Pulse</h1>
        <p>Your real-time feed of the hottest tech news, powered by AI summaries</p>
    </div>
    """, unsafe_allow_html=True)


def render_stats(stories: list[dict]):
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{len(stories)}</div>
            <div class="stat-label">Stories</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_score = sum(s.get("score", 0) for s in stories)
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{total_score:,}</div>
            <div class="stat-label">Total Points</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_comments = sum(s.get("comments", 0) for s in stories)
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{total_comments:,}</div>
            <div class="stat-label">Comments</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        sources = len(set(s.get("source", "") for s in stories))
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{sources}</div>
            <div class="stat-label">Sources</div>
        </div>
        """, unsafe_allow_html=True)


def render_news_card(story: dict, index: int, openai_api_key: str):
    time_ago = get_time_ago(story.get("time", datetime.now()))
    
    st.markdown(f"""
    <div class="news-card">
        <div class="news-title">
            <a href="{story.get('url', '#')}" target="_blank">{index}. {story.get('title', 'No title')}</a>
        </div>
        <div class="news-meta">
            <span class="source-badge">{story.get('source', 'Unknown')}</span>
            <span class="score-badge">▲ {story.get('score', 0)} points</span>
            <span>💬 {story.get('comments', 0)} comments</span>
            <span>⏱️ {time_ago}</span>
            <span>👤 {story.get('author', 'anonymous')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # AI Summary expander
    if openai_api_key:
        with st.expander("🤖 Get AI Summary"):
            if st.button(f"Generate Summary", key=f"sum_{story.get('id', index)}"):
                with st.spinner("Generating summary..."):
                    summary = summarize_with_ai(
                        story.get("title", ""),
                        story.get("url", ""),
                        openai_api_key
                    )
                    if summary:
                        st.markdown(f"""
                        <div class="news-summary">
                            {summary}
                        </div>
                        """, unsafe_allow_html=True)


def get_time_ago(dt: datetime) -> str:
    now = datetime.now()
    diff = now - dt
    
    if diff.days > 0:
        return f"{diff.days}d ago"
    elif diff.seconds >= 3600:
        return f"{diff.seconds // 3600}h ago"
    elif diff.seconds >= 60:
        return f"{diff.seconds // 60}m ago"
    else:
        return "just now"


def main():
    render_header()
    
    # Sidebar for settings
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        # API Keys
        st.markdown("#### API Keys")
        openai_api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Required for AI summaries. Get one at platform.openai.com",
            value=os.getenv("OPENAI_API_KEY", "")
        )
        
        news_api_key = st.text_input(
            "NewsAPI Key (Optional)",
            type="password",
            help="Adds more tech news sources. Get one at newsapi.org",
            value=os.getenv("NEWS_API_KEY", "")
        )
        
        st.markdown("---")
        
        # Filters
        st.markdown("#### Filters")
        num_stories = st.slider("Number of stories", 10, 50, 25)
        min_score = st.slider("Minimum score", 0, 500, 0)
        
        st.markdown("---")
        
        # Data sources
        st.markdown("#### Data Sources")
        use_hackernews = st.checkbox("Hacker News", value=True)
        use_newsapi = st.checkbox("NewsAPI", value=bool(news_api_key))
        
        st.markdown("---")
        
        if st.button("🔄 Refresh News"):
            st.cache_data.clear()
            st.rerun()
    
    # Fetch news
    all_stories = []
    
    with st.spinner("Fetching the latest tech news..."):
        if use_hackernews:
            hn_stories = fetch_hackernews_top_stories(limit=num_stories)
            all_stories.extend(hn_stories)
        
        if use_newsapi and news_api_key:
            newsapi_stories = fetch_newsapi_tech_news(news_api_key, limit=num_stories // 2)
            all_stories.extend(newsapi_stories)
    
    # Filter by minimum score
    all_stories = [s for s in all_stories if s.get("score", 0) >= min_score]
    
    # Sort by score
    all_stories.sort(key=lambda x: x.get("score", 0), reverse=True)
    
    if not all_stories:
        st.warning("No stories found. Try adjusting your filters or refreshing.")
        return
    
    # Render stats
    render_stats(all_stories)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Render news cards
    st.markdown("### 📰 Top Stories")
    
    for i, story in enumerate(all_stories[:num_stories], 1):
        render_news_card(story, i, openai_api_key)


if __name__ == "__main__":
    main()
