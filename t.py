def a(func):
    def wrapper(*args, **kwargs):
        print('Executou a função com paramentros', args, kwargs)
        func(*args, **kwargs)
    return wrapper

class A():
    @a
    def hello_world(self, name: str):
        print('Hello', name)

    

A().hello_world('Tiago')