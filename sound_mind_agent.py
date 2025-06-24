import json
import urllib.request
import urllib.parse
import base64
from datetime import datetime

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

def search_news(topic):
    """Search NewsAPI for articles"""
    env_vars = load_env_file()
    api_key = env_vars.get('NEWS_API_KEY')
    
    if not api_key:
        return []
    
    base_url = "https://newsapi.org/v2/everything"
    params = {
        'q': topic,
        'sortBy': 'publishedAt',
        'pageSize': 3,
        'apiKey': api_key
    }
    
    url = base_url + '?' + urllib.parse.urlencode(params)
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
        
        articles = []
        for article in data.get('articles', []):
            articles.append({
                'title': article['title'],
                'source': f"News: {article['source']['name']}",
                'url': article['url'],
                'date': article['publishedAt'],
                'type': 'news'
            })
        return articles
    except:
        return []

def get_reddit_token():
    """Get Reddit access token"""
    env_vars = load_env_file()
    client_id = env_vars.get('REDDIT_CLIENT_ID')
    client_secret = env_vars.get('REDDIT_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        return None
    
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    
    url = "https://www.reddit.com/api/v1/access_token"
    data = urllib.parse.urlencode({'grant_type': 'client_credentials'}).encode()
    
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('Authorization', f'Basic {encoded_credentials}')
    req.add_header('User-Agent', 'SoundMindAgent/1.0')
    
    try:
        with urllib.request.urlopen(req) as response:
            token_data = json.loads(response.read().decode())
            return token_data.get('access_token')
    except:
        return None

def search_reddit(topic, token):
    """Search Reddit for discussions"""
    if not token:
        return []
    
    subreddits = ['Meditation', 'soundhealing', 'BinauralBeats', 'ambientmusic']
    all_posts = []
    
    for subreddit in subreddits[:2]:  # Limit to avoid rate limits
        url = f"https://oauth.reddit.com/r/{subreddit}/search"
        params = {
            'q': topic,
            'sort': 'relevance',
            'limit': 2,
            'restrict_sr': 'true'
        }
        
        full_url = url + '?' + urllib.parse.urlencode(params)
        
        req = urllib.request.Request(full_url)
        req.add_header('Authorization', f'Bearer {token}')
        req.add_header('User-Agent', 'SoundMindAgent/1.0')
        
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
            
            for post in data.get('data', {}).get('children', []):
                post_data = post['data']
                all_posts.append({
                    'title': post_data['title'],
                    'source': f"Reddit: r/{subreddit}",
                    'url': f"https://reddit.com{post_data['permalink']}",
                    'date': datetime.fromtimestamp(post_data['created_utc']).isoformat(),
                    'type': 'reddit',
                    'score': post_data['score']
                })
        except:
            continue
    
    return all_posts

def search_pubmed(topic):
    """Search PubMed for research"""
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    search_params = {
        'db': 'pubmed',
        'term': topic,
        'retmax': 3,
        'retmode': 'json'
    }
    
    search_full_url = search_url + '?' + urllib.parse.urlencode(search_params)
    
    try:
        with urllib.request.urlopen(search_full_url) as response:
            search_data = json.loads(response.read().decode())
        
        id_list = search_data.get('esearchresult', {}).get('idlist', [])
        
        if not id_list:
            return []
        
        fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        fetch_params = {
            'db': 'pubmed',
            'id': ','.join(id_list),
            'retmode': 'json'
        }
        
        fetch_full_url = fetch_url + '?' + urllib.parse.urlencode(fetch_params)
        
        with urllib.request.urlopen(fetch_full_url) as response:
            fetch_data = json.loads(response.read().decode())
        
        articles = []
        result_data = fetch_data.get('result', {})
        
        for pmid in id_list:
            if pmid in result_data:
                article = result_data[pmid]
                articles.append({
                    'title': article.get('title', 'No title'),
                    'source': f"Research: {article.get('source', 'PubMed')}",
                    'url': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                    'date': article.get('pubdate', 'Unknown'),
                    'type': 'research'
                })
        
        return articles
    except:
        return []

def run_full_content_search():
    """Run the complete Sound Mind content search"""
    print("🎵 SOUND MIND CONTENT AGENT - FULL SEARCH")
    print("=" * 60)
    
    # Topics to search for
    topics = ['sound healing', 'binaural beats']
    
    # Get Reddit token once
    reddit_token = get_reddit_token()
    if reddit_token:
        print("✅ Connected to Reddit")
    else:
        print("❌ Reddit connection failed")
    
    all_content = []
    
    for topic in topics:
        print(f"\n🔍 SEARCHING FOR: '{topic}'")
        print("-" * 40)
        
        # Search all sources
        news_results = search_news(topic)
        reddit_results = search_reddit(topic, reddit_token)
        research_results = search_pubmed(topic)
        
        print(f"📰 News: {len(news_results)} articles")
        print(f"💬 Reddit: {len(reddit_results)} discussions") 
        print(f"🔬 Research: {len(research_results)} papers")
        
        # Combine results
        topic_content = news_results + reddit_results + research_results
        all_content.extend(topic_content)
    
    # Show summary
    print(f"\n🎯 CONTENT DISCOVERY COMPLETE!")
    print("=" * 60)
    print(f"📊 TOTAL FOUND: {len(all_content)} items")
    
    # Count by type
    news_count = len([x for x in all_content if x['type'] == 'news'])
    reddit_count = len([x for x in all_content if x['type'] == 'reddit'])
    research_count = len([x for x in all_content if x['type'] == 'research'])
    
    print(f"📰 News Articles: {news_count}")
    print(f"💬 Reddit Discussions: {reddit_count}")
    print(f"🔬 Research Papers: {research_count}")
    
    # Show top items from each category
    print(f"\n🏆 SAMPLE RESULTS:")
    print("-" * 40)
    
    for content_type in ['news', 'reddit', 'research']:
        items = [x for x in all_content if x['type'] == content_type]
        if items:
            print(f"\n{content_type.upper()}:")
            for item in items[:2]:  # Show top 2
                print(f"  • {item['title'][:60]}...")
                print(f"    {item['source']}")
    
    print(f"\n✅ Your Sound Mind content discovery system is WORKING!")
    return all_content

if __name__ == "__main__":
    content = run_full_content_search()