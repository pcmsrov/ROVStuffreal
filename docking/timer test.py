import time

timer = time.time()

while True:
    current = time.time()

    if current <= timer + 10:
        print("damn")

    if current >= timer + 10:
        print("sus")
        break