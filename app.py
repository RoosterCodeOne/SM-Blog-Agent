from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import sys

# Import your existing API functions
from sound_mind_agent import search_news, get_reddit_token, search_reddit, search_pubmed

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
        
        print(f"🔍 API Search request for terms: {search_terms}")
        
        all_results = []
        
        for term in search_terms:
            print(f"   Searching for: {term}")
            
            # Search news
            try:
                news_results = search_news(term)
                print(f"   📰 News: {len(news_results)} results")
                all_results.extend(news_results)
            except Exception as e:
                print(f"   ❌ News search failed: {e}")
            
            # Search Reddit
            try:
                reddit_results = search_reddit(term, reddit_token)
                print(f"   💬 Reddit: {len(reddit_results)} results")
                all_results.extend(reddit_results)
            except Exception as e:
                print(f"   ❌ Reddit search failed: {e}")
            
            # Search PubMed
            try:
                research_results = search_pubmed(term)
                print(f"   🔬 Research: {len(research_results)} results")
                all_results.extend(research_results)
            except Exception as e:
                print(f"   ❌ PubMed search failed: {e}")
        
        print(f"🎯 Total results found: {len(all_results)}")
        
        return jsonify({
            'success': True,
            'results': all_results,
            'total_count': len(all_results)
        })
        
    except Exception as e:
        print(f"❌ Search API error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/test', methods=['GET'])
def api_test():
    """Test endpoint to verify API is working"""
    return jsonify({
        'message': 'Sound Mind API is working!',
        'reddit_connected': reddit_token is not None
    })

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

if __name__ == '__main__':
    print("🎵 Starting Sound Mind API Server...")
    print("=" * 50)
    
    # Initialize connections
    initialize_reddit()
    
    print("🚀 Server starting on http://localhost:5000")
    print("📂 Serving files from current directory")
    print("🔗 API endpoints available at /api/...")
    print("=" * 50)
    
    # Run the server
    app.run(debug=True, host='0.0.0.0', port=5000)