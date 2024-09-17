import numpy as np

def random_pairs():
    with open("graphs\web-wikipedia2009.mtx", "r") as file:
        lines = file.readlines()

    column1 = []
    column2 = []
    for line in lines:
        nums = line.split()  # Assuming columns are separated by whitespace
        column1.append((nums[0]))  # Convert to float if needed
        column2.append((nums[1]))

    column1_array = np.array(column1)
    column2_array = np.array(column2)

    random_indices_column1 = np.random.choice(len(column1_array), size=1000, replace=False)
    random_indices_column2 = np.random.choice(len(column2_array), size=1000, replace=False)

    random_pairs = np.vstack((column1_array[random_indices_column1], column2_array[random_indices_column2])).T

    with open("pairs/random_pairs_wikipedia2009.txt", "w") as file:
        for pair in random_pairs:
            file.write(f"{pair[0]} {pair[1]}\n")


random_pairs()