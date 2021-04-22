from flask import Flask, render_template, url_for, request, redirect
from youtubeTool import app
from googleapiclient.discovery import build

youtube_API_KEY = "AIzaSyD8E1MLYfX4cNw379bjjHBxQUy3TrbOYro"

youtube_API = build('youtube', 'v3', developerKey = youtube_API_KEY)

@app.route("/", methods=['POST', 'GET'])
@app.route("/home", methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        video_url = request.form['']
        return redirect(url_for('result', video_id = input_button))
    else:
        return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route("/recco",methods=['POST','GET'])
def recco():
    return(render_template('recco.html'))

@app.route("/info",methods=['POST','GET'])
def info():
    return(render_template('info.html'))

@app.route('/playlist',methods=['POST','GET'])
def playlist():
    return render_template('results.html')

@app.route("/results", methods=['POST', 'GET'])
def result():
    if request.method == "GET":
        video_id = request.args['video_id']
        results = get_video_info(video_id)
        return render_template("result.html", title='Result', result=result)
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

    CategoryID = result['items'][0]['snippet']['CategoryID']
    Title = result['items'][0]['snippet']['title']

    data = [Title, viewCount, likeCount, dislikeCount, commentCount, CategoryID]

    return(data)