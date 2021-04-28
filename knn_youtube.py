# use panda, numpy, scipy, mirar operator
# columnas title, like count, comment count, views


import csv
import pandas


def loadCsv():
    # loads csv and reads it into an int array
    lines = csv.reader(open(r'machineLearningImproved.csv'))
    dataset = list(lines)

    for i in range(0, len(dataset)):
        (dataset[i][0]) = int(dataset[i][0])
        (dataset[i][1]) = int(dataset[i][1])

        (dataset[i][2]) = int(dataset[i][2])
        (dataset[i][3]) = int(dataset[i][3])
        (dataset[i][4]) = int(dataset[i][4])


    return dataset


video_dataset = loadCsv()


# using euclidean distance to calculate distance between two points, the points being the given video by the user and
# a video from the dataset.

def euclidean_distance(pt1, pt2):
    difference = 0
    # to calculate the distances between the points we calculate euclidean distance,
    # by squaring and rooting all the given parameters of that point
    for i in range(4):
        difference = difference + (int(pt1[i]) - int(pt2[i])) ** 2
        distance = difference ** 0.5

    return distance


# this function takes max and minimum values normalized the distances and then do the value minus the minimum and
# max minus min the new normalizes distances and titles are appended.

def normalize_distances(a_list_of_distances):
    maximum = max(a_list_of_distances)
    minimum = min(a_list_of_distances)
    normalized_list = []
    for value in a_list_of_distances:
        new_value = (value[0] - minimum[0]) / (maximum[0] - minimum[0])
        normalized_list.append([new_value, value[1]])

    return normalized_list


def get_k_neighbors(video_input, dataset, k):
    # new distances
    distances = []
    # loops through all the videos
    for video_info in dataset:
        # applies euclidean distance function
        final_distance = euclidean_distance(video_info, video_input)
        # appends this and title
        distances.append([final_distance, video_info[5]])
    # applies normalization
    normalized = normalize_distances(distances)
    # use sorting in reverse to get closest neigbors(distances)
    normalized.sort()
    # assigns first K



    neighbors = normalized[0:k]
    KNN = []
    # add to KNN and returns
    i = 0
    for i in range(0, len(neighbors)):
        # KNN.append(neighbors[i])
        KNN.append(neighbors[i][1])

    return KNN


# Testing with 5 different outputs
print(get_k_neighbors((168302,4621,99,784,27,"Overgeared Traxxas X-Maxx FLAT OUT offroad (maximum abuse!),Education,https://www.youtube.com/watch?v=EnrWjK8Emr0"), video_dataset, 20))
print(get_k_neighbors((414102,32572,128,750,1,"Michael Reeves RUST Adventure | Animation,Film & Animation,https://www.youtube.com/watch?v=o4B-Um22y-U"),video_dataset, 20))
print(get_k_neighbors((45562,5601,35,368,20,"HOW is he Putting Up a Fight!? | Dragon Ball FighterZ,Gaming,https://www.youtube.com/watch?v=rhrkkt7E_k8"),video_dataset, 20))
print(get_k_neighbors((6479599,199314,7461,8545,23,"memes that are actually funny,Comedy,https://www.youtube.com/watch?v=rk3-Av1KblM"),video_dataset, 20))
print(get_k_neighbors((27837,1419,4,70,20,"warm up games on ana are always the sweatiest w/ @bogur,Gaming,https://www.youtube.com/watch?v=ksmx5kHWmbc"),video_dataset, 20))