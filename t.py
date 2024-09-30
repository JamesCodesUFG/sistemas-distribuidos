t = [('Hello', 1), ('World', 2)]

a = [tuple[0] for tuple in t]

b = [byte for _bytes in a for byte in _bytes.encode()]

print(bytes(b).decode())