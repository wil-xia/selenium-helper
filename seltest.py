from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def get_tweets(stock_ticker, num_tweets=20):
    options = Options()
    options.add_argument("--headless") 
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service('/path/to/chromedriver')  
    driver = webdriver.Chrome(service=service, options=options)

    try:

        driver.get(f"https://twitter.com/search?q={stock_ticker}&src=typed_query")
        
        time.sleep(3) 
        
        tweets = []
        last_height = driver.execute_script("return document.body.scrollHeight")

        while len(tweets) < num_tweets:

            tweet_elements = driver.find_elements(By.XPATH, '//div[@data-testid="tweetText"]')

            for tweet in tweet_elements:
                tweet_text = tweet.text
                if tweet_text not in tweets:
                    tweets.append(tweet_text)
                    if len(tweets) >= num_tweets:
                        break
            
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            #CHANGE THIS TO 10, 100 IF DETECTING BOT
            time.sleep(2)

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        return tweets

    finally:
        driver.quit()

if __name__ == "__main__":
    stock_ticker = input("Enter stock ticker (e.g., $AAPL): ")
    tweets = get_tweets(stock_ticker)
    for i, tweet in enumerate(tweets, 1):
        print(f"{i}. {tweet}")
