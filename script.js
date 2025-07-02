// Enhanced Sound Mind Content Discovery - JavaScript with Multiple Sources
console.log('Enhanced Sound Mind script loading...');

// Global variables
let searchTerms = ['sound healing', 'binaural beats', 'meditation music'];
let allResults = [];
let displayedResults = [];
let isSearching = false;
let availableSources = [];
let selectedSources = [];
let searchMode = 'comprehensive'; // 'comprehensive' or 'selective'

// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Source configuration with emojis and colors
const sourceConfig = {
    'news': { emoji: '📰', name: 'News', color: '#ff6b6b' },
    'reddit': { emoji: '💬', name: 'Reddit', color: '#ff9500' },
    'research': { emoji: '🔬', name: 'Research', color: '#4ecdc4' },
    'video': { emoji: '📺', name: 'YouTube', color: '#ff4757' },
    'academic': { emoji: '📚', name: 'Academic', color: '#3742fa' },
    'podcast': { emoji: '🎙️', name: 'Podcasts', color: '#2ed573' },
    'blog': { emoji: '✍️', name: 'Blogs', color: '#ffa502' },
    'code': { emoji: '💻', name: 'Code', color: '#5f27cd' }
};

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

// Function to create source selector UI
function createSourceSelector() {
    const searchWidget = document.querySelector('.search-widget');
    if (!searchWidget) return;
    
    // Create search mode selector
    const modeSelector = document.createElement('div');
    modeSelector.className = 'search-mode';
    modeSelector.innerHTML = `
        <div class="mode-buttons">
            <button class="mode-button active" onclick="setSearchMode('comprehensive')">
                🔍 Search All Sources
            </button>
            <button class="mode-button" onclick="setSearchMode('selective')">
                ⚙️ Select Sources
            </button>
        </div>
    `;
    
    // Create source selector (initially hidden)
    const sourceSelector = document.createElement('div');
    sourceSelector.className = 'source-selector';
    sourceSelector.id = 'sourceSelector';
    sourceSelector.style.display = 'none';
    sourceSelector.innerHTML = `
        <h4>Select Data Sources:</h4>
        <div class="source-checkboxes" id="sourceCheckboxes">
            <!-- Will be populated dynamically -->
        </div>
    `;
    
    // Insert after search controls
    const searchControls = searchWidget.querySelector('.search-controls');
    searchControls.parentNode.insertBefore(modeSelector, searchControls.nextSibling);
    searchControls.parentNode.insertBefore(sourceSelector, modeSelector.nextSibling);
}

// Function to set search mode
function setSearchMode(mode) {
    searchMode = mode;
    
    // Update button states
    document.querySelectorAll('.mode-button').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    const sourceSelector = document.getElementById('sourceSelector');
    if (sourceSelector) {
        sourceSelector.style.display = mode === 'selective' ? 'block' : 'none';
    }
}

// Function to populate source checkboxes
function populateSourceSelector(sources) {
    const container = document.getElementById('sourceCheckboxes');
    if (!container || !sources) return;
    
    availableSources = Object.keys(sources);
    selectedSources = [...availableSources]; // Select all by default
    
    container.innerHTML = availableSources.map(sourceKey => {
        const source = sources[sourceKey];
        const config = sourceConfig[source.type] || { emoji: '📄', name: source.name };
        
        return `
            <div class="source-checkbox">
                <input type="checkbox" id="source-${sourceKey}" checked onchange="toggleSource('${sourceKey}')">
                <label for="source-${sourceKey}">
                    ${config.emoji} ${config.name}
                </label>
            </div>
        `;
    }).join('');
}

// Function to toggle source selection
function toggleSource(sourceKey) {
    const checkbox = document.getElementById(`source-${sourceKey}`);
    if (checkbox.checked) {
        if (!selectedSources.includes(sourceKey)) {
            selectedSources.push(sourceKey);
        }
    } else {
        selectedSources = selectedSources.filter(s => s !== sourceKey);
    }
    console.log('Selected sources:', selectedSources);
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

// Enhanced loading display with source indicators
function showEnhancedLoading() {
    const resultsContainer = document.getElementById('resultsContainer');
    if (resultsContainer) {
        const sourcesToSearch = searchMode === 'selective' ? selectedSources : availableSources;
        
        const sourceLoaders = sourcesToSearch.map(sourceKey => {
            const config = sourceConfig[sourceKey] || { emoji: '📄', name: sourceKey };
            return `
                <div class="source-loader">
                    <div class="mini-spinner"></div>
                    ${config.emoji} Searching ${config.name}...
                </div>
            `;
        }).join('');
        
        resultsContainer.innerHTML = `
            <div class="loading">
                <div class="loading-spinner"></div>
                <p>Discovering content across multiple sources...</p>
                <div class="source-loading">
                    ${sourceLoaders}
                </div>
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

// Load available sources
async function loadAvailableSources() {
    try {
        const response = await fetch(`${API_BASE_URL}/sources`);
        const data = await response.json();
        console.log('Available sources:', data);
        populateSourceSelector(data.sources);
        return data.sources;
    } catch (error) {
        console.error('Failed to load sources:', error);
        return null;
    }
}

// Enhanced search function
async function performEnhancedSearch() {
    console.log('performEnhancedSearch called');
    
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
    
    showEnhancedLoading();
    hideStatus();

    try {
        showStatus('🔍 Searching enhanced content sources...');
        
        // Determine which endpoint to use
        const endpoint = searchMode === 'selective' ? 'bulk' : 'search';
        const requestBody = {
            searchTerms: searchTerms
        };
        
        if (searchMode === 'selective') {
            requestBody.sources = selectedSources;
        }
        
        // Call the enhanced API
        const response = await fetch(`${API_BASE_URL}/${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
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
            
            // Shuffle and select for display
            allResults = shuffleArray(allResults);
            displayedResults = allResults.slice(0, 8); // Show more results
            
            hideStatus();
            displayEnhancedResults(data.statistics);
            
            const exportBtn = document.getElementById('exportBtn');
            if (exportBtn) exportBtn.style.display = 'block';
            
            console.log(`✅ Found ${allResults.length} results across multiple sources!`);
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

// Enhanced results display with statistics
function displayEnhancedResults(statistics) {
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

    // Create statistics display
    const statsHtml = createStatsDisplay(statistics);
    
    // Create results HTML
    const resultsHtml = displayedResults.map((item, index) => {
        const config = sourceConfig[item.type] || { emoji: '📄', name: item.type };
        
        // Format additional metadata
        const metadata = [];
        if (item.score) metadata.push(`<span class="item-score">Score: ${item.score}</span>`);
        if (item.stars) metadata.push(`<span class="item-stars">⭐ ${item.stars}</span>`);
        
        const metadataHtml = metadata.length > 0 ? 
            `<div class="item-extra-info">${metadata.join('')}</div>` : '';
        
        return `
            <div class="content-item ${item.type}">
                <div class="item-header">
                    <h3 class="item-title">${item.title}</h3>
                    <button class="remove-item" onclick="removeItem(${index})">&times;</button>
                </div>
                <div class="item-source source-${item.type}">${config.emoji} ${item.source}</div>
                <p class="item-snippet">${item.snippet}</p>
                <a href="${item.url}" target="_blank" rel="noopener noreferrer" class="item-link">🔗 Read More</a>
                <div class="item-metadata">
                    <span class="item-date">${formatDate(item.date)}</span>
                    ${metadataHtml}
                </div>
            </div>
        `;
    }).join('');

    resultsContainer.innerHTML = statsHtml + resultsHtml;
}

// Create statistics display
function createStatsDisplay(statistics) {
    if (!statistics) return '';
    
    const typeStats = {};
    displayedResults.forEach(item => {
        typeStats[item.type] = (typeStats[item.type] || 0) + 1;
    });
    
    const statsItems = Object.entries(typeStats).map(([type, count]) => {
        const config = sourceConfig[type] || { emoji: '📄', name: type };
        return `
            <div class="stat-item">
                ${config.emoji} ${config.name}
                <span class="stat-count">${count}</span>
            </div>
        `;
    }).join('');
    
    return `
        <div class="content-stats">
            <div class="stat-item">
                🎯 Total Results: <span class="stat-count">${displayedResults.length}</span>
            </div>
            ${statsItems}
        </div>
    `;
}

// Format date for display
function formatDate(dateString) {
    if (!dateString || dateString === 'Unknown') return 'Unknown date';
    
    try {
        const date = new Date(dateString);
        const now = new Date();
        const diffTime = Math.abs(now - date);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        
        if (diffDays === 1) return 'Yesterday';
        if (diffDays < 7) return `${diffDays} days ago`;
        if (diffDays < 30) return `${Math.ceil(diffDays / 7)} weeks ago`;
        if (diffDays < 365) return `${Math.ceil(diffDays / 30)} months ago`;
        
        return date.getFullYear().toString();
    } catch {
        return dateString;
    }
}

// Fallback mock search (enhanced with more content types)
async function performMockSearch() {
    allResults = [
        {
            title: 'Sound Healing Benefits for Mental Health',
            source: 'Demo: Health News',
            snippet: 'Recent studies show promising results for sound therapy in treating anxiety and depression.',
            url: 'https://www.healthline.com/health/sound-therapy',
            type: 'news',
            date: new Date().toISOString()
        },
        {
            title: 'My Journey with Binaural Beats',
            source: 'Demo: Reddit Discussion',
            snippet: 'Personal experience using binaural beats for focus and relaxation over 6 months.',
            url: 'https://www.reddit.com/r/Meditation/',
            type: 'reddit',
            date: new Date(Date.now() - 86400000).toISOString(),
            score: 42
        },
        {
            title: 'Deep Sleep Meditation Music',
            source: 'Demo: Meditative Mind',
            snippet: 'Video content featuring relaxing sounds for better sleep and meditation practice.',
            url: 'https://www.youtube.com/watch',
            type: 'video',
            date: new Date(Date.now() - 172800000).toISOString()
        },
        {
            title: 'The Science of Sound Healing Podcast',
            source: 'Demo: Wellness Podcast',
            snippet: 'Expert interviews discussing the neurological effects of sound therapy.',
            url: 'https://podcasts.apple.com/',
            type: 'podcast',
            date: new Date(Date.now() - 259200000).toISOString()
        },
        {
            title: 'Sound Therapy in Clinical Practice',
            source: 'Demo: Journal Article',
            snippet: 'Peer-reviewed research on the therapeutic applications of sound healing.',
            url: 'https://pubmed.ncbi.nlm.nih.gov/',
            type: 'research',
            date: new Date(Date.now() - 2592000000).toISOString()
        },
        {
            title: 'Open Source Binaural Beat Generator',
            source: 'Demo: GitHub Repository',
            snippet: 'Python library for generating custom binaural beats for meditation.',
            url: 'https://github.com/',
            type: 'code',
            date: new Date(Date.now() - 604800000).toISOString(),
            stars: 128
        }
    ];
    
    displayedResults = allResults;
    displayEnhancedResults({
        total_results: allResults.length,
        sources_searched: 6
    });
    
    const exportBtn = document.getElementById('exportBtn');
    if (exportBtn) exportBtn.style.display = 'block';
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
    
    displayEnhancedResults();
}

// Enhanced export with more metadata
function exportResults() {
    const content = displayedResults.map(item => {
        let metadata = `Title: ${item.title}\nSource: ${item.source}\nType: ${item.type}\nURL: ${item.url}\nDate: ${item.date}\nSnippet: ${item.snippet}`;
        
        if (item.score) metadata += `\nScore: ${item.score}`;
        if (item.stars) metadata += `\nStars: ${item.stars}`;
        
        return metadata;
    }).join('\n\n---\n\n');
    
    const summary = `SOUND MIND CONTENT DISCOVERY EXPORT
Generated: ${new Date().toLocaleString()}
Search Terms: ${searchTerms.join(', ')}
Total Results: ${displayedResults.length}
Content Types: ${[...new Set(displayedResults.map(r => r.type))].join(', ')}

===================================

${content}`;
    
    const blob = new Blob([summary], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `sound-mind-enhanced-${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Add filter functionality
function addFilterControls() {
    const resultsWidget = document.querySelector('.results-widget');
    if (!resultsWidget) return;
    
    const filterControls = document.createElement('div');
    filterControls.className = 'filter-controls';
    filterControls.innerHTML = `
        <div class="filter-row">
            <label for="typeFilter">Filter by Type:</label>
            <select id="typeFilter" class="filter-select" onchange="applyFilters()">
                <option value="">All Types</option>
            </select>
            
            <label for="sortBy">Sort by:</label>
            <select id="sortBy" class="filter-select" onchange="applyFilters()">
                <option value="date">Date (Newest)</option>
                <option value="title">Title (A-Z)</option>
                <option value="type">Type</option>
                <option value="score">Score (Highest)</option>
            </select>
        </div>
    `;
    
    const resultsHeader = resultsWidget.querySelector('.results-header');
    resultsHeader.parentNode.insertBefore(filterControls, resultsHeader.nextSibling);
}

// Apply filters and sorting
function applyFilters() {
    const typeFilter = document.getElementById('typeFilter')?.value;
    const sortBy = document.getElementById('sortBy')?.value;
    
    let filteredResults = [...allResults];
    
    // Apply type filter
    if (typeFilter) {
        filteredResults = filteredResults.filter(item => item.type === typeFilter);
    }
    
    // Apply sorting
    switch (sortBy) {
        case 'date':
            filteredResults.sort((a, b) => new Date(b.date) - new Date(a.date));
            break;
        case 'title':
            filteredResults.sort((a, b) => a.title.localeCompare(b.title));
            break;
        case 'type':
            filteredResults.sort((a, b) => a.type.localeCompare(b.type));
            break;
        case 'score':
            filteredResults.sort((a, b) => (b.score || 0) - (a.score || 0));
            break;
    }
    
    displayedResults = filteredResults.slice(0, 8);
    displayEnhancedResults();
    
    // Update type filter options
    updateFilterOptions();
}

// Update filter dropdown options based on available data
function updateFilterOptions() {
    const typeFilter = document.getElementById('typeFilter');
    if (!typeFilter || !allResults.length) return;
    
    const availableTypes = [...new Set(allResults.map(item => item.type))];
    const currentValue = typeFilter.value;
    
    typeFilter.innerHTML = '<option value="">All Types</option>' + 
        availableTypes.map(type => {
            const config = sourceConfig[type] || { emoji: '📄', name: type };
            return `<option value="${type}">${config.emoji} ${config.name}</option>`;
        }).join('');
    
    typeFilter.value = currentValue;
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
    console.log('DOM loaded, initializing Enhanced Sound Mind interface...');
    
    // Initialize search terms display
    updateTermTags();
    
    // Create enhanced UI components
    createSourceSelector();
    addFilterControls();
    
    // Load available sources and test API connection
    setTimeout(async () => {
        await testAPIConnection();
        await loadAvailableSources();
    }, 1000);
    
    // Set up event listeners
    const searchBtn = document.getElementById('searchBtn');
    const addTermBtn = document.getElementById('addTermBtn');
    const customTermInput = document.getElementById('customTerm');
    const exportBtn = document.getElementById('exportBtn');
    
    if (searchBtn) {
        searchBtn.addEventListener('click', performEnhancedSearch);
        console.log('Enhanced search button listener added');
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
        console.log('Enhanced export button listener added');
    }
    
    console.log('Enhanced Sound Mind interface initialized successfully!');
    console.log('Current search terms:', searchTerms);
    console.log('Available source types:', Object.keys(sourceConfig));
});

// Make functions available globally for onclick handlers
window.removeTerm = removeTerm;
window.removeItem = removeItem;
window.setSearchMode = setSearchMode;
window.toggleSource = toggleSource;
window.applyFilters = applyFilters;