for a in range(3, 1000000, 2):
    for j in range(3, (a - 1) / 2, 2):
        if (a % j == 0):
            break

        if (((a - 1) / 2) % 2 == 0):
            if (j == (a - 1) / 2 - 1 ):
                print(a)
                break
        else:
            if (j == (a - 1) / 2 - 2 ):
                print(a)
                break



                