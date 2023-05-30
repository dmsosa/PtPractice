def run():
    import numpy as np
    while True:
        values = np.array([3, 1.5, 0, -1, -1.5])
        califications = list()
        while len(califications) < 5:
            try:
                cal = input("")
                for i in range(5):
                    cent = input("%"+str(i))
                    per = int(cal)*(int(cent)/100)
                    califications.append(int(per))
            except:
                return
        max = int(cal)*3
        r = np.dot(califications, values)
        print("max = ", max ) 
        print("10 percent ",max*0.1)
        print("50 percent ",max*0.5)
        print("30 percent ",max*0.3)
        print(r)
        print("dif =", max-r)

    


if __name__ == '__main__':
    run()