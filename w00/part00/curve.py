import numpy as np
import matplotlib.pyplot as plt


def curve():
    a = 4
    b = 9

    y, x = np.ogrid[-20:20:100j, -10:30:100j]

    plt.contour(x.ravel(), y.ravel(), pow(y, 2) - pow(x, 3) - x * a - b, [0])
    plt.grid()
    plt.show()


if __name__ == '__main__':
    curve()
