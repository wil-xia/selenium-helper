#
# THIS CODE WAS WRITTEN IN 2023 AND IS LIKELY DEPRECATED
#



from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

#Typical positive/negative stock terms
positive_words = 'buy bull long support undervalued underpriced cheap upward rising trend moon rocket hold breakout call beat support buying holding high profit'
negative_words = 'sell bear bubble bearish short overvalued overbought overpriced expensive downward falling sold sell low put miss resistance squeeze cover seller'

dictOfpos = {i: 4 for i in positive_words.split(" ")}
dictOfneg = {i: -4 for i in negative_words.split(" ")}
Financial_Lexicon = {**dictOfpos, **dictOfneg}

sia.lexicon.update(Financial_Lexicon)

def get_tweets(stock_ticker, num_tweets=100):
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

            #INCREASE TO 10, 100 IF BOT DETECTED
            time.sleep(2)

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        return tweets

    finally:
        driver.quit()

def analyze_sentiment(tweets):
    sentiments = []
    for tweet in tweets:
        sentiment = sia.polarity_scores(tweet)
        sentiments.append(sentiment['compound'])  
        print(f"Tweet: {tweet}\nSentiment Score: {sentiment['compound']:.2f}\n")
    
    return sentiments

if __name__ == "__main__":
    stock_ticker = input("Enter stock ticker (e.g., $AAPL): ")
    tweets = get_tweets(stock_ticker)

    if tweets:
        print(f"\n--- Retrieved {len(tweets)} tweets for {stock_ticker} ---\n")
        sentiment_scores = analyze_sentiment(tweets)


        import matplotlib.pyplot as plt
        import seaborn as sns

        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.histplot(sentiment_scores, bins=20, kde=True, color="blue")
        plt.title(f"Sentiment Analysis of {stock_ticker} Tweets")
        plt.xlabel("Sentiment Score (Compound)")
        plt.ylabel("Frequency")
        plt.show()
    else:
        print("No tweets found.")
