# Tech News Summarizer

A simple web app that pulls trending tech news from Hacker News and NewsAPI, with optional AI-powered summaries.

## Setup

```bash
# Clone and setup
git clone https://github.com/dezhouc2/tech-news-app.git
cd tech-news-app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add your API keys (optional but recommended)
cp env.example.txt .env
# Edit .env with your keys

# Run
streamlit run app.py
```

The app opens at `http://localhost:8501`

## API Keys

- **OpenAI** (for AI summaries): Get one at https://platform.openai.com/api-keys
- **NewsAPI** (optional, for more sources): https://newsapi.org/register

The app works without any keys - Hacker News doesn't require auth. Keys just enable extra features.

## How it works

The app fetches top stories from Hacker News (and optionally NewsAPI), displays them in a nice UI, and lets you generate AI summaries for any article using GPT-4o-mini.

I used Streamlit because it's fast to build with and handles the UI/state management out of the box. The main tradeoff is less control over styling compared to a React app, but for a news reader it works well.

Data is cached for 5 minutes to avoid hammering the APIs.

## What I'd add with more time

- Cache the AI summaries so you don't regenerate them
- Add more sources (Reddit, TechCrunch RSS)
- Email digest feature
- Better error handling for rate limits

## Tech stack

- Python / Streamlit
- OpenAI API (gpt-4o-mini)
- Hacker News API
- NewsAPI (optional)

## AI tools used

I used Claude to help with initial scaffolding, CSS styling, and debugging some API issues. The architecture decisions and final implementation were my own.

## Deploy

Push to GitHub, then connect to [Streamlit Cloud](https://share.streamlit.io) - it's free and takes about 2 minutes.
