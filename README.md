# Secure Password Manager Monorepo

## Project Structure

- `backend/` FastAPI + SQLAlchemy + JWT + Argon2 + encrypted vault
- `mobile/` Expo React Native TypeScript app with biometrics
- `extension/` Chrome extension (Manifest v3) with vault sync and autofill

## Environment Variables

Create `backend/.env` from `backend/.env.example`.

```bash
cp backend/.env.example backend/.env
```

Required keys:
- `JWT_SECRET_KEY`
- `JWT_REFRESH_SECRET_KEY`
- `FERNET_KEY` (generate with Python: `from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())`)

## Backend Setup

```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API routes:
- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh`
- `POST /auth/logout`
- `GET /vault`
- `POST /vault`
- `PUT /vault/{id}`
- `DELETE /vault/{id}`
- `POST /backup/export`
- `POST /backup/import`

## Mobile Setup (Expo)

```bash
cd mobile
npm install
npm run start
```

Then press:
- `a` for Android
- `i` for iOS

## Chrome Extension Setup

1. Open `chrome://extensions`.
2. Enable **Developer mode**.
3. Click **Load unpacked**.
4. Select the `extension/` folder.
5. Pin extension and open popup.

## Security Notes

- Master password hashes stored with Argon2 + per-user salt.
- Vault passwords encrypted before DB storage.
- Access/refresh JWT token flow with expiration + refresh rotation.
- 2FA (TOTP) support included at auth layer.
- Rate-limited auth routes.
- Security headers middleware and strict validation via Pydantic.

## Screenshots

- Backend: terminal/API workflow
- Mobile: Login, Vault List, Add/Edit, Generator, Settings (dark theme)
- Extension: popup login, vault search, copy password, generator
