def log(msg):
    print(msg)

def error(msg):
    print("\033[31m%s\033[0m" % msg)

def warning(msg):
    print("\033[33m%s\033[0m" % msg)

def display(msg):
    print("\033[32m%s\033[0m" % msg)
    