import requests

url = "http://127.0.0.1:5001/upload_video"
video_path = "videos/1.mp4"

with open(video_path, 'rb') as video_file:
    files = {'video': video_file}
    response = requests.post(url, files=files)

try:
    response_data = response.json()
    if response.status_code == 200:
        print("✅ Server Response:")
        print(response_data)
    else:
        print("❌ Error:", response_data.get("error", "Unknown error"))
except requests.exceptions.JSONDecodeError:
    print("❌ Failed to parse JSON response:")
    print(response.text)
