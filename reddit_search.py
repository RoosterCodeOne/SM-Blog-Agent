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

def get_reddit_token():
    """Get access token from Reddit"""
    env_vars = load_env_file()
    client_id = env_vars.get('REDDIT_CLIENT_ID')
    client_secret = env_vars.get('REDDIT_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("❌ Reddit credentials not found in .env file!")
        return None
    
    # Create basic auth header
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    
    # Request token
    url = "https://www.reddit.com/api/v1/access_token"
    data = urllib.parse.urlencode({
        'grant_type': 'client_credentials'
    }).encode()
    
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('Authorization', f'Basic {encoded_credentials}')
    req.add_header('User-Agent', 'SoundMindAgent/1.0')
    
    try:
        with urllib.request.urlopen(req) as response:
            token_data = json.loads(response.read().decode())
            return token_data.get('access_token')
    except Exception as e:
        print(f"❌ Error getting Reddit token: {e}")
        return None

def search_reddit_subreddit(subreddit, query, token, limit=10):
    """Search a specific subreddit"""
    print(f"🔍 Searching r/{subreddit} for: {query}")
    
    # Build search URL
    base_url = f"https://oauth.reddit.com/r/{subreddit}/search"
    params = {
        'q': query,
        'sort': 'relevance',
        'limit': limit,
        'restrict_sr': 'true'  # Restrict to this subreddit
    }
    
    url = base_url + '?' + urllib.parse.urlencode(params)
    
    # Make request with token
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'Bearer {token}')
    req.add_header('User-Agent', 'SoundMindAgent/1.0')
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
        posts = data.get('data', {}).get('children', [])
        results = []
        
        for post in posts:
            post_data = post['data']
            results.append({
                'title': post_data['title'],
                'score': post_data['score'],
                'num_comments': post_data['num_comments'],
                'created': datetime.fromtimestamp(post_data['created_utc']),
                'url': f"https://reddit.com{post_data['permalink']}",
                'selftext': post_data.get('selftext', '')[:200] + "..." if post_data.get('selftext') else '',
                'subreddit': subreddit
            })
        
        return results
        
    except Exception as e:
        print(f"❌ Error searching r/{subreddit}: {e}")
        return []

def search_sound_healing_topics():
    """Search multiple subreddits for sound healing content"""
    print("🎵 Sound Mind Reddit Searcher!")
    print("=" * 50)
    
    # Get Reddit access token
    token = get_reddit_token()
    if not token:
        print("❌ Could not get Reddit access token")
        return
    
    print("✅ Connected to Reddit API!")
    print()
    
    # Subreddits related to sound healing
    subreddits = [
        'Meditation',
        'soundhealing',
        'BinauralBeats',
        'WeAreTheMusicMakers',
        'ambientmusic',
        'psychology',
        'neuroscience',
        'wellness'
    ]
    
    # Search terms
    search_terms = [
        'sound healing',
        'frequency healing', 
        'binaural beats',
        'meditation music',
        'sound therapy'
    ]
    
    all_results = []
    
    for term in search_terms[:2]:  # Start with just 2 terms to avoid rate limits
        print(f"🔍 Searching for: '{term}'")
        print("-" * 30)
        
        for subreddit in subreddits[:4]:  # Start with 4 subreddits
            results = search_reddit_subreddit(subreddit, term, token, limit=3)
            
            if results:
                print(f"✅ r/{subreddit}: Found {len(results)} posts")
                for result in results:
                    print(f"   • {result['title'][:60]}... (Score: {result['score']}, Comments: {result['num_comments']})")
                all_results.extend(results)
            else:
                print(f"   r/{subreddit}: No results")
        
        print()
    
    # Show top results
    if all_results:
        print("🏆 TOP DISCUSSIONS:")
        print("=" * 50)
        
        # Sort by score (upvotes)
        top_results = sorted(all_results, key=lambda x: x['score'], reverse=True)[:10]
        
        for i, result in enumerate(top_results, 1):
            print(f"{i}. {result['title']}")
            print(f"   📍 r/{result['subreddit']} | 👍 {result['score']} | 💬 {result['num_comments']} comments")
            print(f"   🕒 {result['created'].strftime('%Y-%m-%d')}")
            print(f"   🔗 {result['url']}")
            if result['selftext']:
                print(f"   📝 {result['selftext']}")
            print()
    
    print(f"🎯 Found {len(all_results)} total discussions!")
    print("✅ Reddit integration working!")

if __name__ == "__main__":
    search_sound_healing_topics()