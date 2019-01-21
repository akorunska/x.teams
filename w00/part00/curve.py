import numpy as np
import matplotlib.pyplot as plt


def main():
    a = 4
    b = 9

    y, x = np.ogrid[-20:20:100j, -20:20:100j]
    plt.contour(x.ravel(), y.ravel(), pow(y, 2) - pow(x, 3) - x * a - b, [0])
    plt.grid()
    plt.show()


if __name__ == '__main__':
    main()
