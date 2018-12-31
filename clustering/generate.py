def gen(dim, number_of_points):
    import random
    return [[random.randint(1, 100)
             for i in range(dim)] for j in range(number_of_points)]
