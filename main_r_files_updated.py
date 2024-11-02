import instaloader
import pandas as pd
import re
from dotenv import load_dotenv
import os
import time  # Add this at the beginning of your script

# Function to log into Instagram and save the session
def login_instagram(username, password):
    loader = instaloader.Instaloader()
    # Load an existing session or log in if none exists
    try:
        loader.load_session_from_file(username)
        print("Loaded session from file.")
    except FileNotFoundError:
        loader.login(username, password)
        loader.save_session_to_file()
        print("Logged in and session saved.")
    return loader

# Function to extract the shortcode (unique ID) from an Instagram link
def extract_shortcode(link):
    match = re.search(r'/(p|reel)/([^/]+)/', link)
    return match.group(2) if match else None

# Function to get comments from a post given its shortcode
def get_comments_from_post(loader, shortcode):
    comments = []
    post = instaloader.Post.from_shortcode(loader.context, shortcode)
    for comment in post.get_comments():
        comments.append({
            'username': comment.owner.username,
            'text': comment.text,
            'date': comment.created_at_utc
        })
    return comments

# Function to save comments to a CSV file
def save_comments_to_csv(comments, shortcode):
    comments_df = pd.DataFrame(comments)
    filename = f"{shortcode}_comments.csv"
    comments_df.to_csv(filename, index=False)
    print(f"Comments saved to {filename}")

# Main function to handle the entire process
def main():
    # Load environment variables from .env file
    load_dotenv()

    # Fetch credentials from environment variables
    username = os.getenv('INSTA_USERNAME')
    password = os.getenv('INSTA_PASSWORD')

    # Check if username and password are available
    if not username or not password:
        print("Instagram username or password not found in environment variables.")
        return

    # Log in to Instagram with session handling
    loader = login_instagram(username, password)
    
    # Load the CSV file containing Instagram post links with semicolon as the delimiter
    csv_file = 'AUDI_PROCESSADO.csv'  # Replace with your CSV file path
    df = pd.read_csv(csv_file, delimiter=';')
    
    # Loop through each link in the CSV
    for link in df['LINK_PUBLICACAO']:  # Assuming 'LINK_PUBLICACAO' is the column name in your CSV
        # Get the shortcode from the link
        shortcode = extract_shortcode(link)
        
        # Get comments for the post with this shortcode
        comments = get_comments_from_post(loader, shortcode)
        
        # Save the comments to a CSV file named after the shortcode
        save_comments_to_csv(comments, shortcode)

        time.sleep(2)  # Wait 2 seconds before processing the next post

    print("Scraping completed!")

# Run the main function
if __name__ == "__main__":
    main()
