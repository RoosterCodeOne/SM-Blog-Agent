import json
import os
from datetime import datetime

# Simple way to load environment variables without extra libraries
def load_env_file():
    """Load variables from .env file"""
    env_vars = {}
    try:
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value
    except FileNotFoundError:
        print("❌ .env file not found!")
    return env_vars

def search_real_news(topic):
    """Search for real news using NewsAPI"""
    print(f"🔍 Searching for real news about: {topic}")
    
    # Load API key
    env_vars = load_env_file()
    api_key = env_vars.get('NEWS_API_KEY')
    
    if not api_key:
        print("❌ No API key found! Check your .env file.")
        return
    
    # We'll use urllib (built into Python) instead of requests
    import urllib.request
    import urllib.parse
    
    # Build the URL
    base_url = "https://newsapi.org/v2/everything"
    params = {
        'q': topic,
        'sortBy': 'publishedAt',
        'pageSize': 5,
        'apiKey': api_key
    }
    
    url = base_url + '?' + urllib.parse.urlencode(params)
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            
        articles = data.get('articles', [])
        print(f"✅ Found {len(articles)} articles!\n")
        
        for i, article in enumerate(articles, 1):
            print(f"{i}. {article['title']}")
            print(f"   Source: {article['source']['name']}")
            print(f"   Published: {article['publishedAt']}")
            print(f"   URL: {article['url']}")
            print()
            
    except Exception as e:
        print(f"❌ Error: {e}")

# Test it!
if __name__ == "__main__":
    print("🎵 Sound Mind REAL News Searcher!")
    print("=" * 50)
    
    topics = ["sound healing", "binaural beats", "meditation music"]
    
    for topic in topics:
        search_real_news(topic)
        print("-" * 50)
    
    print("🎯 Success! Your first real API is working!")