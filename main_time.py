import os
import instaloader
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

# Initialize Instaloader
loader = instaloader.Instaloader()

# Fetch credentials from environment variables
username = os.getenv('INSTA_USERNAME')
password = os.getenv('INSTA_PASSWORD')

# Log in with environment variables
loader.login(username, password)

# Define the post shortcode
post_shortcode = 'C-qlwTWRdJJ'  # Replace with the Instagram post shortcode

# Start the timer just before scraping
scraping_start_time = time.time()

# Load the post and scrape comments
post = instaloader.Post.from_shortcode(loader.context, post_shortcode)
comments = []
for comment in post.get_comments():
    comments.append({
        'text': comment.text,
        'username': comment.owner.username,
        'date': comment.created_at_utc
    })

# End the timer after scraping
scraping_end_time = time.time()
scraping_elapsed_time = scraping_end_time - scraping_start_time

# Display the comments
for comment in comments:
    print(f"Username: {comment['username']}, Comment: {comment['text']}, Date: {comment['date']}")

# Print the scraping time
print(f"\nScraping Time: {scraping_elapsed_time:.2f} seconds")
