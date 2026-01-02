import numpy as np

# 1. Setup the equations
# We will solve: log(letter1) + log(letter2) + ... = log(value)
equations = [
    ("one", 1), ("two", 2), ("three", 3), ("four", 4), ("five", 5),
    ("six", 6), ("seven", 7), ("eight", 8), ("nine", 9), ("ten", 10),
    ("twenty", 20), ("thirty", 30), ("forty", 40), ("fifty", 50), ("sixty", 60)
]

# Identify all unique letters
letters = sorted(list(set("".join([w for w, v in equations]))))
letter_map = {l: i for i, l in enumerate(letters)}
n_vars = len(letters)

# 2. Build the Linear System for Logarithms
A = np.zeros((len(equations), n_vars))
b = np.zeros(len(equations))

for row, (word, val) in enumerate(equations):
    # The value side is log(value). log(1) is 0.
    b[row] = np.log(val)
    for char in word:
        col = letter_map[char]
        A[row, col] += 1

# 3. Solve for log(letters) using Least Squares
# We use lstsq because the system might be overdetermined
log_x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)

# Convert back to real values: letter = exp(log_x)
# We map them to a dictionary for easy use
letter_values = {l: np.exp(val) for l, val in zip(letters, log_x)}

# 4. Decode the Cipher
cipher_words = [
    "sennsu", "eeegnw", "ewveer", "vtfesg", "rexifr", "wsfwes", "xgtgee", 
    "reerux", "eisifh", "enwege", "eetggx", "regvws", "vgeuge", "heisif", 
    "fftfei", "eegfgf", "gtxgee", "etftve", "sverwg", "gveegu", "nggeug", 
    "ieffgf", "eenesv", "eshiif", "fehiis", "uextst", "wrwuee", "revwsg", 
    "ewvsrg", "iifhse", "wereev", "sxtsws", "xgeget", "gteuvg", "wuweer", 
    "ettnen", "ggffee", "eggext", "ihiefs", "urweew", "erxrue", "hisfie", 
    "sxeeeu", "egngwt", "gtxeeg", "vfteee", "eihsif", "tswtxi", "sefihi", 
    "esvsve", "eegtgx", "wrieww", "ftevee", "vgeeug", "ersntv"
]

decoded_message = ""

for word in cipher_words:
    # "Letter Times": Multiply the values of the letters
    product = 1.0
    for char in word:
        if char in letter_values:
            product *= letter_values[char]
    
    # "Round": Round to the nearest integer for ASCII
    ascii_val = int(round(product))
    decoded_message += chr(ascii_val)

print(f"\nDecoded Message:\n{decoded_message}")