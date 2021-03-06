import datetime


def err_log(name: str, text: str, code=0):
    current_time = datetime.datetime.now()
    print(name, text, code, datetime)
    with open("log.txt", "at") as log_file:
        string = "Subject: " + name + "\n" + "Test: " + text + "\n" + "Code: " + str(code) + "\n" + "Time:" + \
                 str(current_time)
        string += "\n" * 3 + '-' * 30 + "\n" * 3
        log_file.write(string)
