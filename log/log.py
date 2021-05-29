from datetime import datetime


def write_log(message):
    with open('log/log.txt', "a") as file:
        file.write(f"##### {datetime.now()} #####\n{message}\n\n")

