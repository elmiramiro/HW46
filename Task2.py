import threading
import time
import logging


# Класс, который читает данные из файла и обновляет их периодически
class NumbersData:
    def __init__(self, filename, update_interval=5):
        self.filename = filename
        self.update_interval = update_interval
        self.numbers = []
        self.lock = threading.Lock()
        self._stop_event = threading.Event()
        self._update_thread = threading.Thread(target=self._update_loop)
        self._update_thread.daemon = True
        self._update_thread.start()

    def _update_loop(self):
        while not self._stop_event.is_set():
            self.load_numbers()
            time.sleep(self.update_interval)

    def load_numbers(self):
        with self.lock:
            try:
                with open(self.filename, "r") as f:
                    self.numbers = [int(line.strip()) for line in f if line.strip().isdigit()]
            except FileNotFoundError:
                self.numbers = []

    def stop(self):
        self._stop_event.set()
        self._update_thread.join()

    def get_numbers(self):
        with self.lock:
            return list(self.numbers)


# Proxy для NumbersData, добавляющий логирование доступа и операции над данными
class NumbersDataProxy:
    def __init__(self, numbers_data):
        self._numbers_data = numbers_data
        logging.basicConfig(filename="access.log", level=logging.INFO,
                            format="%(asctime)s - %(message)s")

    def _log_access(self, action):
        logging.info(f"Accessed numbers to perform: {action}")

    def get_sum(self):
        self._log_access("sum")
        return sum(self._numbers_data.get_numbers())

    def get_max(self):
        self._log_access("max")
        nums = self._numbers_data.get_numbers()
        return max(nums) if nums else None

    def get_min(self):
        self._log_access("min")
        nums = self._numbers_data.get_numbers()
        return min(nums) if nums else None

    def get_all(self):
        self._log_access("get all numbers")
        return self._numbers_data.get_numbers()


if __name__ == "__main__":
    filename = "numbers.txt"

    # Создаем объект с данными и запускаем обновление из файла каждые 5 секунд
    numbers_data = NumbersData(filename=filename, update_interval=5)

    # Оборачиваем прокси с логированием
    proxy = NumbersDataProxy(numbers_data)

    try:
        while True:
            time.sleep(10)
            print("Сумма чисел:", proxy.get_sum())
            print("Максимум:", proxy.get_max())
            print("Минимум:", proxy.get_min())
            print("Все числа:", proxy.get_all())
            print("-----")
    except KeyboardInterrupt:
        print("Останавливаем...")
        numbers_data.stop()
