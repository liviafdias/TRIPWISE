
import os
import csv
from dotenv import load_dotenv
import instaloader

# Load environment variables from .env file
load_dotenv()

# Initialize Instaloader
loader = instaloader.Instaloader()

# Fetch credentials from environment variables
username = os.getenv('INSTA_USERNAME')
password = os.getenv('INSTA_PASSWORD')

#print(f"Username: {username}, Password: {password}")

# Log in with environment variables
loader.login(username, password)

# Load the post using the shortcode or post URL
post_shortcode = 'C-qlwTWRdJJ'
post = instaloader.Post.from_shortcode(loader.context, post_shortcode)



# with open('post_data.csv', mode='w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
    
#     # Write header row for easy use with pandas
#     writer.writerow(['username', 'comment'])

#     # Collect and write comments to the CSV file
#     for comment in post.get_comments():
#         writer.writerow([comment.owner.username, comment.text])

# Iterate through comments
comments = []
for comment in post.get_comments():
    comments.append({
        'text': comment.text,
        'username': comment.owner.username,
        'date': comment.created_at_utc
    })

# Display the comments or save them to a file
for comment in comments:
    print(f"Username: {comment['username']}, Comment: {comment['text']}, Date: {comment['date']}")
