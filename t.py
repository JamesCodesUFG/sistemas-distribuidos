import base64
import json

message = {
                    'name': f'a_a',
                    'file': b''
                }

json_string = json.dumps(message)

decoded_data = json.loads(json_string)

print(decoded_data['name'])

