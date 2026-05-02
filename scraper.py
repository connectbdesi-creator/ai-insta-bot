import os
import requests
from bs4 import BeautifulSoup
import urllib.parse
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap
from groq import Groq

# 1. Setup the Writer (Groq)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

URL = "https://connectbdesi-creator.github.io/ai-signal-brief/"

def get_viral_hook(headline):
    print(f"Original news: {headline}")
    prompt = f"Rewrite this AI news into a viral Instagram 'Hook' under 60 characters. Use 1 emoji. BE LOUD! Headline: {headline}"
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    hook = completion.choices[0].message.content
    return hook.replace('"', '') # Remove quotes

def make_magic():
    print("--- STARTING ROBOT ---")
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    update = soup.find(['h2', 'h3'])
    
    if update:
        raw_headline = update.text.strip()
        viral_headline = get_viral_hook(raw_headline).upper()
        print(f"Generated Hook: {viral_headline}")
        
        # Get the AI image
        encoded_prompt = urllib.parse.quote(f"Futuristic technology, neon, cinematic, {raw_headline}")
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1350&nologo=true"
        
        print("Downloading background image...")
        img_res = requests.get(image_url)
        img = Image.open(io.BytesIO(img_res.content))
        draw = ImageDraw.Draw(img)
        
        # --- THE DESIGNER PART ---
        print("Drawing text layers...")
        
        # Load Font (with backup)
        try:
            font_url = "https://github.com/google/fonts/raw/main/ofl/anton/Anton-Regular.ttf"
            font_res = requests.get(font_url)
            font = ImageFont.truetype(io.BytesIO(font_res.content), 70)
            print("Fancy font loaded!")
        except:
            font = ImageFont.load_default()
            print("Using backup font.")

        # Wrap text so it fits in the box
        lines = textwrap.wrap(viral_headline, width=20) 
        
        # Draw Box (Yellow with Black Shadow)
        # Position: Bottom of the image
        draw.rectangle([40, 990, 1040, 1310], fill="black") # Shadow
        draw.rectangle([50, 1000, 1030, 1300], fill="yellow", outline="black", width=10)
        
        # Draw each line of text
        y_text = 1030
        for line in lines:
            draw.text((100, y_text), line, fill="black", font=font)
            y_text += 80 # Move down for next line
        
        img.save('latest_news_post.jpg')
        print("--- SUCCESS: POST CREATED ---")
    else:
        print("No news found on the site!")

if __name__ == "__main__":
    make_magic()