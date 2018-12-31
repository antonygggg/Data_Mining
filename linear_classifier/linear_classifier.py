# linear classifier


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def distance(p1, p2):
        return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5


class Line:
    def __init__(self, a, b, x, line_type):
        self.a = a
        self.b = b
        self.x = x
        self.line_type = line_type  # l : y = a * x + b , s : x = b


def get_center(points):
    if not points:
        return None
    len_p = len(points)
    x = sum([p.x for p in points]) / len_p
    y = sum([p.y for p in points]) / len_p
    return Point(x, y)


def get_classifier_line_two_points(p1, p2):
    if p1.x == p2.x and p1.y == p2.y:
        return Line(0, p1.y, float('nan'), 'l')
    elif p1.x == p2.x:
        b = (p1.y - p2.y) / 2 if p1.y > p2.y else (p2.y - p1.y) / 2
        return Line(0, b, float('nan'), 'l')
    else:

        connect_line_a = (p1.y - p2.y) / (p1.x - p2.x)

        common_point_x = (p1.x - p2.x) / \
            2 if p1.x > p2.x else (p2.x - p1.x) / 2
        common_point_y = (p1.y - p2.y) / \
            2 if p1.y > p2.y else (p2.y - p1.y) / 2

        if connect_line_a == 0:
            b = (p1.x - p2.x) / 2 if p1.x > p2.x else (p2.x - p1.x) / 2
            return Line(float('nan'), float('nan'), b, 's')

        separate_line_a = -1 / connect_line_a
        separate_line_b = common_point_y - separate_line_a * common_point_x
        return Line(separate_line_a, separate_line_b, float('nan'), 'l')


def get_classifier_line_list(data, tag1, tag2):
    min_x = data[0][0]
    max_x = data[0][0]
    min_y = data[0][1]
    max_y = data[0][1]

    points_tag1 = [Point(p[0], p[1]) for p in data if p[2] == tag1]
    points_tag2 = [Point(p[0], p[1]) for p in data if p[2] == tag2]

    center_tag1 = get_center(points_tag1)
    center_tag2 = get_center(points_tag2)

    line = get_classifier_line_two_points(center_tag1, center_tag2)

    if not center_tag1 or not center_tag2:
        return None

    for p in data:
        if p[0] > max_x:
            max_x = p[0]
        elif p[0] < min_x:
            min_x = p[0]
        if p[1] > max_y:
            max_y = p[1]
        elif p[1] < min_y:
            min_x = p[1]
    if line:
        if line.line_type == 's':
            return [Point(line.x, p[1]) for p in data]
        elif line.a == 0:
            return [Point(p[0], line.b) for p in data]
        return [Point(p[0], line.a * p[0] + line.b) for p in data]


def print_result(line_x, line_y, tag1_points, tag2_points):
    import matplotlib.pyplot as plt
    for item in tag1_points + tag2_points:
        print(item)
    t_x = [p[0] for p in tag1_points]
    t_y = [p[1] for p in tag1_points]
    plt.scatter(t_x, t_y)
    t_x = [p[0] for p in tag2_points]
    t_y = [p[1] for p in tag2_points]
    plt.scatter(t_x, t_y)
    plt.plot(line_x, line_y, color='black', linewidth=3)
    plt.show()
    plt.gcf().clear()


def get_random_data(number_of_points, min_x, min_y, max_x, max_y,
                    tag1="a", tag2="b"):
    from random import randint
    data = []
    for _ in range(number_of_points):
        t = [randint(min_x, max_x), randint(min_y, max_y),
             tag1 if randint(0, 1) % 2 == 0 else tag2]
        data.append(t)
    return data


def get_random_area(number_of_points, radius, x, y, tag):
    from random import randint
    data = []
    for _ in range(number_of_points):
        t = [randint(x - radius, x + radius),
             randint(y - radius, y + radius), tag]
        data.append(t)
    return data


def read_data(filename):
    import csv
    if not filename:
        return None
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            return [row for row in reader]
    except Exception as e:
        print('error : ', e)
        return None


def main():
    # pre learn data arrange
    # 1 - age , 5 - balance , 7 - loan
    # the first row is caption so we skip it
    raw_data = read_data('bank.csv')[1:]
    data = [[int(row[0]), int(row[5]), row[7]] for row in raw_data]
    tags = list(set([row[2] for row in data]))
    tag1, tag2 = tags[0], tags[-1]

    line = list(get_classifier_line_list(data, tag1, tag2))
    points_tag1 = [p for p in data if p[2] == tag1]
    points_tag2 = [p for p in data if p[2] == tag2]
    line_x = [p.x for p in line]
    line_y = [p.y for p in line]
    print_result(line_x, line_y, points_tag1, points_tag2)

    # example of two areas with different tags
    data = get_random_area(100, 50, 20, 10, 'a') + \
        get_random_area(100, 50, 100, 100, 'b')
    tags = list(set([row[2] for row in data]))
    tag1, tag2 = tags[0], tags[-1]

    line = list(get_classifier_line_list(data, tag1, tag2))
    points_tag1 = [p for p in data if p[2] == tag1]
    points_tag2 = [p for p in data if p[2] == tag2]
    line_x = [p.x for p in line]
    line_y = [p.y for p in line]
    print_result(line_x, line_y, points_tag1, points_tag2)


if __name__ == '__main__':
    main()
