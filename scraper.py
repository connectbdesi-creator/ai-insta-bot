import os
import requests
from bs4 import BeautifulSoup
import urllib.parse
from PIL import Image, ImageDraw, ImageFont
import io
from groq import Groq

# 1. Setup the Writer (Groq)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

URL = "https://connectbdesi-creator.github.io/ai-signal-brief/"

def get_viral_hook(headline):
    # This tells the AI to be a viral genius
    prompt = f"Rewrite this AI news headline into a viral, catchy Instagram 'Hook' under 50 characters. Use 1 emoji. Headline: {headline}"
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

def make_magic():
    print("Checking for news...")
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    update = soup.find(['h2', 'h3'])
    
    if update:
        raw_headline = update.text.strip()
        
        # 2. Get the viral version!
        viral_headline = get_viral_hook(raw_headline)
        print(f"Viral Hook: {viral_headline}")
        
        # 3. Create Image based on viral hook
        encoded_prompt = urllib.parse.quote(f"Futuristic tech, {viral_headline}, cinematic")
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1350&nologo=true"
        
        img_res = requests.get(image_url)
        img = Image.open(io.BytesIO(img_res.content))
        draw = ImageDraw.Draw(img)
        
        # 4. Draw the Box and the Viral Hook
        draw.rectangle([50, 1050, 1030, 1250], fill="yellow", outline="black", width=8)
        draw.text((80, 1100), viral_headline.upper(), fill="black")
        
        img.save('latest_news_post.jpg')
        print("Success! Viral post created.")

if __name__ == "__main__":
    make_magic()