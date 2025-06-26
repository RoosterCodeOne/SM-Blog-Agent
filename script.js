// Sound Mind Content Discovery - JavaScript
console.log('Sound Mind script loading...');

// Global variables
let searchTerms = ['sound healing', 'binaural beats', 'meditation music'];
let allResults = [];
let displayedResults = [];
let isSearching = false;

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
                <p>Discovering content across multiple sources...</p>
            </div>
        `;
    }
}

// Main search function
async function performSearch() {
    console.log('performSearch called');
    
    if (isSearching) {
        console.log('Search already in progress, skipping');
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
        allResults = [];
        
        for (const term of searchTerms) {
            showStatus(`Searching for "${term}"...`);
            
            // Simulate news search
            await delay(800);
            const newsResults = await mockNewsSearch(term);
            allResults.push(...newsResults);
            
            // Simulate Reddit search
            await delay(600);
            const redditResults = await mockRedditSearch(term);
            allResults.push(...redditResults);
            
            // Simulate research search
            await delay(700);
            const researchResults = await mockResearchSearch(term);
            allResults.push(...researchResults);
        }

        // Shuffle and select top 5 for display
        allResults = shuffleArray(allResults);
        displayedResults = allResults.slice(0, 5);
        
        hideStatus();
        displayResults();
        
        const exportBtn = document.getElementById('exportBtn');
        if (exportBtn) exportBtn.style.display = 'block';
        
    } catch (error) {
        showStatus('❌ Search failed. Please try again.');
        console.error('Search error:', error);
    } finally {
        isSearching = false;
        if (searchBtn) searchBtn.disabled = false;
        if (searchBtnText) searchBtnText.textContent = '🔍 Search Content';
    }
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
                <p>Try adjusting your search terms or search again later.</p>
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
            <a href="#" onclick="handleLinkClick('${item.type}', '${item.title.replace(/'/g, "\\'")}')" class="item-link">🔗 Read More</a>
        </div>
    `).join('');
}

// Handle clicking on result links (mock)
function handleLinkClick(type, title) {
    alert(`This is a mock result. In the real version, this would link to:\n\n${title}\n\nType: ${type} content`);
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
        `Title: ${item.title}\nSource: ${item.source}\nSnippet: ${item.snippet}\nType: ${item.type}\n\n`
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

// Mock API functions (these will be replaced with real API calls later)
async function mockNewsSearch(term) {
    const mockNews = [
        {
            title: `Revolutionary Study: ${term} Shows 85% Improvement in Sleep Quality`,
            source: 'News: Sleep Medicine Journal',
            snippet: `Groundbreaking research reveals that regular ${term} practice leads to significant improvements in sleep patterns, with participants reporting deeper, more restorative sleep within just two weeks of starting therapy.`,
            url: '#mock-news-link',
            type: 'news'
        },
        {
            title: `Breaking: Major Hospital Adopts ${term} for Patient Recovery`,
            source: 'News: Medical Innovation Today',
            snippet: `Massachusetts General Hospital becomes the first major medical center to integrate ${term} therapy into their standard patient care protocols, citing remarkable recovery improvements.`,
            url: '#mock-news-link',
            type: 'news'
        },
        {
            title: `${term} Industry Sees 300% Growth in Consumer Demand`,
            source: 'News: Wellness Business Weekly',
            snippet: `Market analysis shows unprecedented growth in ${term} services and products as consumers increasingly seek natural wellness solutions. Industry experts predict continued expansion through 2025.`,
            url: '#mock-news-link',
            type: 'news'
        }
    ];
    return mockNews.slice(0, Math.floor(Math.random() * 3) + 1);
}

async function mockRedditSearch(term) {
    const mockReddit = [
        {
            title: `6-month ${term} journey - my anxiety is completely gone (detailed post)`,
            source: 'Reddit: r/SoundHealing',
            snippet: `I started my ${term} practice 6 months ago as a last resort for severe anxiety. The transformation has been incredible - I no longer need medication and feel more centered than ever. Here's my complete routine and the specific techniques that worked...`,
            url: '#mock-reddit-link',
            type: 'reddit'
        },
        {
            title: `Scientists of Reddit: Can someone explain the actual mechanism behind ${term}?`,
            source: 'Reddit: r/AskScience',
            snippet: `Fascinating scientific discussion exploring exactly how ${term} affects our nervous system and brain chemistry. Top-voted responses from neuroscientists and sound therapists with peer-reviewed sources.`,
            url: '#mock-reddit-link',
            type: 'reddit'
        },
        {
            title: `DIY ${term} setup that changed my meditation practice forever`,
            source: 'Reddit: r/Meditation',
            snippet: `After years of struggling with traditional meditation, I discovered ${term} and built my own setup for under $100. The difference in my ability to reach deep meditative states is remarkable. Full equipment list and instructions included.`,
            url: '#mock-reddit-link',
            type: 'reddit'
        }
    ];
    return mockReddit.slice(0, Math.floor(Math.random() * 3) + 1);
}

async function mockResearchSearch(term) {
    const mockResearch = [
        {
            title: `Neuroplasticity changes induced by ${term}: A longitudinal fMRI study (n=240)`,
            source: 'Research: Nature Neuroscience',
            snippet: `This comprehensive neuroimaging study demonstrates measurable structural brain changes following 8 weeks of ${term} therapy. Participants showed increased gray matter density in regions associated with emotional regulation and stress response.`,
            url: '#mock-research-link',
            type: 'research'
        },
        {
            title: `Clinical efficacy of ${term} in treating chronic pain: Randomized controlled trial`,
            source: 'Research: Journal of Pain Management',
            snippet: `Double-blind RCT (n=180) comparing ${term} therapy to standard treatment for chronic pain conditions. Results show significant pain reduction and improved quality of life measures in the treatment group.`,
            url: '#mock-research-link',
            type: 'research'
        },
        {
            title: `Biomarker analysis of stress hormones following ${term} intervention`,
            source: 'Research: Psychoneuroendocrinology',
            snippet: `Laboratory analysis reveals significant decreases in cortisol and inflammatory markers following ${term} sessions. This study provides biological evidence for the stress-reducing effects previously observed in behavioral assessments.`,
            url: '#mock-research-link',
            type: 'research'
        }
    ];
    return mockResearch.slice(0, Math.floor(Math.random() * 2) + 1);
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