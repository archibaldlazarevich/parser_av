import threading
import subprocess


def run_script(script_name):
    subprocess.run(["python", "-m", script_name])


if __name__ == "__main__":
    thread1 = threading.Thread(target=run_script, args=(("src.parcer.main"),))
    thread2 = threading.Thread(
        target=run_script, args=(("src.database.main"),)
    )
    thread3 = threading.Thread(
        target=run_script, args=(("src.telegram_bot.main"),)
    )
    thread4 = threading.Thread(
        target=run_script,
        args=(("src.telegram_bot.handlers.custom.update_chat"),),
    )

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
