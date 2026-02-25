function randomPassword(length = 20) {
  const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=';
  return Array.from({ length }, () => chars[Math.floor(Math.random() * chars.length)]).join('');
}

async function renderVault(search = '') {
  const token = await storage.get('access_token');
  if (!token) return;
  const vault = await apiVault(token, search);
  const ul = document.getElementById('vault');
  ul.innerHTML = '';
  vault.forEach(item => {
    const li = document.createElement('li');
    li.innerHTML = `<strong>${item.site}</strong><br/><span class="small">${item.username}</span><br/>`;
    const btn = document.createElement('button');
    btn.textContent = 'Copy Password';
    btn.onclick = async () => navigator.clipboard.writeText(item.password);
    li.appendChild(btn);
    ul.appendChild(li);
  });
}

document.getElementById('loginBtn').addEventListener('click', async () => {
  try {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const tokens = await apiLogin(email, password);
    await storage.set('access_token', tokens.access_token);
    await storage.set('refresh_token', tokens.refresh_token);
    await storage.set('last_active', Date.now());
    await renderVault();
  } catch (e) {
    alert('Login failed');
  }
});

document.getElementById('search').addEventListener('input', (e) => renderVault(e.target.value));
document.getElementById('generateBtn').addEventListener('click', () => {
  document.getElementById('generated').textContent = randomPassword();
});

renderVault();
