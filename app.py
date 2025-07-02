from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import sys

# Import your enhanced API functions
from sound_mind_agent import (
    search_news, get_reddit_token, search_reddit, search_pubmed,
    search_youtube, search_arxiv, search_podcasts, search_medium, 
    search_github, search_google_scholar, search_all_sources
)

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from your frontend

# Store Reddit token globally to avoid repeated requests
reddit_token = None

def initialize_reddit():
    """Initialize Reddit token once at startup"""
    global reddit_token
    print("🔄 Initializing Reddit connection...")
    reddit_token = get_reddit_token()
    if reddit_token:
        print("✅ Reddit connected successfully!")
    else:
        print("❌ Reddit connection failed - check your .env file")

@app.route('/')
def serve_index():
    """Serve your main HTML file"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS)"""
    return send_from_directory('.', filename)

@app.route('/api/search', methods=['POST'])
def api_search():
    """Main search endpoint that combines all sources"""
    try:
        data = request.get_json()
        search_terms = data.get('searchTerms', [])
        
        if not search_terms:
            return jsonify({'error': 'No search terms provided'}), 400
        
        print(f"🔍 Enhanced API Search request for terms: {search_terms}")
        
        all_results = []
        
        for term in search_terms:
            print(f"   Searching all sources for: {term}")
            
            # Use the enhanced search function that searches all sources
            term_results = search_all_sources(term, reddit_token)
            all_results.extend(term_results)
        
        print(f"🎯 Total results found across all sources: {len(all_results)}")
        
        # Add some metadata about source diversity
        source_types = set(result['type'] for result in all_results)
        
        return jsonify({
            'success': True,
            'results': all_results,
            'total_count': len(all_results),
            'source_types': list(source_types),
            'sources_searched': len(source_types)
        })
        
    except Exception as e:
        print(f"❌ Enhanced Search API error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/test', methods=['GET'])
def api_test():
    """Test endpoint to verify API is working"""
    return jsonify({
        'message': 'Sound Mind Enhanced API is working!',
        'reddit_connected': reddit_token is not None,
        'available_sources': [
            'NewsAPI', 'Reddit', 'PubMed', 'YouTube', 
            'arXiv', 'Podcasts', 'Medium', 'GitHub', 'Google Scholar'
        ]
    })

# Individual source endpoints for testing
@app.route('/api/search/news/<term>')
def api_search_news(term):
    """Search only news for a specific term"""
    try:
        results = search_news(term)
        return jsonify({'success': True, 'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search/reddit/<term>')
def api_search_reddit(term):
    """Search only Reddit for a specific term"""
    try:
        results = search_reddit(term, reddit_token)
        return jsonify({'success': True, 'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search/research/<term>')
def api_search_research(term):
    """Search only research papers for a specific term"""
    try:
        results = search_pubmed(term)
        return jsonify({'success': True, 'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search/youtube/<term>')
def api_search_youtube(term):
    """Search only YouTube for a specific term"""
    try:
        results = search_youtube(term)
        return jsonify({'success': True, 'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search/arxiv/<term>')
def api_search_arxiv(term):
    """Search only arXiv for a specific term"""
    try:
        results = search_arxiv(term)
        return jsonify({'success': True, 'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search/podcasts/<term>')
def api_search_podcasts(term):
    """Search only podcasts for a specific term"""
    try:
        results = search_podcasts(term)
        return jsonify({'success': True, 'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search/medium/<term>')
def api_search_medium(term):
    """Search only Medium for a specific term"""
    try:
        results = search_medium(term)
        return jsonify({'success': True, 'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search/github/<term>')
def api_search_github(term):
    """Search only GitHub for a specific term"""
    try:
        results = search_github(term)
        return jsonify({'success': True, 'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search/scholar/<term>')
def api_search_scholar(term):
    """Search only Google Scholar for a specific term"""
    try:
        results = search_google_scholar(term)
        return jsonify({'success': True, 'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sources', methods=['GET'])
def api_get_sources():
    """Get information about all available data sources"""
    sources = {
        'news': {
            'name': 'NewsAPI',
            'description': 'Latest news articles from various publications',
            'type': 'news',
            'requires_api_key': True
        },
        'reddit': {
            'name': 'Reddit',
            'description': 'Community discussions and user experiences',
            'type': 'reddit',
            'requires_api_key': True
        },
        'pubmed': {
            'name': 'PubMed',
            'description': 'Peer-reviewed medical and scientific research',
            'type': 'research',
            'requires_api_key': False
        },
        'youtube': {
            'name': 'YouTube',
            'description': 'Video content from selected channels',
            'type': 'video',
            'requires_api_key': False
        },
        'arxiv': {
            'name': 'arXiv',
            'description': 'Preprint academic papers',
            'type': 'academic',
            'requires_api_key': False
        },
        'podcasts': {
            'name': 'iTunes/Apple Podcasts',
            'description': 'Podcast episodes and shows',
            'type': 'podcast',
            'requires_api_key': False
        },
        'medium': {
            'name': 'Medium',
            'description': 'Blog articles and personal experiences',
            'type': 'blog',
            'requires_api_key': False
        },
        'github': {
            'name': 'GitHub',
            'description': 'Open source projects and code repositories',
            'type': 'code',
            'requires_api_key': False
        },
        'scholar': {
            'name': 'Google Scholar',
            'description': 'Academic papers and citations',
            'type': 'academic',
            'requires_api_key': False
        }
    }
    
    return jsonify({
        'sources': sources,
        'total_sources': len(sources)
    })

@app.route('/api/search/bulk', methods=['POST'])
def api_bulk_search():
    """Search multiple sources simultaneously with detailed breakdown"""
    try:
        data = request.get_json()
        search_terms = data.get('searchTerms', [])
        selected_sources = data.get('sources', [])  # Allow filtering by source
        
        if not search_terms:
            return jsonify({'error': 'No search terms provided'}), 400
        
        print(f"🔍 Bulk search for terms: {search_terms}")
        if selected_sources:
            print(f"   Limited to sources: {selected_sources}")
        
        results_by_source = {}
        all_results = []
        
        for term in search_terms:
            print(f"   Processing term: {term}")
            
            # Search each source individually for detailed breakdown
            source_functions = {
                'news': lambda: search_news(term),
                'reddit': lambda: search_reddit(term, reddit_token),
                'pubmed': lambda: search_pubmed(term),
                'youtube': lambda: search_youtube(term),
                'arxiv': lambda: search_arxiv(term),
                'podcasts': lambda: search_podcasts(term),
                'medium': lambda: search_medium(term),
                'github': lambda: search_github(term),
                'scholar': lambda: search_google_scholar(term)
            }
            
            for source_name, search_func in source_functions.items():
                # Skip if user specified sources and this isn't included
                if selected_sources and source_name not in selected_sources:
                    continue
                    
                try:
                    source_results = search_func()
                    if source_name not in results_by_source:
                        results_by_source[source_name] = []
                    results_by_source[source_name].extend(source_results)
                    all_results.extend(source_results)
                    print(f"     {source_name}: {len(source_results)} results")
                except Exception as e:
                    print(f"     {source_name}: Error - {e}")
                    if source_name not in results_by_source:
                        results_by_source[source_name] = []
        
        # Calculate statistics
        total_results = len(all_results)
        source_stats = {
            source: len(results) for source, results in results_by_source.items()
        }
        
        return jsonify({
            'success': True,
            'results': all_results,
            'results_by_source': results_by_source,
            'statistics': {
                'total_results': total_results,
                'sources_searched': len(results_by_source),
                'results_per_source': source_stats,
                'search_terms': search_terms
            }
        })
        
    except Exception as e:
        print(f"❌ Bulk search error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🎵 Starting Sound Mind Enhanced API Server...")
    print("=" * 60)
    
    # Initialize connections
    initialize_reddit()
    
    print("🚀 Server starting on http://localhost:5000")
    print("📂 Serving files from current directory")
    print("🔗 Enhanced API endpoints:")
    print("   /api/search - Search all sources")
    print("   /api/search/bulk - Detailed multi-source search")
    print("   /api/sources - Get source information")
    print("   /api/search/[source]/[term] - Search individual sources")
    print("=" * 60)
    
    # Run the server
    app.run(debug=True, host='0.0.0.0', port=5000)