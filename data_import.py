import requests
import zipfile
import io

# URL of the zip file
url = 'https://www.scribbr.com/wp-content/uploads//2020/02/heart.data_.zip'

# Headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
# Fetch the file from the URL
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Use BytesIO to handle the binary data of the zip file
    zip_file = zipfile.ZipFile(io.BytesIO(response.content))
    # Extract all the contents
    zip_file.extractall('.')
    print(f"File extracted")
else:
    print(f"Failed to fetch the file. Status code: {response.status_code}")
