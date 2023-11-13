from flask import Flask, request, jsonify
from googleapiclient.discovery import build
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
API_KEY = 'AIzaSyBfnqL3eTT9Ihxy7uu_VoEdRR3EdCTVeq0'

@app.route('/')
def index():
    return "Welcome to the YouTube search API"

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()  # Retrieve JSON data
    search_query = data.get('search_query')  # Access 'search_query' from the JSON
    print('Hello')
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    # ... (rest of your code remains the same)

    
    search_response = youtube.search().list(
        q=search_query,
        type='video',
        part='id',
        maxResults=5
    ).execute()

    videos = []
    for search_result in search_response.get('items', []):
        video_id = search_result['id']['videoId']
        video_response = youtube.videos().list(
            id=video_id,
            part='snippet,statistics'
        ).execute()

        video_data = video_response.get('items', [])[0]
        video_info = {
            'title': video_data['snippet']['title'],
            'url': f'https://www.youtube.com/watch?v={video_id}',
            'views': int(video_data['statistics']['viewCount']),
            'likes': int(video_data['statistics']['likeCount']),
            'comments': int(video_data['statistics']['commentCount'])
        }
        video_info['total_count'] = video_info['likes'] + video_info['comments'] + video_info['views']
        videos.append(video_info)

    videos.sort(key=lambda x: x['total_count'], reverse=True)
    print(videos)
   
    return jsonify(videos)

if __name__ == '__main__':
    app.run(debug=True)
