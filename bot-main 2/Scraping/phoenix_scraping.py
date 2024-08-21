import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_phoenix_news():
    url = "https://phoenixnews.io/"
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return pd.DataFrame()
    
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all articles
    articles = soup.find_all('div', class_='outCard')

    print(f"Found {len(articles)} articles")

    news_items = []

    for article in articles:
        try:
            title_tag = article.find('span', class_='news-title')
            title = title_tag.get_text(strip=True) if title_tag else 'N/A'

            card_body = article.find('div', class_='card-body')

            summary_tag = card_body.find('span', class_='card-text-title')
            summary = summary_tag.get_text(strip=True) if summary_tag else 'N/A'

            timestamp_date_tag = article.find('span', class_='dateNews')
            timestamp_date = timestamp_date_tag.get_text(strip=True) if timestamp_date_tag else 'N/A'
            timestamp_time_tag = article.find('span', class_='hourNews')
            timestamp_time = timestamp_time_tag.get_text(strip=True) if timestamp_time_tag else 'N/A'
            timestamp = f"{timestamp_date} {timestamp_time}"

            link_tag = card_body.find('a')
            link = link_tag['href'] if link_tag else 'N/A'

            print(f"Title: {title}")
            print(f"Summary: {summary}")
            print(f"Timestamp: {timestamp}")
            print(f"Link: {link}")
            
            news_items.append({
                'title': title,
                'summary': summary,
                'link': link,
                'timestamp': timestamp
            })

            print(f"Scraped Article: {title}")

        except AttributeError as e:
            print(f"Error: {e}")
            continue

    news_df = pd.DataFrame(news_items)
    return news_df

if __name__ == "__main__":
    news = get_phoenix_news()
    print(news)