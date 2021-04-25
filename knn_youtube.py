# use panda, numpy, scipy, mirar operator
# columnas title, like count, comment count, views


import csv
import pandas


def loadCsv():
    lines = csv.reader(open(r'machineLearningImproved.csv'))
    dataset = list(lines)


    for i in range(0, len(dataset)):

        
        (dataset[i][0]) = int(dataset[i][0])
        (dataset[i][1]) = int(dataset[i][1])

        (dataset[i][2]) = int(dataset[i][2])
        (dataset[i][3]) = int(dataset[i][3])
        (dataset[i][4]) = int(dataset[i][4])


                #dataset[i][0] = int(dataset[i][j])
                #print(type(dataset[i][j]))
    return dataset


video_dataset = loadCsv()
"""
print(type(video_dataset[0][0]))
print(video_dataset)
"""

iconic_vines = [26966888, 581645, 29449, 26872, 24, "iconic vines that changed the world"]
Funny_Vines_March = [373128, 6136, 143, 276, 24, "Funny Vines March 2021 (Part 1) TBT Clean Vine"]
Memes_that_have_power = [162793, 5623, 137, 810, 23, "Memes that have the power of God and Anime on their side"]
funny_memes = [6292544, 195949, 7322, 8359, 23, "memes that are actually funny"]


# using euclidean distance to calculate distance between two points
def euclidean_distance(pt1, pt2):
    difference = 0

    for i in range(len(pt1) - 1):
        difference = difference + (pt1[i] - pt2[i]) ** 2
        distance = difference ** 0.5

    return distance


"""
print("The euclidean distance between video " + iconic_vines[5] + " and video " + Funny_Vines_March[5] + " is ")
print(euclidean_distance(iconic_vines, Funny_Vines_March))
print(euclidean_distance(iconic_vines, Memes_that_have_power))
print(euclidean_distance(iconic_vines, funny_memes))
print(euclidean_distance(Funny_Vines_March, Memes_that_have_power))
print(euclidean_distance(Funny_Vines_March, funny_memes))
print(euclidean_distance(Memes_that_have_power, funny_memes))

"""
# here we should have a list of all the hypotetical distances
distances_list = [26600015.934873667, 26810312.35429192, 20677961.542909663, 210336.3035403066, 5922468.372980644,
                  6132713.911467173]


# A function that normalizes the results so that the data is more usable and appropriate scale
# takes values for videos list and returns them normalized

def normalize_distances(a_list_of_distances):
    maximum = max(distances_list)
    minimum = min(distances_list)
    normalized_list = []
    for value in distances_list:
        new_value = (value - minimum) / (maximum - minimum)
        normalized_list.append(new_value)
    return normalized_list


# print(normalize_distances(distances_list))
"""
video_dataset = [(26966888, 581645, 29449, 26872, 24, "iconic vines that changed the world"),
                 (373128, 6136, 143, 276, 24, "Funny Vines March 2021 (Part 1) TBT Clean Vine"),
                 (162793, 5623, 137, 810, 23, "memes that are actually funny"), (2301143, 79879, 898, 2149, 20,
                                                                                 "When Three Idiots Attempt THE HARDEST BOSS BATTLE In Dragonball FighterZ...")]
"""
# print(distance(video_dataset[0][1], video_dataset[1][1]))


# This function returns k number of closest neighbors
def classify(video_input, dataset, k):
    # new distances
    distances = []
    for title in dataset:
        video_info = title
        # print("information on the video ")
        # print(video_info)
        final_distance = euclidean_distance(video_info, video_input)
        # print("final distance between given video and dataset is ")
        # print(final_distance)

        distances.append([final_distance, title[5]])
        # print("unsorted distances ")
        # print(distances)
        distances.sort(reverse=True)

    neighbors = distances[0:k]
    KNN = []
    i = 0
    for i in range(0, len(neighbors)):
        KNN.append(neighbors[i][1])

    return KNN


# sample of a video that would be tested against
iconic_vines_2 = (26966888, 581645, 29449, 26872, 24, "iconic vines that changed the world 2")

print(classify(iconic_vines_2, video_dataset, 34))
