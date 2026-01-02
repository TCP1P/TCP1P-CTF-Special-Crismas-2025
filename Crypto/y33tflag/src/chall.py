import mpmath as mp
mp.mp.prec = 2000
FLAG = b"XMAS{this_is_actually_an_exercise_problem_from_the_book_An-Introduction-To-Mathematical-Cryptography_by_silverman}"
FLAG += b"X" * (-len(FLAG) % 12)
secrets = [int.from_bytes(FLAG[i:i+12]) for i in range(0, len(FLAG), 12)]
print(list(map(lambda x : str(mp.mpf(x).sqrt()).split('.')[-1], secrets)))
