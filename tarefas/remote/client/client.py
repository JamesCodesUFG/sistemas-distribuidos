import rpyc

conn = rpyc.connect("localhost", 18861)

calc = conn.root

a, b = 10, 5

print(f"Soma: {a} + {b} = {calc.add(a, b)}")
print(f"Subtração: {a} - {b} = {calc.subtract(a, b)}")
print(f"Multiplicação: {a} * {b} = {calc.multiply(a, b)}")
print(f"Divisão: {a} / {b} = {calc.divide(a, b)}")

conn.close()