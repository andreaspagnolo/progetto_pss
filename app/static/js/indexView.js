/**
 * Gestione della visualizzazione (UI) per la pagina principale
 * Responsabilità:
 * - Gestione dropdown piattaforme
 * - Visualizzazione piattaforme selezionate
 * - Gestione eventi UI
 */

document.addEventListener('DOMContentLoaded', function() {
    // Inizializza le piattaforme al caricamento
    updateSelectedPlatformsView();

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

    // Aggiungi event listener alle checkbox piattaforme
    document.querySelectorAll('input[name="platform"]').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateSelectedPlatformsView();
        });
    });

    // Gestione click sul pulsante dropdown
    document.getElementById('platform-dropdown-button')?.addEventListener('click', function(e) {
        e.stopPropagation();
        const dropdown = document.getElementById('platform-dropdown');
        dropdown.classList.toggle('show');
    });

    // Previeni la chiusura quando si clicca dentro il dropdown
    document.getElementById('platform-dropdown')?.addEventListener('click', function(e) {
        e.stopPropagation();
    });
});

// Mostra/nascondi dropdown piattaforme
function togglePlatformDropdown() {
    const dropdown = document.getElementById('platform-dropdown');
    const overlay = document.getElementById('overlay');
    dropdown.classList.toggle('show');
    overlay.classList.toggle('show');
}

// Aggiorna la visualizzazione delle piattaforme selezionate
function updateSelectedPlatformsView() {
    const selectedPlatformsDiv = document.getElementById('selected-platforms');
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
    
    // Aggiorna il campo nascosto tramite il controller
    updateSelectedPlatforms(selectedPlatforms);
}

// Rimuovi piattaforma selezionata (chiama il controller)
function removePlatform(platform) {
    const checkboxes = document.querySelectorAll('input[name="platform"]');
    checkboxes.forEach(checkbox => {
        if (checkbox.value === platform) {
            checkbox.checked = false;
        }
    });
    updateSelectedPlatformsView();
}