import requests
from bs4 import BeautifulSoup
import urllib.parse
import os

# 1. Where to look for news
URL = "https://connectbdesi-creator.github.io/ai-signal-brief/"

def make_magic():
    print("Robot is checking the site...")
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Finding the latest headline
    update = soup.find(['h2', 'h3'])
    
    if update:
        headline = update.text.strip()
        print(f"New Update Found: {headline}")
        
        # 2. Creating the "Art Prompt"
        # We tell the AI what to draw based on your headline
        art_prompt = f"Futuristic AI news, {headline}, cinematic lighting, high resolution, neon colors, 3d render"
        encoded_prompt = urllib.parse.quote(art_prompt)
        
        # 3. Generating the Image
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1350&nologo=true"
        print(f"Generating your Instagram image...")
        
        # 4. Saving the image to a folder
        img_data = requests.get(image_url).content
        with open('latest_news_post.jpg', 'wb') as handler:
            handler.write(img_data)
        
        print("Success! Image saved as latest_news_post.jpg")
    else:
        print("No news found yet!")

if __name__ == "__main__":
    make_magic()