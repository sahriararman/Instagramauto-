import os
import instaloader
from instabot import Bot
import schedule
import time
import json

# Load configurations
with open("config.json", "r") as config_file:
    config = json.load(config_file)

USERNAME = config["username"]
PASSWORD = config["password"]
PROFILE = config["target_profile"]
CONTENT_FOLDER = "downloads"

# Function to download content from a public profile
def download_content(profile):
    loader = instaloader.Instaloader(download_videos=True, download_comments=False)
    if not os.path.exists(CONTENT_FOLDER):
        os.makedirs(CONTENT_FOLDER)
    os.chdir(CONTENT_FOLDER)
    loader.download_profile(profile, profile_pic=False, fast_update=True)
    os.chdir("..")
    print(f"Downloaded content from {profile}")

# Function to post the next content
def post_next_content():
    bot = Bot()
    bot.login(username=USERNAME, password=PASSWORD)
    files = sorted(
        [f for f in os.listdir(CONTENT_FOLDER) if f.endswith((".jpg", ".mp4"))]
    )
    if files:
        next_file = os.path.join(CONTENT_FOLDER, files[0])
        caption = "Reposted with permission"  # Customize the caption
        if next_file.endswith(".jpg"):
            bot.upload_photo(next_file, caption=caption)
        elif next_file.endswith(".mp4"):
            bot.upload_video(next_file, caption=caption)
        os.remove(next_file)  # Remove the file after posting
        print(f"Posted: {next_file}")
    else:
        print("No more content to post.")

# Schedule posts
def schedule_posts():
    schedule.every(2).hours.do(post_next_content)
    print("Scheduler is running...")
    while True:
        schedule.run_pending()
        time.sleep(1)

# Main workflow
def main():
    download_content(PROFILE)
    schedule_posts()

if __name__ == "__main__":
    main()