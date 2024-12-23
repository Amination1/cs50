i = "x"
counter = 0
while not isinstance(i, float) or not i >= 0:
    try:
        i = float(input("Change: "))

    except:
        print("this input as invalid, as by re-prompting the user to type in another number.")
i = int(i * 100)
while (i >= 25):
    i -= 25
    counter += 1

while (i >= 10):
    i -= 10
    counter += 1

while (i >= 5):
    i -= 5
    counter += 1

while (i >= 1):
    i -= 1
    counter += 1

print(counter)
