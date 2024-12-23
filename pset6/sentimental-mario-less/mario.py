h = 0
while not isinstance(h, int) or not (h > 0 and h < 9):
    try:
        h = int(input("Height: "))

    except:
        print("this input as invalid, as by re-prompting the user to type in another number.")


for i in range(1, h+1):
    string = ""
    for _ in range(h-i):
        string += " "
    for _ in range(i):
        string += "#"
    print(string)
