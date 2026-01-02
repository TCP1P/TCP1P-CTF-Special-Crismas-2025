import mpmath as mp
mp.mp.prec = 2000
FLAG = b"XMAS{REDACTED}"
FLAG += b"X" * (-len(FLAG) % 12)
secrets = [int.from_bytes(FLAG[i:i+12]) for i in range(0, len(FLAG), 12)]
print(list(map(lambda x : str(mp.mpf(x).sqrt()).split('.')[-1], secrets)))
