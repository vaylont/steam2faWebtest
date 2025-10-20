# steam2fa/core/utils.py
import base64
import binascii
import time
import hmac
import hashlib
from typing import Tuple

# Попытки декодирования: Base64 -> hex -> base32
def decode_secret(secret: str) -> bytes:
    s = secret.strip()
    # Base64 попытка
    try:
        # некоторые shared_secret в steam хранятся в Base64
        b = base64.b64decode(s + '=' * (-len(s) % 4))
        if b:
            return b
    except Exception:
        pass

    # hex попытка
    try:
        return binascii.unhexlify(s)
    except Exception:
        pass

    # Base32 (A..Z2..7)
    try:
        # base64.b32decode требует padding
        s2 = s.replace(' ', '').upper()
        padding = '=' * (-len(s2) % 8)
        return base64.b32decode(s2 + padding)
    except Exception:
        pass

    raise ValueError("Не удалось декодировать secret (поддерживается: Base64, hex, Base32)")

def totp_code(secret_bytes: bytes, digits: int = 6, timestep: int = 30, now: int = None) -> Tuple[str,int]:
    """
    Возвращает (code, seconds_left)
    """
    if now is None:
        now = int(time.time())
    t = int(now // timestep)
    seconds_left = int(timestep - (now % timestep))

    # сообщение — 8 байт big-endian counter
    msg = t.to_bytes(8, 'big')

    h = hmac.new(secret_bytes, msg, hashlib.sha1).digest()
    offset = h[-1] & 0x0F
    binary = ((h[offset] & 0x7f) << 24) | ((h[offset+1] & 0xff) << 16) | ((h[offset+2] & 0xff) << 8) | (h[offset+3] & 0xff)
    otp = binary % (10 ** digits)
    return (str(otp).zfill(digits), seconds_left)

import time, hmac, hashlib

STEAM_ALPHABET = "23456789BCDFGHJKMNPQRTVWXY"  # 26 символов

def steam_guard_code(secret_bytes: bytes, timestep: int = 30, now: int | None = None):
    """
    Возвращает (code5, seconds_left) по алгоритму Steam (HMAC-SHA1 + кастомный алфавит).
    """
    if now is None:
        now = int(time.time())
    counter = int(now // timestep)
    seconds_left = int(timestep - (now % timestep))

    # 8 байт big-endian счетчик
    msg = counter.to_bytes(8, "big")
    digest = hmac.new(secret_bytes, msg, hashlib.sha1).digest()

    # динамическая усечка
    offset = digest[19] & 0x0F
    full = (
        ((digest[offset]   & 0x7f) << 24) |
        ((digest[offset+1] & 0xff) << 16) |
        ((digest[offset+2] & 0xff) <<  8) |
        ( digest[offset+3] & 0xff)
    )

    # переводим число в 5 символов из STEAM_ALPHABET
    code = []
    for _ in range(5):
        code.append(STEAM_ALPHABET[full % len(STEAM_ALPHABET)])
        full //= len(STEAM_ALPHABET)

    return ("".join(code), seconds_left)