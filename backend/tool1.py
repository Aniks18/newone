from flask import Flask, request, jsonify, send_from_directory
import json
import os
import logging
from flask_cors import CORS

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)

@app.route('/search', methods=['POST'])
def search():
    try:
        logging.debug('Received request with headers: %s', request.headers)
        logging.debug('Received request data: %s', request.data)

        data = request.json
        if not data:
            raise ValueError('No JSON data received or invalid JSON format')

        search_query = data.get('query', '')
        location = data.get('location', '')

        if not search_query or not location:
            raise ValueError('Both query and location must be provided')

        logging.debug('Extracted search query: %s', search_query)
        logging.debug('Extracted location: %s', location)

        data_to_save = {
            'query': search_query,
            'location': location
        }

        file_path = 'backend/data.json'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w') as json_file:
            json.dump(data_to_save, json_file, indent=4)
        
        logging.info('Data successfully saved to %s', file_path)
        
        response_message = f'Search Query: "{search_query}", Location: "{location}"'
        return jsonify({'message': response_message})
    
    except ValueError as ve:
        logging.error('ValueError occurred: %s', str(ve))
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        logging.error('An unexpected error occurred: %s', str(e))
        return jsonify({'error': 'An unexpected error occurred'}), 500


@app.route('/api/results', methods=['GET'])
def get_results():
    try:
        file_path = os.path.join('backend', 'results.json')
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'{file_path} not found')

        with open(file_path, 'r') as json_file:
            results_data = json.load(json_file)
        
        return jsonify(results_data)

    except Exception as e:
        logging.error('Error occurred while fetching results: %s', str(e))
        return jsonify({'error': 'Failed to fetch results'}), 500

@app.route('/api/twitterresults', methods=['GET'])
def get_twitter_results():
    try:
        file_path = os.path.join('backend', 'twitterresult.json')
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'{file_path} not found')

        with open(file_path, 'r') as json_file:
            twitter_data = json.load(json_file)
        
        return jsonify(twitter_data)

    except Exception as e:
        logging.error('Error occurred while fetching Twitter results: %s', str(e))
        return jsonify({'error': 'Failed to fetch Twitter results'}), 500

@app.route('/api/image', methods=['GET'])
def get_image():
    try:
        image_path = os.path.join('backend', 'hashtag_analysis.png')
        
        if not os.path.exists(image_path):
            raise FileNotFoundError(f'{image_path} not found')

        return send_from_directory(directory='backend', path='hashtag_analysis.png')

    except Exception as e:
        logging.error('Error occurred while fetching image: %s', str(e))
        return jsonify({'error': 'Failed to fetch image'}), 500
    
@app.route('/api/wordcloud', methods=['GET'])
def get_wordcloud():
    try:
        image_path = os.path.join('backend', 'hashtag_wordcloud.png')
        
        if not os.path.exists(image_path):
            raise FileNotFoundError(f'{image_path} not found')

        return send_from_directory(directory='backend', path='hashtag_wordcloud.png')

    except Exception as e:
        logging.error('Error occurred while fetching wordcloud image: %s', str(e))
        return jsonify({'error': 'Failed to fetch wordcloud image'}), 500


@app.route('/api/temporal', methods=['GET'])
def get_temporal():
    try:
        image_path = os.path.join('backend', 'temporal_analysis.png')
        
        if not os.path.exists(image_path):
            raise FileNotFoundError(f'{image_path} not found')

        return send_from_directory(directory='backend', path='temporal_analysis.png')

    except Exception as e:
        logging.error('Error occurred while fetching temporal analysis image: %s', str(e))
        return jsonify({'error': 'Failed to fetch temporal analysis image'}), 500


if __name__ == '__main__':
    app.run(port=5000)
