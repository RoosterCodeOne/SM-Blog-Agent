// DEBUG VERSION - Sound Mind Script
console.log('🔧 DEBUG: Script is loading...');

// Test if script loads
window.addEventListener('load', function() {
    console.log('🔧 DEBUG: Window loaded');
});

// Global variables
let searchTerms = ['sound healing', 'binaural beats', 'meditation music'];
console.log('🔧 DEBUG: Initial search terms set:', searchTerms);

// Test function - simple version
function updateTermTags() {
    console.log('🔧 DEBUG: updateTermTags called');
    console.log('🔧 DEBUG: Current terms:', searchTerms);
    
    const container = document.getElementById('termTags');
    console.log('🔧 DEBUG: Container found:', !!container);
    
    if (!container) {
        console.error('🔧 DEBUG: termTags container NOT FOUND!');
        return;
    }
    
    // Simple version first
    const html = searchTerms.map(term => 
        `<span class="term-tag">${term} <span class="remove-term" onclick="removeTerm('${term}')">&times;</span></span>`
    ).join('');
    
    console.log('🔧 DEBUG: Generated HTML:', html);
    container.innerHTML = html;
    console.log('🔧 DEBUG: HTML inserted successfully');
}

// Test function - simple version
function addCustomTerm() {
    console.log('🔧 DEBUG: addCustomTerm called');
    
    const input = document.getElementById('customTerm');
    console.log('🔧 DEBUG: Input found:', !!input);
    
    if (!input) {
        console.error('🔧 DEBUG: customTerm input NOT FOUND!');
        return;
    }
    
    const term = input.value.trim();
    console.log('🔧 DEBUG: Input value:', term);
    
    if (term && !searchTerms.includes(term)) {
        searchTerms.push(term);
        input.value = '';
        console.log('🔧 DEBUG: Term added. New array:', searchTerms);
        updateTermTags();
    } else {
        console.log('🔧 DEBUG: Term not added - empty or duplicate');
    }
}

// Test function - simple version  
function removeTerm(term) {
    console.log('🔧 DEBUG: removeTerm called with:', term);
    searchTerms = searchTerms.filter(t => t !== term);
    console.log('🔧 DEBUG: Updated terms:', searchTerms);
    updateTermTags();
}

// Test initialization
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 DEBUG: DOM loaded, starting initialization...');
    
    // Test if elements exist
    const searchBtn = document.getElementById('searchBtn');
    const addTermBtn = document.getElementById('addTermBtn');
    const customTermInput = document.getElementById('customTerm');
    const termTags = document.getElementById('termTags');
    
    console.log('🔧 DEBUG: Elements found:');
    console.log('  - searchBtn:', !!searchBtn);
    console.log('  - addTermBtn:', !!addTermBtn);
    console.log('  - customTermInput:', !!customTermInput);
    console.log('  - termTags:', !!termTags);
    
    // Initialize search terms display
    console.log('🔧 DEBUG: Calling updateTermTags...');
    updateTermTags();
    
    // Add event listeners with debugging
    if (addTermBtn) {
        addTermBtn.addEventListener('click', function() {
            console.log('🔧 DEBUG: Add button clicked!');
            addCustomTerm();
        });
        console.log('🔧 DEBUG: Add button listener added');
    } else {
        console.error('🔧 DEBUG: Add button not found!');
    }
    
    if (customTermInput) {
        customTermInput.addEventListener('keypress', function(e) {
            console.log('🔧 DEBUG: Key pressed in input:', e.key);
            if (e.key === 'Enter') {
                console.log('🔧 DEBUG: Enter key detected!');
                addCustomTerm();
            }
        });
        console.log('🔧 DEBUG: Input listener added');
    } else {
        console.error('🔧 DEBUG: Input not found!');
    }
    
    console.log('🔧 DEBUG: Initialization complete!');
});