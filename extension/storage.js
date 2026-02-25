const storage = {
  async set(key, value) { return chrome.storage.local.set({ [key]: value }); },
  async get(key) { const value = await chrome.storage.local.get([key]); return value[key]; },
  async remove(key) { return chrome.storage.local.remove(key); }
};
