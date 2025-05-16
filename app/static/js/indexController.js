/**
 * Gestione della logica applicativa per la pagina principale
 * Responsabilità:
 * - Comunicazione con il backend
 * - Gestione dello stato dell'applicazione
 * - Logica di business
 */

// Aggiorna le piattaforme selezionate nel form
function updateSelectedPlatforms(platforms) {
    document.getElementById('hidden-platforms').value = platforms.join(',');
}

// Aggiungi film alla watchlist
function addToWatchlist(movieName) {
    fetch(`/add_to_watchlist/${encodeURIComponent(movieName)}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert(`${movieName} added to your watchlist!`);
            } else if (data.message === 'already_exists') {
                showAlert(`${movieName} is already in your watchlist.`);
            } else if (data.message === 'movie_not_found') {
                showAlert(`Movie "${movieName}" not found in database.`);
            } else if (data.message === 'invalid_movie_id') {
                showAlert(`Invalid movie ID for "${movieName}".`);
            } else {
                showAlert(`Could not add ${movieName} to your watchlist.`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert(`Something went wrong while adding ${movieName}.`);
        });
}

// Mostra un messaggio all'utente (può essere sovrascritto dalla view per personalizzare l'UI)
function showAlert(message) {
    alert(message);
}