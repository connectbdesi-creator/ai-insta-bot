import requests
from bs4 import BeautifulSoup

# This tells the robot where to look
URL = "https://connectbdesi-creator.github.io/ai-signal-brief/"

def check_for_news():
    print("Robot is waking up to check the news...")
    response = requests.get(URL)
    
    # The robot 'reads' the page here
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # We look for the main updates (assuming they are in 'h2' or 'p' tags)
    updates = soup.find_all(['h2', 'h3']) 
    
    if updates:
        latest_news = updates[0].text.strip()
        print(f"I found something new! It says: {latest_news}")
        # Later, we will send this to the Image Creator
    else:
        print("Nothing new right now. I'll check again later!")

if __name__ == "__main__":
    check_for_news()