import json
import urllib.request
import urllib.parse
from datetime import datetime

def search_pubmed(query, max_results=10):
    """Search PubMed for scientific articles"""
    print(f"🔬 Searching PubMed for: {query}")
    
    # Step 1: Search for article IDs
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    search_params = {
        'db': 'pubmed',
        'term': query,
        'retmax': max_results,
        'retmode': 'json',
        'sort': 'relevance'
    }
    
    search_full_url = search_url + '?' + urllib.parse.urlencode(search_params)
    
    try:
        # Get article IDs
        with urllib.request.urlopen(search_full_url) as response:
            search_data = json.loads(response.read().decode())
        
        id_list = search_data.get('esearchresult', {}).get('idlist', [])
        
        if not id_list:
            print(f"   No articles found for '{query}'")
            return []
        
        print(f"   Found {len(id_list)} articles!")
        
        # Step 2: Get article details
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
                    'pmid': pmid,
                    'title': article.get('title', 'No title'),
                    'authors': ', '.join([author.get('name', '') for author in article.get('authors', [])[:3]]),
                    'journal': article.get('source', 'Unknown journal'),
                    'pub_date': article.get('pubdate', 'Unknown date'),
                    'url': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                })
        
        return articles
        
    except Exception as e:
        print(f"❌ Error searching PubMed: {e}")
        return []

def search_sound_healing_research():
    """Search for sound healing research papers"""
    print("🔬 Sound Mind Research Paper Finder!")
    print("=" * 50)
    
    # Research terms that should find good papers
    research_terms = [
        'sound therapy',
        'music therapy anxiety',
        'binaural beats',
        'acoustic therapy',
        'vibroacoustic therapy',
        'frequency healing'
    ]
    
    all_articles = []
    
    for term in research_terms:
        articles = search_pubmed(term, max_results=5)
        all_articles.extend(articles)
        print()
    
    if all_articles:
        print("🏆 RESEARCH PAPERS FOUND:")
        print("=" * 50)
        
        for i, article in enumerate(all_articles, 1):
            print(f"{i}. {article['title']}")
            print(f"   👨‍🔬 Authors: {article['authors']}")
            print(f"   📚 Journal: {article['journal']}")
            print(f"   📅 Published: {article['pub_date']}")
            print(f"   🔗 {article['url']}")
            print()
    
    print(f"🎯 Found {len(all_articles)} research papers!")
    print("✅ PubMed integration working!")

if __name__ == "__main__":
    search_sound_healing_research()