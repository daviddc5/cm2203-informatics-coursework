from flask import Flask, render_template, url_for, request, redirect
from youtubeTool import app
from googleapiclient.discovery import build
import csv
import pandas
# use panda, numpy, scipy, mirar operator
# columnas title, like count, comment count, views

youtube_API_KEY = "AIzaSyD8E1MLYfX4cNw379bjjHBxQUy3TrbOYro"

youtube_API = build('youtube', 'v3', developerKey = youtube_API_KEY)

@app.route("/", methods=['POST', 'GET'])
@app.route("/home", methods=['POST', 'GET'])
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route("/recco",methods=['POST','GET'])
def recco():
    if request.method == "POST":
        video_url = request.form['search_videoLink']
        return redirect(url_for('results', link = video_url))
    else:
        return(render_template('recco.html'))

@app.route("/info",methods=['POST','GET'])
def info():
    return(render_template('info.html'))

@app.route("/allVideos", methods=['POST','GET'])
def machineReadable():
    return(render_template('allVideos.html'))

@app.route("/results", methods=['POST', 'GET'])
def results():
    if request.method == "GET":
        link = request.args['link']
        video_data = get_video_info(link)
        results = machineLearning_function(video_data)
        return render_template("results.html", title='Results', results=results)
    else:
        return render_template('home.html')

def get_video_info(video_link):
    h = 0

    for h in range(0, len(video_link) - 1):
        if video_link[h] == "v" and video_link[h+1] == "=":
            video_ID = (video_link[(h+2):])

    request = youtube_API.videos().list(
        part = 'statistics',
        id = video_ID
        )

    video_info = request.execute()

    viewCount = video_info["items"][0]["statistics"]["viewCount"]
    likeCount = video_info["items"][0]["statistics"]["likeCount"]
    dislikeCount = video_info["items"][0]["statistics"]["dislikeCount"]
    commentCount = video_info["items"][0]["statistics"]["commentCount"]

    request_categoryInfo = youtube_API.videos().list (
        part='snippet',
        id=video_ID
        )

    video_category_info = request_categoryInfo.execute()

    videoID = video_category_info['items'][0]['snippet']['categoryId']
    Title = video_category_info['items'][0]['snippet']['title']

    data = [viewCount, likeCount, dislikeCount, commentCount, videoID, Title]

    return(data)


def machineLearning_function(data):
    video_dataset = loadCsv()


    machine_learning_data = (get_k_neighbors(data, video_dataset, 20))

    return(machine_learning_data)


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
        normalized_list.append([new_value, value[1], value[2]])

    return normalized_list


def get_k_neighbors(video_input, dataset, k):
    # new distances
    distances = []
    # loops through all the videos
    for video_info in dataset:
        # applies euclidean distance function
        final_distance = euclidean_distance(video_info, video_input)
        # appends this and title
        distances.append([final_distance, video_info[5], video_info[7]])
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
        KNN.append([neighbors[i][1], neighbors[i][2]])

    return KNN


