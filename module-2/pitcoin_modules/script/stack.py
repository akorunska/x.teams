

class Stack:
    def __init__(self):
        self.stack = []

    def push(self, arg):
        self.stack.append(arg)

    def pop(self):
        if len(self.stack) == 0:
            return None
        arg = self.stack[-1]
        del(self.stack[-1])
        return arg

    def perform_operation(self, opcode):
        pass
