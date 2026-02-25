(async function () {
  const token = await storage.get('access_token');
  if (!token) return;

  const forms = document.querySelectorAll('form');
  if (!forms.length) return;

  const host = location.hostname;
  try {
    const entries = await apiVault(token, host);
    if (!entries.length) return;
    const match = entries.find(e => host.includes(new URL(e.site.startsWith('http') ? e.site : `https://${e.site}`).hostname)) || entries[0];

    const userInput = document.querySelector('input[type="email"], input[name*=user i], input[name*=email i], input[name*=login i]');
    const passInput = document.querySelector('input[type="password"]');
    if (userInput) userInput.value = match.username;
    if (passInput) passInput.value = match.password;
  } catch (err) {
    console.warn('Autofill failed', err);
  }
})();
