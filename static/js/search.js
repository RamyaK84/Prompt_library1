// Live search suggestions
let debounceTimer;
const searchInput = document.getElementById('searchQuery') || document.getElementById('heroSearch');
if (searchInput) {
  searchInput.addEventListener('input', function() {
    clearTimeout(debounceTimer);
    const q = this.value.trim();
    if (q.length < 2) return;
    debounceTimer = setTimeout(() => {
      fetch(`/api/search?q=${encodeURIComponent(q)}&mode=keyword`)
        .then(r => r.json())
        .then(results => console.log('Suggestions:', results.map(r => r.title)));
    }, 300);
  });
}
