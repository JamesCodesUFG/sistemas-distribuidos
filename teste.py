aux = 127

aux_bytes = (-aux).to_bytes(1, 'big', signed=True)

print((-aux).to_bytes(1, 'big', signed=True))

int_value = int.from_bytes(aux_bytes, byteorder='big')

print(int_value)  # Imprime 128