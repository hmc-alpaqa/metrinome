import os

matches = []
for root, dirnames, filenames in os.walk('.'):
    for name in filenames:
        isMatch = not name.isascii()
        if isMatch:
            matches.append(os.path.join(root, name))

d = {}
for match in matches:
    matchReplacement = "".join([c if c.isascii() else '__' for c in match])
    d[match] = matchReplacement

replaced = {}
print(f"Found {len(d.keys())} many files to replace.")
for key in d.keys():
    if os.path.exists(d[key]):
        print(f'error, {d[key]} already exists')
    else:
        replaced[key] = d[key]
        os.rename(key, d[key])

with open("changed_files.txt", "w") as f:
    for key in replaced.keys():
        f.write(f"{key}: {replaced[key]}\n")
