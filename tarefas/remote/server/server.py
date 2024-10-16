import rpyc

class CalculatorService(rpyc.Service):
    def __init__(self):
        pass

    def exposed_add(self, a, b):
        return a + b

    def exposed_subtract(self, a, b):
        return a - b

    def exposed_multiply(self, a, b):
        return a * b

    def exposed_divide(self, a, b):
        if b == 0:
            return "Error: Division by zero."
        return a / b

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer

    server = ThreadedServer(CalculatorService, port=18861)

    print("Servidor de calculadora rodando na porta 18861...")

    server.start()