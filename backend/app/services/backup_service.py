import json
from app.utils.crypto import encrypt_value, decrypt_value


class BackupService:
    @staticmethod
    def export_entries(entries: list[dict], user_salt: str) -> str:
        payload = json.dumps(entries)
        return encrypt_value(payload, user_salt)

    @staticmethod
    def import_entries(encrypted_blob: str, user_salt: str) -> list[dict]:
        return json.loads(decrypt_value(encrypted_blob, user_salt))
