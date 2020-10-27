from impl import santa
import numpy as np


def GaSantaTest():
    users = np.array(["ulf", "lotta", "kalle", "petra", "olof", "pikachu"])
    gift_rate = np.array([1.0, 2.0, 3.0, 1.0, 0.1, 1.0])
    gifts = np.random.choice(users, 200, p=gift_rate / gift_rate.sum())


    print(users, gifts)

    ga_santa = santa.GaOptimizingSanta(None)
    print(ga_santa.sort(gifts))


if __name__ == "__main__":
    GaSantaTest()
