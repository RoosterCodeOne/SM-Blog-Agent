import json
import urllib.request
import urllib.parse
import base64
import ssl
from datetime import datetime, timedelta
import re

# Create SSL context that doesn't verify certificates (for development)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

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

# ============================================================================
# EXISTING SOURCES (NewsAPI, Reddit, PubMed)
# ============================================================================

def search_news(topic):
    """Search NewsAPI for articles"""
    print(f"📰 Searching NewsAPI for: {topic}")
    env_vars = load_env_file()
    api_key = env_vars.get('NEWS_API_KEY')
    
    if not api_key:
        print("❌ No NewsAPI key found!")
        return []
    
    base_url = "https://newsapi.org/v2/everything"
    params = {
        'q': topic,
        'sortBy': 'publishedAt',
        'pageSize': 5,
        'apiKey': api_key
    }
    
    url = base_url + '?' + urllib.parse.urlencode(params)
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ssl_context) as response:
            data = json.loads(response.read().decode())
        
        articles = []
        for article in data.get('articles', []):
            articles.append({
                'title': article['title'],
                'source': f"News: {article['source']['name']}",
                'url': article['url'],
                'date': article['publishedAt'],
                'type': 'news',
                'snippet': article.get('description', 'No description available.')[:200] + "..."
            })
        print(f"   ✅ Found {len(articles)} news articles")
        return articles
    except Exception as e:
        print(f"   ❌ NewsAPI error: {e}")
        return []

def get_reddit_token():
    """Get Reddit access token"""
    print("🔄 Getting Reddit token...")
    env_vars = load_env_file()
    client_id = env_vars.get('REDDIT_CLIENT_ID')
    client_secret = env_vars.get('REDDIT_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("❌ Reddit credentials missing!")
        return None
    
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    
    url = "https://www.reddit.com/api/v1/access_token"
    data = urllib.parse.urlencode({'grant_type': 'client_credentials'}).encode()
    
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('Authorization', f'Basic {encoded_credentials}')
    req.add_header('User-Agent', 'SoundMindAgent/1.0')
    
    try:
        with urllib.request.urlopen(req, context=ssl_context) as response:
            token_data = json.loads(response.read().decode())
            print("   ✅ Reddit token obtained")
            return token_data.get('access_token')
    except Exception as e:
        print(f"   ❌ Reddit token error: {e}")
        return None

def search_reddit(topic, token):
    """Search Reddit for discussions"""
    print(f"💬 Searching Reddit for: {topic}")
    if not token:
        print("   ❌ No Reddit token available")
        return []
    
    subreddits = ['Meditation', 'soundhealing', 'BinauralBeats', 'ambientmusic', 'WeAreTheMusicMakers']
    all_posts = []
    
    for subreddit in subreddits[:3]:  # Limit to avoid rate limits
        url = f"https://oauth.reddit.com/r/{subreddit}/search"
        params = {
            'q': topic,
            'sort': 'relevance',
            'limit': 3,
            'restrict_sr': 'true'
        }
        
        full_url = url + '?' + urllib.parse.urlencode(params)
        
        req = urllib.request.Request(full_url)
        req.add_header('Authorization', f'Bearer {token}')
        req.add_header('User-Agent', 'SoundMindAgent/1.0')
        
        try:
            with urllib.request.urlopen(req, context=ssl_context) as response:
                data = json.loads(response.read().decode())
            
            for post in data.get('data', {}).get('children', []):
                post_data = post['data']
                all_posts.append({
                    'title': post_data['title'],
                    'source': f"Reddit: r/{subreddit}",
                    'url': f"https://reddit.com{post_data['permalink']}",
                    'date': datetime.fromtimestamp(post_data['created_utc']).isoformat(),
                    'type': 'reddit',
                    'score': post_data['score'],
                    'snippet': post_data.get('selftext', 'Reddit discussion thread')[:200] + "..."
                })
        except Exception as e:
            print(f"   ❌ Reddit search error for r/{subreddit}: {e}")
            continue
    
    print(f"   ✅ Found {len(all_posts)} Reddit posts")
    return all_posts

def search_pubmed(topic):
    """Search PubMed for research"""
    print(f"🔬 Searching PubMed for: {topic}")
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    search_params = {
        'db': 'pubmed',
        'term': topic,
        'retmax': 5,
        'retmode': 'json'
    }
    
    search_full_url = search_url + '?' + urllib.parse.urlencode(search_params)
    
    try:
        req = urllib.request.Request(search_full_url)
        with urllib.request.urlopen(req, context=ssl_context) as response:
            search_data = json.loads(response.read().decode())
        
        id_list = search_data.get('esearchresult', {}).get('idlist', [])
        
        if not id_list:
            print(f"   ❌ No PubMed articles found for '{topic}'")
            return []
        
        fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        fetch_params = {
            'db': 'pubmed',
            'id': ','.join(id_list),
            'retmode': 'json'
        }
        
        fetch_full_url = fetch_url + '?' + urllib.parse.urlencode(fetch_params)
        
        req = urllib.request.Request(fetch_full_url)
        with urllib.request.urlopen(req, context=ssl_context) as response:
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
                    'type': 'research',
                    'snippet': f"Research paper published in {article.get('source', 'academic journal')}. Click to read full abstract and details."
                })
        
        print(f"   ✅ Found {len(articles)} research papers")
        return articles
    except Exception as e:
        print(f"   ❌ PubMed error: {e}")
        return []

# ============================================================================
# NEW DATA SOURCES
# ============================================================================

def search_youtube(topic):
    """Search YouTube for videos (using RSS feeds and search)"""
    print(f"📺 Searching YouTube for: {topic}")
    
    try:
        videos = []
        
        # Method 1: Try known working channels with updated IDs
        channels = {
            'Meditative Mind': 'UCN4vyryy6O4GlIXcXTIuZQQ',
            'Jason Stephenson': 'UCNfVZjGzUfUOWjKIwxC_2kw',
            'Michael Sealey': 'UCggB0khNZsT8Oj7M2YQ5d4Q',
            'Soothing Relaxation': 'UCSXm6c-n6lsjtyjvdD0bFVw'
        }
        
        for channel_name, channel_id in channels.items():
            try:
                rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
                
                req = urllib.request.Request(rss_url)
                req.add_header('User-Agent', 'SoundMindAgent/1.0')
                
                with urllib.request.urlopen(req, context=ssl_context, timeout=10) as response:
                    content = response.read().decode()
                
                # Parse XML content for video information
                import re
                
                # Extract video entries
                entry_pattern = r'<entry>(.*?)</entry>'
                entries = re.findall(entry_pattern, content, re.DOTALL)
                
                for entry in entries[:3]:  # Limit to 3 videos per channel
                    # Extract title
                    title_match = re.search(r'<title>(.*?)</title>', entry)
                    # Extract link
                    link_match = re.search(r'<link rel="alternate" href="(.*?)"', entry)
                    # Extract date
                    date_match = re.search(r'<published>(.*?)</published>', entry)
                    
                    if title_match and link_match:
                        title = title_match.group(1).strip()
                        link = link_match.group(1)
                        date = date_match.group(1) if date_match else "Unknown"
                        
                        # Filter videos that mention our topic (case insensitive)
                        topic_words = topic.lower().split()
                        title_lower = title.lower()
                        
                        if any(word in title_lower for word in topic_words):
                            videos.append({
                                'title': title,
                                'source': f"YouTube: {channel_name}",
                                'url': link,
                                'date': date,
                                'type': 'video',
                                'snippet': f"Video content about {topic} from {channel_name}"
                            })
                
                print(f"   ✅ {channel_name}: Found relevant videos")
                
            except Exception as e:
                print(f"   ⚠️  {channel_name}: {str(e)[:50]}...")
                continue
        
        # Method 2: If no results from channels, create some generic search results
        if not videos:
            print(f"   🔄 No RSS results, generating search suggestions...")
            
            # Create direct YouTube search links as fallback
            search_terms = [topic, f"{topic} music", f"{topic} guided"]
            
            for i, search_term in enumerate(search_terms[:2]):  # Limit to 2 suggestions
                encoded_term = urllib.parse.quote_plus(search_term)
                search_url = f"https://www.youtube.com/results?search_query={encoded_term}"
                
                videos.append({
                    'title': f"YouTube search: {search_term}",
                    'source': "YouTube: Search Results",
                    'url': search_url,
                    'date': datetime.now().isoformat(),
                    'type': 'video',
                    'snippet': f"Click to search YouTube directly for '{search_term}' content"
                })
        
        print(f"   ✅ Found {len(videos)} YouTube videos/searches")
        return videos
        
    except Exception as e:
        print(f"   ❌ YouTube search error: {e}")
        
        # Emergency fallback - return search links
        try:
            encoded_topic = urllib.parse.quote_plus(topic)
            search_url = f"https://www.youtube.com/results?search_query={encoded_topic}"
            
            return [{
                'title': f"Search YouTube for '{topic}'",
                'source': "YouTube: Direct Search",
                'url': search_url,
                'date': datetime.now().isoformat(),
                'type': 'video',
                'snippet': f"Click to search YouTube directly for {topic} videos"
            }]
        except:
            return []

def search_arxiv(topic):
    """Search arXiv for academic papers"""
    print(f"📚 Searching arXiv for: {topic}")
    
    try:
        base_url = "http://export.arxiv.org/api/query"
        params = {
            'search_query': f'all:{topic}',
            'start': 0,
            'max_results': 5,
            'sortBy': 'submittedDate',
            'sortOrder': 'descending'
        }
        
        url = base_url + '?' + urllib.parse.urlencode(params)
        
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'SoundMindAgent/1.0')
        
        with urllib.request.urlopen(req, context=ssl_context, timeout=15) as response:
            content = response.read().decode()
        
        # Simple XML parsing for arXiv results
        import re
        
        # Extract paper information using regex
        entry_pattern = r'<entry>(.*?)</entry>'
        title_pattern = r'<title>(.*?)</title>'
        summary_pattern = r'<summary>(.*?)</summary>'
        link_pattern = r'<id>(http://arxiv\.org/abs/.*?)</id>'
        date_pattern = r'<published>(.*?)</published>'
        
        entries = re.findall(entry_pattern, content, re.DOTALL)
        papers = []
        
        for entry in entries:
            title_match = re.search(title_pattern, entry)
            summary_match = re.search(summary_pattern, entry, re.DOTALL)
            link_match = re.search(link_pattern, entry)
            date_match = re.search(date_pattern, entry)
            
            if title_match and link_match:
                title = title_match.group(1).strip()
                summary = summary_match.group(1).strip()[:200] + "..." if summary_match else "No summary available"
                link = link_match.group(1)
                date = date_match.group(1) if date_match else "Unknown"
                
                papers.append({
                    'title': title,
                    'source': "Academic: arXiv",
                    'url': link,
                    'date': date,
                    'type': 'academic',
                    'snippet': summary
                })
        
        print(f"   ✅ Found {len(papers)} arXiv papers")
        return papers
        
    except Exception as e:
        print(f"   ❌ arXiv search error: {e}")
        return []

def search_podcasts(topic):
    """Search for podcasts using iTunes/Apple Podcasts API"""
    print(f"🎙️ Searching Podcasts for: {topic}")
    
    try:
        base_url = "https://itunes.apple.com/search"
        params = {
            'term': topic,
            'media': 'podcast',
            'limit': 5
        }
        
        url = base_url + '?' + urllib.parse.urlencode(params)
        
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'SoundMindAgent/1.0')
        
        with urllib.request.urlopen(req, context=ssl_context, timeout=10) as response:
            data = json.loads(response.read().decode())
        
        podcasts = []
        for result in data.get('results', []):
            podcasts.append({
                'title': result.get('trackName', 'Unknown Podcast'),
                'source': f"Podcast: {result.get('artistName', 'Unknown Artist')}",
                'url': result.get('trackViewUrl', ''),
                'date': result.get('releaseDate', 'Unknown'),
                'type': 'podcast',
                'snippet': result.get('description', f"Podcast about {topic}")[:200] + "..."
            })
        
        print(f"   ✅ Found {len(podcasts)} podcasts")
        return podcasts
        
    except Exception as e:
        print(f"   ❌ Podcast search error: {e}")
        return []

def search_medium(topic):
    """Search Medium articles (using RSS feeds)"""
    print(f"✍️ Searching Medium for: {topic}")
    
    try:
        # Medium RSS search by tag
        search_terms = topic.replace(' ', '-').lower()
        rss_url = f"https://medium.com/feed/tag/{search_terms}"
        
        req = urllib.request.Request(rss_url)
        req.add_header('User-Agent', 'SoundMindAgent/1.0')
        
        try:
            with urllib.request.urlopen(req, context=ssl_context, timeout=10) as response:
                content = response.read().decode()
        except:
            # If tag-specific search fails, try general Medium feed
            rss_url = "https://medium.com/feed/topic/wellness"
            req = urllib.request.Request(rss_url)
            req.add_header('User-Agent', 'SoundMindAgent/1.0')
            with urllib.request.urlopen(req, context=ssl_context, timeout=10) as response:
                content = response.read().decode()
        
        # Simple XML parsing for Medium articles
        import re
        
        title_pattern = r'<title><!\[CDATA\[(.*?)\]\]></title>'
        link_pattern = r'<link>(https://medium\.com/.*?)</link>'
        date_pattern = r'<pubDate>(.*?)</pubDate>'
        description_pattern = r'<description><!\[CDATA\[(.*?)\]\]></description>'
        
        titles = re.findall(title_pattern, content)
        links = re.findall(link_pattern, content)
        dates = re.findall(date_pattern, content)
        descriptions = re.findall(description_pattern, content)
        
        articles = []
        
        # Filter articles that mention our topic
        for i, title in enumerate(titles):
            if any(word.lower() in title.lower() for word in topic.split()) or \
               any(word.lower() in descriptions[i].lower() for word in topic.split() if i < len(descriptions)):
                
                if i < len(links):
                    snippet = descriptions[i][:200] + "..." if i < len(descriptions) else f"Medium article about {topic}"
                    articles.append({
                        'title': title,
                        'source': "Blog: Medium",
                        'url': links[i],
                        'date': dates[i] if i < len(dates) else "Unknown",
                        'type': 'blog',
                        'snippet': snippet
                    })
        
        print(f"   ✅ Found {len(articles)} Medium articles")
        return articles[:3]  # Limit results
        
    except Exception as e:
        print(f"   ❌ Medium search error: {e}")
        return []

def search_github(topic):
    """Search GitHub repositories"""
    print(f"💻 Searching GitHub for: {topic}")
    
    try:
        base_url = "https://api.github.com/search/repositories"
        params = {
            'q': topic,
            'sort': 'updated',
            'order': 'desc',
            'per_page': 5
        }
        env_vars = load_env_file()
        github_token = env_vars.get('GITHUB_TOKEN')        
        
        url = base_url + '?' + urllib.parse.urlencode(params)

        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'SoundMindAgent/1.0')
        req.add_header('Accept', 'application/vnd.github.v3+json')
        
        if github_token:
            req.add_header('Authorization', f'token {github_token}')
        
        with urllib.request.urlopen(req, context=ssl_context, timeout=10) as response:
            data = json.loads(response.read().decode())
        
        repos = []
        for repo in data.get('items', []):
            repos.append({
                'title': repo['name'],
                'source': f"GitHub: {repo['owner']['login']}",
                'url': repo['html_url'],
                'date': repo['updated_at'],
                'type': 'code',
                'snippet': repo.get('description', f"GitHub repository related to {topic}")[:200] + "...",
                'stars': repo['stargazers_count']
            })
        
        print(f"   ✅ Found {len(repos)} GitHub repositories")
        return repos
        
    except Exception as e:
        print(f"   ❌ GitHub search error: {e}")
        return []

def search_google_scholar(topic):
    """Search Google Scholar (simplified scraping approach)"""
    print(f"🎓 Searching Google Scholar for: {topic}")
    
    try:
        # Note: This is a simplified approach
        # For production, consider using scholarly library or Serpapi
        
        query = urllib.parse.quote_plus(topic)
        url = f"https://scholar.google.com/scholar?q={query}&hl=en&num=5"
        
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (compatible; SoundMindAgent/1.0)')
        
        with urllib.request.urlopen(req, context=ssl_context, timeout=15) as response:
            content = response.read().decode()
        
        # Simple extraction (very basic - real implementation would need proper parsing)
        papers = []
        
        # For now, return a placeholder indicating Google Scholar integration
        papers.append({
            'title': f"Google Scholar results for '{topic}'",
            'source': "Academic: Google Scholar",
            'url': url,
            'date': datetime.now().isoformat(),
            'type': 'academic',
            'snippet': f"Click to search Google Scholar directly for academic papers about {topic}"
        })
        
        print(f"   ✅ Generated Google Scholar search link")
        return papers
        
    except Exception as e:
        print(f"   ❌ Google Scholar search error: {e}")
        return []

# ============================================================================
# ENHANCED SEARCH ORCHESTRATOR
# ============================================================================

def search_all_sources(topic, reddit_token=None):
    """Search all available data sources for a topic"""
    print(f"\n🔍 COMPREHENSIVE SEARCH FOR: '{topic}'")
    print("-" * 50)
    
    all_results = []
    
    # Original sources
    try:
        news_results = search_news(topic)
        all_results.extend(news_results)
    except Exception as e:
        print(f"❌ News search failed: {e}")
    
    try:
        reddit_results = search_reddit(topic, reddit_token)
        all_results.extend(reddit_results)
    except Exception as e:
        print(f"❌ Reddit search failed: {e}")
    
    try:
        pubmed_results = search_pubmed(topic)
        all_results.extend(pubmed_results)
    except Exception as e:
        print(f"❌ PubMed search failed: {e}")
    
    # New sources
    try:
        youtube_results = search_youtube(topic)
        all_results.extend(youtube_results)
    except Exception as e:
        print(f"❌ YouTube search failed: {e}")
    
    try:
        arxiv_results = search_arxiv(topic)
        all_results.extend(arxiv_results)
    except Exception as e:
        print(f"❌ arXiv search failed: {e}")
    
    try:
        podcast_results = search_podcasts(topic)
        all_results.extend(podcast_results)
    except Exception as e:
        print(f"❌ Podcast search failed: {e}")
    
    try:
        medium_results = search_medium(topic)
        all_results.extend(medium_results)
    except Exception as e:
        print(f"❌ Medium search failed: {e}")
    
    try:
        github_results = search_github(topic)
        all_results.extend(github_results)
    except Exception as e:
        print(f"❌ GitHub search failed: {e}")
    
    try:
        scholar_results = search_google_scholar(topic)
        all_results.extend(scholar_results)
    except Exception as e:
        print(f"❌ Google Scholar search failed: {e}")
    
    return all_results

def run_enhanced_content_search():
    """Run the enhanced Sound Mind content search with all sources"""
    print("🎵 SOUND MIND ENHANCED CONTENT AGENT")
    print("=" * 60)
    
    # Topics to search for
    topics = ['sound healing', 'binaural beats']
    
    # Get Reddit token once
    reddit_token = get_reddit_token()
    
    all_content = []
    
    for topic in topics:
        topic_results = search_all_sources(topic, reddit_token)
        all_content.extend(topic_results)
    
    # Show comprehensive summary
    print(f"\n🎯 ENHANCED CONTENT DISCOVERY COMPLETE!")
    print("=" * 60)
    print(f"📊 TOTAL FOUND: {len(all_content)} items")
    
    # Count by type
    type_counts = {}
    for item in all_content:
        item_type = item['type']
        type_counts[item_type] = type_counts.get(item_type, 0) + 1
    
    print(f"\n📈 BREAKDOWN BY SOURCE TYPE:")
    for content_type, count in sorted(type_counts.items()):
        emoji_map = {
            'news': '📰',
            'reddit': '💬', 
            'research': '🔬',
            'video': '📺',
            'academic': '📚',
            'podcast': '🎙️',
            'blog': '✍️',
            'code': '💻'
        }
        emoji = emoji_map.get(content_type, '📄')
        print(f"{emoji} {content_type.title()}: {count}")
    
    # Show sample from each type
    print(f"\n🏆 SAMPLE RESULTS BY TYPE:")
    print("-" * 40)
    
    for content_type in type_counts.keys():
        items = [x for x in all_content if x['type'] == content_type]
        if items:
            print(f"\n{content_type.upper()}:")
            for item in items[:2]:  # Show top 2
                print(f"  • {item['title'][:60]}...")
                print(f"    {item['source']}")
    
    print(f"\n✅ Your enhanced Sound Mind system now searches {len(type_counts)} different content types!")
    return all_content

if __name__ == "__main__":
    content = run_enhanced_content_search()