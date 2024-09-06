import requests


def get_response_text(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'http://google.com/'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Failed to fetch URL: {e}")
        return None


def read_sitemap_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except IOError as e:
        print(f"Failed to read file: {e}")
        return None

