/**
 * Funzioni per l'area personale (personal_area.html)
 * Gestione:
 * - Svuotamento watchlist
 */

// Svuota completamente la watchlist
function clearWatchlist() {
    if (confirm('Are you sure you want to remove all movies from your watchlist?')) {
        fetch('/clear_watchlist')
            .then(response => {
                if (response.redirected) {
                    window.location.href = response.url;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Something went wrong while clearing the watchlist.');
            });
    }
}