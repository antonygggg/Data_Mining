# linear regression

import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score


def generate_2d_list(rows, cols, min_x, max_x):
    from random import randint
    return [[randint(min_x, max_x) for _ in range(cols)] for _ in range(rows)]


def generate_line(a, b, x, diff):
    from random import randint
    return [a * x_i + b + randint(1, diff) for x_i in x]


def main():
    from random import randint
    a = randint(-10, 10)
    b = randint(-10, 10)
    points = 500
    range_min = 1
    range_max = 1200
    diff_y_range = range_max - range_min
    test_set_size = int(0.1 * points)

    print(
        "x : points = {0}, min = {1}, max = {2}, \n"
        "line : a = {3}, b = {4}, difference "
        "of each point = 0 to {5}\n".format(
            points, range_min, range_max, a, b, diff_y_range))

    x = np.array(generate_2d_list(points, 4, range_min, range_max))[
        :, np.newaxis, 2]
    y = np.array(generate_line(
        a, b, (list(np.transpose(x).tolist()))[0], diff_y_range))
    x_train = x[:-test_set_size]
    y_train = y[:-test_set_size]
    x_test = x[-test_set_size:]
    y_test = y[-test_set_size:]
    r = linear_model.LinearRegression()
    r.fit(x_train, y_train)
    y_pred = r.predict(x_test)
    a_pred = r.coef_[0]
    b_pred = y_pred[0] - r.coef_[0] * x_test[0][0]

    print('result line : coefficients =', a_pred, ', b =', b_pred,
          ', mean squared error =',
          mean_squared_error(y_test, y_pred),
          ', variance score =', r2_score(y_test, y_pred))

    plt.scatter(x_test, y_test, color='dodgerblue', s=6)
    plt.plot(x_test, y_pred, color='grey', linewidth=1.5)

    plt.show()
    plt.gcf().clear()


if __name__ == '__main__':
    main()
