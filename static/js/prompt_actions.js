function showToast(msg, duration=2500) {
  const existing = document.querySelector('.toast');
  if (existing) existing.remove();
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.textContent = msg;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), duration);
}

function trackAndCopy(promptId, text) {
  fetch('/api/use-prompt', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({prompt_id: promptId})
  })
  .then(r => r.json())
  .then(data => {
    if (data.limit_reached) {
      document.getElementById('guestLimitModal').style.display = 'flex';
      return;
    }
    navigator.clipboard.writeText(text)
      .then(() => showToast('✓ Prompt copied to clipboard!'))
      .catch(() => {
        const ta = document.createElement('textarea');
        ta.value = text; document.body.appendChild(ta);
        ta.select(); document.execCommand('copy'); document.body.removeChild(ta);
        showToast('✓ Prompt copied!');
      });
  })
  .catch(() => {
    navigator.clipboard.writeText(text).then(() => showToast('✓ Copied!')).catch(() => {});
  });
}

function copyPrompt(promptId, text) {
  trackAndCopy(promptId, text);
}

function toggleFav(promptId, btn) {
  fetch('/api/favourite', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({prompt_id: promptId})
  })
  .then(r => {
    if (r.status === 401) {
      window.location.href = '/login';
      return null;
    }
    return r.json();
  })
  .then(data => {
    if (!data) return;
    if (data.status === 'added') {
      btn.innerHTML = '❤️'; btn.classList.add('fav-active');
      showToast('Added to favourites!');
    } else {
      btn.innerHTML = '🤍'; btn.classList.remove('fav-active');
      showToast('Removed from favourites');
    }
  });
}

// Close modals on overlay click
document.addEventListener('click', function(e) {
  if (e.target.classList.contains('modal')) {
    e.target.style.display = 'none';
  }
});
