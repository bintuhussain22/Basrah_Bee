# Chapter 11: PCOS Forum Data Miner
# Extracts and counts mentions of PCOS treatments & symptoms using regex

import re

fname = input("Enter file name: ")
if len(fname) < 1:
    fname = "forum_posts.txt"
fh = open(fname)

# Keywords to track (medications, treatments, symptoms)
keywords = [
    "clomid", "metformin", "letrozole", 
    "ivf", "iui",
    "cramps", "sore boobs", "acne", "spotting"
]

# Initialize counts
counts = {k: 0 for k in keywords}

# Process each line
for line in fh:
    line = line.strip().lower()
    if not line:
        continue

    # Clean up line: remove punctuation
    line = re.sub(r'[^a-z0-9\s]', '', line)

    # Count keyword mentions
    for k in keywords:
        if re.search(r'\b' + re.escape(k) + r'\b', line):
            counts[k] += 1

# Print results
print("Mentions Count:")
for k, v in counts.items():
    print(f"{k}: {v}")
