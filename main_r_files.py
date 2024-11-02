import instaloader
import pandas as pd
import re
from dotenv import load_dotenv
import os

# Function to log into Instagram
def login_instagram(username, password):
    loader = instaloader.Instaloader()
    loader.login(username, password)
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

    # Initialize Instaloader
    loader = instaloader.Instaloader()

    # Fetch credentials from environment variables
    username = os.getenv('INSTA_USERNAME')
    password = os.getenv('INSTA_PASSWORD')

    #print(f"Username: {username}, Password: {password}")

    # Log in with environment variables
    loader.login(username, password)
    
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

    print("Scraping completed!")

# Run the main function
if __name__ == "__main__":
    main()
