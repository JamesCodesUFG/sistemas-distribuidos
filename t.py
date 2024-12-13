import json

a = {"hello": 1, 'World': 2}

aux = json.dumps(a)

b = json.loads(aux)

print(b.hello)