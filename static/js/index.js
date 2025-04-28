/**
 * Funzioni per la pagina principale (index.html)
 * Gestione:
 * - Dropdown piattaforme
 * - Selezione/rimozione piattaforme
 * - Aggiunta alla watchlist
 */

document.addEventListener('DOMContentLoaded', function() {
    // Inizializza le piattaforme al caricamento
    updateSelectedPlatforms();

    // Gestione autocomplete
    const movieSearch = document.getElementById('movie-search');
    if (movieSearch) {
        movieSearch.addEventListener('input', function() {
            const input = this.value.toLowerCase();
            const options = document.querySelectorAll('#movie-options option');
            
            options.forEach(option => {
                option.hidden = !option.value.toLowerCase().includes(input);
            });
        });
    }

    // Chiudi dropdown se si clicca fuori
    window.addEventListener('click', function(event) {
        const dropdown = document.getElementById('platform-dropdown');
        const overlay = document.getElementById('overlay');
        if (!event.target.matches('.platform-selector') && !event.target.closest('.platform-dropdown')) {
            dropdown.classList.remove('show');
            overlay.classList.remove('show');
        }
    });
});

// Mostra/nascondi dropdown piattaforme
function togglePlatformDropdown() {
    const dropdown = document.getElementById('platform-dropdown');
    const overlay = document.getElementById('overlay');
    dropdown.classList.toggle('show');
    overlay.classList.toggle('show');
}

// Rimuovi piattaforma selezionata
function removePlatform(platform) {
    const checkboxes = document.querySelectorAll('input[name="platform"]');
    checkboxes.forEach(checkbox => {
        if (checkbox.value === platform) {
            checkbox.checked = false;
        }
    });
    updateSelectedPlatforms();
}

// Aggiorna l'elenco piattaforme selezionate
function updateSelectedPlatforms() {
    const selectedPlatformsDiv = document.getElementById('selected-platforms');
    const hiddenInput = document.getElementById('hidden-platforms');
    const checkboxes = document.querySelectorAll('input[name="platform"]:checked');
    
    selectedPlatformsDiv.innerHTML = '';
    const selectedPlatforms = [];
    
    checkboxes.forEach(checkbox => {
        selectedPlatforms.push(checkbox.value);
        const platformTag = document.createElement('div');
        platformTag.className = 'platform-tag';
        platformTag.innerHTML = `
            ${checkbox.value}
            <span class="close" onclick="removePlatform('${checkbox.value}')">×</span>
        `;
        selectedPlatformsDiv.appendChild(platformTag);
    });
    
    hiddenInput.value = selectedPlatforms.join(',');
}

// Aggiungi film alla watchlist
function addToWatchlist(movieName) {
    fetch(`/add_to_watchlist/${encodeURIComponent(movieName)}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(`${movieName} added to your watchlist!`);
            } else if (data.message === 'already_exists') {
                alert(`${movieName} is already in your watchlist.`);
            } else if (data.message === 'movie_not_found') {
                alert(`Movie "${movieName}" not found in database.`);
            } else if (data.message === 'invalid_movie_id') {
                alert(`Invalid movie ID for "${movieName}".`);
            } else {
                alert(`Could not add ${movieName} to your watchlist.`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert(`Something went wrong while adding ${movieName}.`);
        });
}

// Aggiungi event listener alle checkbox piattaforme
document.querySelectorAll('input[name="platform"]').forEach(checkbox => {
    checkbox.addEventListener('change', updateSelectedPlatforms);
});