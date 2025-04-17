import os
import threading
import subprocess


def run_script(script_name):
    subprocess.run(["python", "-m", script_name])


if __name__ == "__main__":
    # Создаем потоки для каждого скрипта
    thread1 = threading.Thread(target=run_script, args=(("src.parcer.main"),))
    thread2 = threading.Thread(
        target=run_script, args=(("src.database.main"),)
    )
    thread3 = threading.Thread(
        target=run_script, args=(("src.telegram_bot.main"),)
    )

    # Запускаем потоки
    thread1.start()
    thread2.start()
    thread3.start()

    # Ожидаем завершения потоков
    thread1.join()
    thread2.join()
    thread3.join()
