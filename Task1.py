from abc import ABC, abstractmethod

# Абстрактная команда с методом execute
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

# Получатель команд — какой-то объект, на котором выполняется действие
class Light:
    def turn_on(self):
        print("Свет включен")
    def turn_off(self):
        print("Свет выключен")

# Конкретная команда включения света
class TurnOnCommand(Command):
    def __init__(self, light: Light):
        self.light = light
    def execute(self):
        self.light.turn_on()

# Конкретная команда выключения света
class TurnOffCommand(Command):
    def __init__(self, light: Light):
        self.light = light
    def execute(self):
        self.light.turn_off()

# Отправитель команд — объект, который вызывает команды
class RemoteControl:
    def __init__(self):
        self.command = None
    def set_command(self, command: Command):
        self.command = command
    def press_button(self):
        if self.command:
            self.command.execute()

# Тестирование паттерна
if __name__ == "__main__":
    light = Light()  # Получатель
    remote = RemoteControl()  # Отправитель

    turn_on = TurnOnCommand(light)
    turn_off = TurnOffCommand(light)

    remote.set_command(turn_on)
    remote.press_button()  # Output: Свет включен

    remote.set_command(turn_off)
    remote.press_button()  # Output: Свет выключен
