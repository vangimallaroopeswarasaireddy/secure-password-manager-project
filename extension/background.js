chrome.runtime.onInstalled.addListener(() => {
  chrome.alarms.create('vault-lock', { periodInMinutes: 1 });
});

chrome.alarms.onAlarm.addListener(async (alarm) => {
  if (alarm.name !== 'vault-lock') return;
  const { last_active } = await chrome.storage.local.get(['last_active']);
  if (!last_active) return;
  const inactiveMs = Date.now() - last_active;
  if (inactiveMs > 5 * 60 * 1000) {
    await chrome.storage.local.remove(['access_token', 'refresh_token']);
  }
});
