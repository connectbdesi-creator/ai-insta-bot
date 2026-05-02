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
    prompt = f"Rewrite this AI news into a viral Instagram 'Hook' under 40 characters. Use 1 emoji. Be punchy! Headline: {headline}"
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
        viral_headline = get_viral_hook(raw_headline).upper()
        print(f"Viral Hook: {viral_headline}")
        
        # Get the AI image
        encoded_prompt = urllib.parse.quote(f"Futuristic technology, {viral_headline}, highly detailed, 4k")
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1350&nologo=true"
        
        img_res = requests.get(image_url)
        img = Image.open(io.BytesIO(img_res.content))
        draw = ImageDraw.Draw(img)
        
        # --- THE FONT FIX ---
        # We download a bold font so it's guaranteed to work on GitHub
        font_url = "https://github.com/google/fonts/raw/main/ofl/anton/Anton-Regular.ttf"
        font_res = requests.get(font_url)
        font = ImageFont.truetype(io.BytesIO(font_res.content), 80) # Size 80 is HUGE!
        
        # 1. Draw a Shadow/Border for the box (to make it pop)
        draw.rectangle([45, 1045, 1035, 1255], fill="black") # Black shadow
        draw.rectangle([50, 1050, 1030, 1250], fill="yellow", outline="black", width=10)
        
        # 2. Draw the Text in the center of the box
        # We use a simple way to center it
        draw.text((100, 1110), viral_headline, fill="black", font=font)
        
        img.save('latest_news_post.jpg')
        print("Success! Viral post with BIG TEXT created.")
    else:
        print("No news found!")

if __name__ == "__main__":
    make_magic()