import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, 'twitterresult.json')

class DataChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == data_path:
            print("data.json has been modified. Processing...")
            process_data()

def process_data():
    # Load JSON data
    try:
        with open(data_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: The file 'data.json' was not found in the directory: {script_dir}")
        print("Please ensure that the data file is in the same directory as this script.")
        return
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON. Please check the format of 'data.json'.")
        return

    # Convert JSON data to DataFrame
    df = pd.json_normalize(data)

    # Temporal Analysis
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        def temporal_analysis(df):
            df.set_index('date', inplace=True)
            daily_counts = df.resample('D').size()
            monthly_counts = df.resample('M').size()

            plt.figure(figsize=(14, 7))
            plt.subplot(2, 1, 1)
            daily_counts.plot()
            plt.title('Daily Post Counts')
            plt.xlabel('Date')
            plt.ylabel('Number of Posts')

            plt.subplot(2, 1, 2)
            monthly_counts.plot()
            plt.title('Monthly Post Counts')
            plt.xlabel('Date')
            plt.ylabel('Number of Posts')

            plt.tight_layout()
            plt.savefig('temporal_analysis.png')
            plt.close()

        temporal_analysis(df)

    # Hashtag Analysis
    def hashtag_analysis(df):
        if 'hashtags' not in df.columns:
            print("Error: 'hashtags' column not found in the dataset.")
            return

        hashtags = df['hashtags'].dropna().apply(lambda x: [tag.lower() for tag in x])
        all_hashtags = [hashtag for sublist in hashtags for hashtag in sublist]
        hashtag_counts = Counter(all_hashtags)

        top_hashtags = hashtag_counts.most_common(10)
        hashtag_df = pd.DataFrame(top_hashtags, columns=['Hashtag', 'Count'])

        plt.figure(figsize=(10, 8))
        sns.barplot(x='Count', y='Hashtag', data=hashtag_df)
        plt.title('Top 10 Hashtags')
        plt.xlabel('Count')
        plt.ylabel('Hashtag')
        plt.savefig('hashtag_analysis.png')
        plt.close()

        # Word Cloud for Hashtags
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(hashtag_counts)
        plt.figure(figsize=(10, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Hashtag Word Cloud')
        plt.savefig('hashtag_wordcloud.png')
        plt.close()

    hashtag_analysis(df)

    # Mention Analysis
    def mention_analysis(df):
        if 'content' not in df.columns:
            print("Error: 'content' column not found in the dataset.")
            return

        mentions = df['content'].dropna().apply(lambda x: [mention.lower() for mention in x.split() if mention.startswith('@')])
        all_mentions = [mention for sublist in mentions for mention in sublist]
        mention_counts = Counter(all_mentions)

        top_mentions = mention_counts.most_common(10)
        mention_df = pd.DataFrame(top_mentions, columns=['Mention', 'Count'])

        plt.figure(figsize=(10, 8))
        sns.barplot(x='Count', y='Mention', data=mention_df)
        plt.title('Top 10 Mentions')
        plt.xlabel('Count')
        plt.ylabel('Mention')
        plt.savefig('mention_analysis.png')
        plt.close()

    mention_analysis(df)

    print("Results have been written to twitterresult.json")

if __name__ == "__main__":
    event_handler = DataChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=script_dir, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
