// Sound Mind Content Discovery - JavaScript with Real API Integration
console.log('Sound Mind script loading...');

// Global variables
let searchTerms = ['sound healing', 'binaural beats', 'meditation music'];
let allResults = [];
let displayedResults = [];
let isSearching = false;

// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

console.log('Initial search terms:', searchTerms);

// Function to update the display of search term tags
function updateTermTags() {
    console.log('updateTermTags called with terms:', searchTerms);
    
    const container = document.getElementById('termTags');
    if (!container) {
        console.error('termTags container not found!');
        return;
    }
    
    if (searchTerms.length === 0) {
        container.innerHTML = '<span style="color: rgba(93, 64, 55, 0.6); font-style: italic;">No search terms yet</span>';
        return;
    }
    
    const html = searchTerms.map(term => 
        `<span class="term-tag">${term}<span class="remove-term" onclick="removeTerm('${term}')">&times;</span></span>`
    ).join('');
    
    console.log('Generated HTML for tags:', html);
    container.innerHTML = html;
}

// Function to add a custom search term
function addCustomTerm() {
    console.log('addCustomTerm called');
    
    const input = document.getElementById('customTerm');
    if (!input) {
        console.error('customTerm input not found!');
        return;
    }
    
    const term = input.value.trim();
    console.log('Input value:', term);
    
    if (term && !searchTerms.includes(term)) {
        searchTerms.push(term);
        input.value = '';
        console.log('Added term. New array:', searchTerms);
        updateTermTags();
    } else {
        console.log('Term not added - either empty or duplicate');
    }
}

// Function to remove a search term
function removeTerm(term) {
    console.log('removeTerm called with:', term);
    
    const oldLength = searchTerms.length;
    searchTerms = searchTerms.filter(t => t !== term);
    
    console.log('Removed term. Old length:', oldLength, 'New length:', searchTerms.length);
    console.log('Updated array:', searchTerms);
    
    updateTermTags();
}

// Status message functions
function showStatus(message) {
    const statusMessage = document.getElementById('statusMessage');
    if (statusMessage) {
        statusMessage.innerHTML = `<div class="status-message">${message}</div>`;
    }
}

function hideStatus() {
    const statusMessage = document.getElementById('statusMessage');
    if (statusMessage) {
        statusMessage.innerHTML = '';
    }
}

// Loading display function
function showLoading() {
    const resultsContainer = document.getElementById('resultsContainer');
    if (resultsContainer) {
        resultsContainer.innerHTML = `
            <div class="loading">
                <div class="loading-spinner"></div>
                <p>Discovering real content across multiple sources...</p>
            </div>
        `;
    }
}

// Test API connection
async function testAPIConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/test`);
        const data = await response.json();
        console.log('✅ API Connection Test:', data);
        return true;
    } catch (error) {
        console.error('❌ API Connection Failed:', error);
        showStatus('❌ Cannot connect to API server. Make sure the Python server is running on port 5000.');
        return false;
    }
}

// Main search function with real API
async function performSearch() {
    console.log('performSearch called');
    
    if (isSearching) {
        console.log('Search already in progress, skipping');
        return;
    }
    
    // Test API connection first
    const apiConnected = await testAPIConnection();
    if (!apiConnected) {
        return;
    }
    
    isSearching = true;
    const searchBtn = document.getElementById('searchBtn');
    const searchBtnText = document.getElementById('searchBtnText');
    
    if (searchBtn) searchBtn.disabled = true;
    if (searchBtnText) searchBtnText.textContent = '🔍 Searching...';
    
    showLoading();
    hideStatus();

    try {
        showStatus('🔍 Searching real content sources...');
        
        // Call the real API
        const response = await fetch(`${API_BASE_URL}/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                searchTerms: searchTerms
            })
        });
        
        if (!response.ok) {
            throw new Error(`API request failed: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            allResults = data.results;
            
            // Add snippet property if missing (for consistent display)
            allResults = allResults.map(result => ({
                ...result,
                snippet: result.snippet || `Content from ${result.source} about the search topic.`
            }));
            
            // Shuffle and select top 5 for display
            allResults = shuffleArray(allResults);
            displayedResults = allResults.slice(0, 5);
            
            hideStatus();
            displayResults();
            
            const exportBtn = document.getElementById('exportBtn');
            if (exportBtn) exportBtn.style.display = 'block';
            
            console.log(`✅ Found ${allResults.length} real results!`);
        } else {
            throw new Error(data.error || 'Unknown API error');
        }
        
    } catch (error) {
        showStatus(`❌ Search failed: ${error.message}`);
        console.error('Search error:', error);
        
        // Fallback to mock data if API fails
        console.log('🔄 Falling back to mock data...');
        await performMockSearch();
    } finally {
        isSearching = false;
        if (searchBtn) searchBtn.disabled = false;
        if (searchBtnText) searchBtnText.textContent = '🔍 Search Content';
    }
}

// Fallback mock search (simplified version)
async function performMockSearch() {
    allResults = [
        {
            title: 'Sound Healing Benefits for Mental Health',
            source: 'Demo: Health News',
            snippet: 'Recent studies show promising results for sound therapy in treating anxiety and depression.',
            url: 'https://www.healthline.com/health/sound-therapy',
            type: 'news'
        },
        {
            title: 'My Journey with Binaural Beats',
            source: 'Demo: Reddit Discussion',
            snippet: 'Personal experience using binaural beats for focus and relaxation over 6 months.',
            url: 'https://www.reddit.com/r/Meditation/',
            type: 'reddit'
        }
    ];
    
    displayedResults = allResults;
    displayResults();
    
    const exportBtn = document.getElementById('exportBtn');
    if (exportBtn) exportBtn.style.display = 'block';
}

// Function to display search results
function displayResults() {
    const resultsContainer = document.getElementById('resultsContainer');
    if (!resultsContainer) return;
    
    if (displayedResults.length === 0) {
        resultsContainer.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">🌀</div>
                <h3>No Results Found</h3>
                <p>Try adjusting your search terms or check your API connection.</p>
            </div>
        `;
        return;
    }

    resultsContainer.innerHTML = displayedResults.map((item, index) => `
        <div class="content-item ${item.type}">
            <div class="item-header">
                <h3 class="item-title">${item.title}</h3>
                <button class="remove-item" onclick="removeItem(${index})">&times;</button>
            </div>
            <div class="item-source source-${item.type}">${item.source}</div>
            <p class="item-snippet">${item.snippet}</p>
            <a href="${item.url}" target="_blank" rel="noopener noreferrer" class="item-link">🔗 Read More</a>
        </div>
    `).join('');
}

// Remove a result item and replace with next available
function removeItem(index) {
    displayedResults.splice(index, 1);
    
    const remainingResults = allResults.filter(result => 
        !displayedResults.some(displayed => displayed.title === result.title)
    );
    
    if (remainingResults.length > 0) {
        const replacement = remainingResults[0];
        displayedResults.push(replacement);
    }
    
    displayResults();
}

// Export results to text file
function exportResults() {
    const content = displayedResults.map(item => 
        `Title: ${item.title}\nSource: ${item.source}\nSnippet: ${item.snippet}\nType: ${item.type}\nURL: ${item.url}\n\n`
    ).join('---\n\n');
    
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `sound-mind-content-${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Utility functions
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function shuffleArray(array) {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
}

// Initialize when DOM loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing Sound Mind interface...');
    
    // Initialize search terms display
    updateTermTags();
    
    // Test API connection on startup
    setTimeout(testAPIConnection, 1000);
    
    // Set up event listeners
    const searchBtn = document.getElementById('searchBtn');
    const addTermBtn = document.getElementById('addTermBtn');
    const customTermInput = document.getElementById('customTerm');
    const exportBtn = document.getElementById('exportBtn');
    
    if (searchBtn) {
        searchBtn.addEventListener('click', performSearch);
        console.log('Search button listener added');
    }
    
    if (addTermBtn) {
        addTermBtn.addEventListener('click', addCustomTerm);
        console.log('Add term button listener added');
    }
    
    if (customTermInput) {
        customTermInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                addCustomTerm();
            }
        });
        console.log('Enter key listener added to input');
    }
    
    if (exportBtn) {
        exportBtn.addEventListener('click', exportResults);
        console.log('Export button listener added');
    }
    
    console.log('Sound Mind interface initialized successfully!');
    console.log('Current search terms:', searchTerms);
});