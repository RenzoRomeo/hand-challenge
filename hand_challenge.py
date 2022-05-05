class Interpreter:
    def __init__(self) -> None:
        self.memory = [0 for i in range(4096)]  # 4k of memory
        self.memory_pointer = 0
        self.program = []
        self.program_counter = 0
        self.instructions = {
            '👉': self.increment_pointer,
            '👈': self.decrement_pointer,
            '👆': self.increment_value,
            '👇': self.decrement_value,
            '🤜': self.conditional_z,
            '🤛': self.conditional_nz,
            '👊': self.display_current
        }

    def increment_pointer(self) -> None:
        self.memory_pointer += 1

    def decrement_pointer(self) -> None:
        self.memory_pointer -= 1

    def increment_value(self) -> None:
        value = self.memory[self.memory_pointer] + 1
        self.memory[self.memory_pointer] = value & 255

    def decrement_value(self) -> None:
        value = self.memory[self.memory_pointer] - 1
        self.memory[self.memory_pointer] = value & 255

    def display_current(self) -> None:
        print(chr(self.memory[self.memory_pointer]))

    def conditional_z(self, loc: int) -> None:
        if self.memory[self.memory_pointer] == 0:
            self.program_counter = loc

    def conditional_nz(self, loc: int) -> None:
        if self.memory[self.memory_pointer] != 0:
            self.program_counter = loc

    def read_program(self, file_path: str):
        program = []
        with open(file_path, encoding='utf-8') as f:
            while c := f.read(1):
                program.append(c)
        self.program = program

    def display_program(self) -> None:
        print(self.program)

    def run(self) -> None:
        while self.program_counter < len(self.program):
            instruction = self.program[self.program_counter]
            if instruction == '🤜':
                queue = [1]
                aux = self.program_counter + 1
                while len(queue) != 0:
                    if self.program[aux] == '🤜':
                        queue.append(1)
                    elif self.program[aux] == '🤛':
                        queue.pop()
                    aux += 1
                self.instructions[instruction](aux+1)
            elif instruction == '🤛':
                queue = [1]
                aux = self.program_counter - 1
                while len(queue) != 0:
                    if self.program[aux] == '🤛':
                        queue.append(1)
                    elif self.program[aux] == '🤜':
                        queue.pop()
                    aux -= 1
                self.instructions[instruction](aux)
            else:
                self.instructions[instruction]()
            self.program_counter += 1


if __name__ == '__main__':
    interpreter = Interpreter()
    interpreter.read_program('input.hand')
    interpreter.run()
