import time
import json
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from opencage.geocoder import OpenCageGeocode
from collections import Counter
import re
from deep_translator import GoogleTranslator
from typing import List, Dict, Any
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Initialize geocoder with your API key
OPENCAGE_API_KEY = '98983cac27924ea9b0ba4bc40742750b'
geocoder = OpenCageGeocode(OPENCAGE_API_KEY)

# Initialize translator
translator = GoogleTranslator(source='auto', target='en')

def process_query(query: str, location: str) -> Dict[str, Any]:
    """
    Process the query and location to generate search results and additional information.
    """
    try:
        # Get location suggestions
        location_info = geocoder.geocode(location)
        location_suggestions = [result['formatted'] for result in location_info] if location_info else [location]
        
        # Use the first suggestion for simplicity
        if location_suggestions:
            location = location_suggestions[0]

        # Search for news articles
        search_query = f"{query} {location}"
        search_results = search(search_query, num_results=10)
        
        results = []
        for url in search_results:
            try:
                article_data = fetch_article_data(url)
                if article_data:
                    results.append(article_data)
            except Exception as e:
                print(f"Error fetching data for {url}: {e}")
                continue

        # Generate summary and key points
        all_text = " ".join(f"{result['title']} {result['snippet']}" for result in results)
        summary = summarize_text(all_text)
        key_points = extract_key_points(all_text)

        # Get Instagram results
        instagram_results = search_instagram(query, location)

        return {
            "query": query,
            "location": location,
            "results": results,
            "summary": summary,
            "key_points": key_points,
            "instagram_results": instagram_results
        }

    except Exception as e:
        print(f"Error during processing: {e}")
        return {"error": str(e)}

def fetch_article_data(url: str) -> Dict[str, Any]:
    """
    Fetch and parse article data from a given URL.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title = soup.title.string if soup.title else "No Title"
    snippet = ' '.join(p.text for p in soup.find_all('p')[:3])
    published_date = soup.find('meta', {'property': 'article:published_time'})
    published_date = published_date['content'] if published_date else "No Date"
    source = soup.find('meta', {'property': 'og:site_name'})
    source = source['content'] if source else "No Source"
    image = soup.find('meta', {'property': 'og:image'})
    image_url = image['content'] if image else "No Image"

    report_links = find_report_links(soup, url)

    return {
        'title': title,
        'snippet': snippet,
        'link': url,
        'publishedAt': published_date,
        'source': source,
        'image': image_url,
        'report_links': report_links
    }

def find_report_links(soup: BeautifulSoup, url: str) -> List[Dict[str, str]]:
    """
    Find related report links from the parsed HTML.
    """
    report_links = []
    disaster_keywords = [
        'disaster', 'accident', 'destruction', 'flood', 'landslide', 'earthquake', 
        'hurricane', 'tornado', 'tsunami', 'fire', 'explosion'
    ]
    
    if 'reliefweb.int' in url:
        report_elements = soup.find_all('a', class_='resource-title')
        for element in report_elements:
            if any(keyword in element.text.lower() for keyword in disaster_keywords):
                report_links.append({
                    'title': element.text.strip(),
                    'url': 'https://reliefweb.int' + element['href'] if element['href'].startswith('/') else element['href']
                })
                if len(report_links) == 5:
                    return report_links
    else:
        for a in soup.find_all('a', href=True):
            if any(keyword in a.text.lower() for keyword in disaster_keywords):
                report_links.append({
                    'title': a.text.strip(),
                    'url': a['href'] if a['href'].startswith('http') else f"{url.rstrip('/')}/{a['href'].lstrip('/')}"
                })
                if len(report_links) == 5:
                    return report_links
    
    return report_links

def summarize_text(text: str, sentences_count: int = 3) -> str:
    """
    Generate a summary of the given text.
    """
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    words = re.findall(r'\w+', text.lower())
    word_freq = Counter(words)
    
    sentence_scores = []
    for sentence in sentences:
        score = sum(word_freq[word.lower()] for word in re.findall(r'\w+', sentence))
        sentence_scores.append((score, sentence))
    
    top_sentences = sorted(sentence_scores, reverse=True)[:sentences_count]
    return ' '.join(sentence for _, sentence in sorted(top_sentences, key=lambda x: sentences.index(x[1])))

def extract_key_points(text: str, num_points: int = 5) -> List[str]:
    """
    Extract key points from the given text.
    """
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    words = re.findall(r'\w+', text.lower())
    word_freq = Counter(words)
    
    common_words = word_freq.most_common(num_points)
    
    key_points = []
    for word, _ in common_words:
        for sentence in sentences:
            if word in sentence.lower():
                key_points.append(sentence)
                break
    
    return key_points[:num_points]

def search_instagram(query: str, location: str, num_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search Instagram for posts related to the query and location.
    """
    hashtag = f"{query.replace(' ', '')}in{location.replace(' ', '')}"
    url = f"https://www.instagram.com/explore/tags/{hashtag}/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        script = soup.find('script', text=re.compile('window._sharedData'))
        
        if script:
            json_data = script.string.split('window._sharedData = ')[1].split(';</script>')[0]
            data = json.loads(json_data)
            
            posts = data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']
            
            results = []
            for post in posts[:num_results]:
                node = post['node']
                results.append({
                    'url': f"https://www.instagram.com/p/{node['shortcode']}/",
                    'image_url': node['display_url'],
                    'caption': node['edge_media_to_caption']['edges'][0]['node']['text'] if node['edge_media_to_caption']['edges'] else '',
                    'likes': node['edge_liked_by']['count'],
                    'comments': node['edge_media_to_comment']['count']
                })
            
            return results
    except Exception as e:
        print(f"Error fetching Instagram data: {str(e)}")
        return []

def process_data_json():
    """
    Process the data from data.json and write results to results.json.
    """
    try:
        # Read data from data.json
        with open('data.json', 'r') as f:
            data = json.load(f)
        
        query = data.get('query', '')
        location = data.get('location', '')
        
        if not query or not location:
            raise ValueError("Query and location must be provided in data.json")
        
        # Process the query and location
        results = process_query(query, location)
        
        # Write results to a file
        with open('results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print("Results have been written to results.json")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        # Write error to a file
        with open('error.json', 'w') as f:
            json.dump({"error": str(e)}, f, indent=2)

class DataJSONHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('data.json'):
            print("data.json has been modified. Processing...")
            process_data_json()

def main():
    """
    Main function to set up the file watcher and start monitoring data.json.
    """
    event_handler = DataJSONHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    try:
        print("Monitoring data.json for changes. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()