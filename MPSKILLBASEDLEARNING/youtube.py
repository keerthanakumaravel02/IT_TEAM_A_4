from googleapiclient.discovery import build

# Replace 'YOUR_API_KEY' with your actual API key
API_KEY = 'AIzaSyBfnqL3eTT9Ihxy7uu_VoEdRR3EdCTVeq0'

# Create a service object for the YouTube Data API
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Search for videos based on a query
search_query = input("Enter your video choice: ")
search_response = youtube.search().list(
    q=search_query,
    type='video',
    part='id',
    maxResults=5  # Adjust the number of results as needed
).execute()

# Fetch video details for the search results
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

# Sort videos based on total count in descending order
videos.sort(key=lambda x: x['total_count'], reverse=True)

# Display the top-rated videos based on the total count
print("Top-rated videos based on total count (likes + comments + views):\n")
for idx, video in enumerate(videos, start=1):
    print(f"Video {idx}:")
    print(f"Title: {video['title']}")
    print(f"URL: {video['url']}")
    print(f"Views: {video['views']}")
    print(f"Likes: {video['likes']}")
    print(f"Comments: {video['comments']}")
    print(f"Total Count: {video['total_count']}")
    print()