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


    B = (26966888,581645,29449,26872,24, "iconic vines that changed the world")

    machine_learning_data = (get_neighbors(data, video_dataset, 20))

    return(machine_learning_data)


def loadCsv():
    lines = csv.reader(open(r'machineLearningImproved.csv'))
    dataset = list(lines)

    for i in range(0, len(dataset)):
        (dataset[i][0]) = int(dataset[i][0])
        (dataset[i][1]) = int(dataset[i][1])

        (dataset[i][2]) = int(dataset[i][2])
        (dataset[i][3]) = int(dataset[i][3])
        (dataset[i][4]) = int(dataset[i][4])

        # dataset[i][0] = int(dataset[i][j])
        # print(type(dataset[i][j]))
    return dataset



# using euclidean distance to calculate distance between two points
def euclidean_distance(pt1, pt2):
    difference = 0

    for i in range(4):
        difference = difference + (int(pt1[i]) - int(pt2[i])) ** 2
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
#distances_list = [26600015.934873667, 26810312.35429192, 20677961.542909663, 210336.3035403066, 5922468.372980644, 6132713.911467173]


# A function that normalizes the results so that the data is more usable and appropriate scale
# takes values for videos list and returns them normalized

def normalize_distances(a_list_of_distances):
    #print("title to append is")
    #print(a_list_of_distances)

    maximum = max(a_list_of_distances)
    minimum = min(a_list_of_distances)
    normalized_list = []
    for value in a_list_of_distances:

        #print(value[1])
        #print("minimum and maximum")
        #print(minimum[0], maximum[0])

        new_value = (value[0] - minimum[0]) / (maximum[0] - minimum[0])
        normalized_list.append([new_value, value[1], value[2]])
        #print(normalized_list)
    return normalized_list


# This function returns k number of closest neighbors
def get_neighbors(video_input, dataset, k):
    # new distances
    distances = []
    for title in dataset:
        video_info = title

        #print("dataset is")
        #print(dataset)

        final_distance = euclidean_distance(video_info, video_input)

        #print("final distance between given video and dataset is ")
        #print(video_info)
        #print(final_distance)

        distances.append([final_distance, title[5], title[7]])
        #print(distances)

    normalized = normalize_distances(distances)
    normalized.sort(reverse=True)
    #print(normalized)

    #print(x)

    neighbors = normalized[0:k]
    KNN = []
    i = 0

    for i in range(0, len(neighbors)):
        #KNN.append(neighbors[i])
        KNN.append([neighbors[i][1], neighbors[i][2]])

    return KNN


#sample of a video that would be tested against
#iconic_vines_2 = (26966888, 581645, 29449, 26872, 24, "iconic vines that changed the world 2")
#testing different results
