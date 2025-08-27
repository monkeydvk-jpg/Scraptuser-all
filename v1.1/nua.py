from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace with your actual API key and access token
API_KEY = 'YOUR_API_KEY'
ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'

@app.route('/get_download_url', methods=['POST'])
def get_download_url():
    image_id = request.json.get('image_id')
    
    if not image_id:
        return jsonify({'error': 'Image ID is required'}), 400

    # Step 1: Get the comp URL
    comp_url_endpoint = f'https://stock.adobe.io/Rest/Media/1/Files?ids={image_id}&result_columns[]=comp_url'
    headers = {
        'X-Product': 'MySampleApp/1.0',
        'x-api-key': API_KEY,
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }

    response = requests.get(comp_url_endpoint, headers=headers)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to get comp URL'}), 500

    comp_url = response.json()['files'][0]['comp_url']

    # Step 2: Get the download URL
    download_url_endpoint = f'{comp_url}?token={ACCESS_TOKEN}'
    response = requests.get(download_url_endpoint, allow_redirects=False)
    
    if response.status_code == 302:
        download_url = response.headers['Location']
        return jsonify({'download_url': download_url})
    else:
        return jsonify({'error': 'Failed to get download URL'}), 500

if __name__ == '__main__':
    app.run(debug=True)
