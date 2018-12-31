# knn

import matplotlib.pyplot as plt
# i have used matplotlib 3.0.2


# plot methods
def plot_2d_data(points_data):
    for p in points_data:
        plt.plot(p[0], p[1], marker='o', color=p[-1], markersize=4)


def plt_result(point, tag, longest_dist=0):
    from math import ceil
    plt.plot(point[0], point[1], marker='o', color=tag, markersize=8)
    if(longest_dist and longest_dist > 0):
        circle = plt.Circle((point[0], point[1]), ceil(
            longest_dist) + 1, color='#000000', fill=False, clip_on=True)
        plt.gca().add_artist(circle)


def set_plot_figure():
    fig = plt.gcf()
    fig.canvas.set_window_title('knn')
    fig.set_size_inches(8, 6)


def show_plt():
    plt.show()


# euclids distance between two vectors
def dist(x1, x2):
    if(x1 is None or x2 is None):
        raise 'MissingParam'
    l = len(x1)
    if(l != len(x2)):
        raise 'DifferentLengthVectors'
    return (sum([(x1[i] - x2[i])**2 for i in range(l - 1)]))**0.5


# sort the list of items in ascending order by their
# distance to the target item
def sort_by_distance(target_item, items):
    if target_item is None or items is None:
        raise 'MissingParam'
    items.sort(key=lambda i: dist(i, target_item))
    return items


# count the occurrences of each tag in all tags
def count_items(list, to_sort=False):
    if list is None:
        raise 'MissingParam'
    tags = [l[-1] for l in list]
    unique_tags = set(tags)
    count = {}
    for tag in unique_tags:
        count[tag] = tags.count(tag)
    return count


def knn(item, known_items, n=3):
    sorted_items = sort_by_distance(item, known_items)[0:n]
    topn_tags = dict(count_items(sorted_items))
    sort_res = sorted(topn_tags.items(), reverse=True, key=lambda di: di[1])[0]
    top_tag_count = sort_res[1]
    # choose the nearest neighbor if there are few with the same count
    for near_item in sorted_items:
        if top_tag_count == topn_tags[near_item[-1]]:
            tag = near_item[-1]
            break
    return {'tag': tag, 'longest_dist': dist(item, sorted_items[-1])}


# generate data set
def generate_data(dimensions, count, min=1, max=400):
    from random import randint
    categories = ["#9b59b6", "#3498db", "#95a5a6",
                  "#e74c3c", "#34495e", "#2ecc71"]
    cat_len = len(categories)
    data = []
    for _ in range(count):
        item = [randint(min, max) for i in range(dimensions)]
        item.append(categories[randint(0, cat_len - 1)])
        data.append(item)
    return data


# run nearest neighbor example with generated data
def main():
    dims = 2
    data = generate_data(dims, 48)
    set_plot_figure()
    plot_2d_data(data)
    item = generate_data(dims, 1)[0]
    knn_res = knn(item, data, 3)
    tag_of_item = knn_res['tag']
    longest_dist = knn_res['longest_dist']
    plt_result(item, tag_of_item, longest_dist)
    show_plt()


if __name__ == "__main__":
    main()
