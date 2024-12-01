from threading import Thread, Semaphore

class Commmand():
    def __init__(self, exec, has_args: bool) -> None:
        self.__exec = exec
        self.__has_args = has_args

    def execute(self, args):
        if not self.__has_args:
            self.__exec()
        elif self.__has_args and args == []:
            print('\nComando não reconhecido...\n')
        else:
            self.__exec(args[0])
                

class InputManager():
    def __init__(self, commands: dict[str, Commmand]) -> None:
        self.__commands = commands

    def next(self):
        input_cmd, *input_arg = input('> ').split(' ')

        if input_cmd in self.__commands:
            self.__commands[input_cmd].execute(input_arg)
        else:
            print('\nComando não reconhecido...\n')

