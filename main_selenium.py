import pandas as pd
import re
from dotenv import load_dotenv
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Function to set up Selenium WebDriver
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Function to log into Instagram using Selenium
def login_instagram(driver, username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(3)  # Wait for the page to load
    
    # Enter username and password
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
    
    # Wait for the home page to load after login
    time.sleep(5)

# Function to extract the shortcode (unique ID) from an Instagram link
def extract_shortcode(link):
    match = re.search(r'/(p|reel)/([^/]+)/', link)
    return match.group(2) if match else None

# Function to get comments from a post given its shortcode
def get_comments_from_post(driver, link):
    driver.get(link)
    time.sleep(3)  # Wait for the post page to load
    
    comments = []
    # Scroll to load more comments if they exist
    while True:
        try:
            load_more_comments = driver.find_element(By.XPATH, "//button[contains(text(), 'Load more comments')]")
            load_more_comments.click()
            time.sleep(2)  # Wait for comments to load
        except:
            break  # No more "Load more comments" button found
    
    # Collect all comments
    comment_elements = driver.find_elements(By.XPATH, "//ul[@class='Mr508']/div/li/div/div/div/span")
    for elem in comment_elements:
        comments.append({
            'text': elem.text,
            'username': elem.find_element(By.XPATH, "./../../../../../*[@class='_6lAjh']").text
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

    # Set up Selenium WebDriver and log in to Instagram
    driver = setup_driver()
    login_instagram(driver, username, password)
    
    # Load the CSV file containing Instagram post links with semicolon as the delimiter
    csv_file = 'AUDI_PROCESSADO.csv'  # Replace with your CSV file path
    df = pd.read_csv(csv_file, delimiter=';')
    
    # Loop through each link in the CSV
    for link in df['LINK_PUBLICACAO']:  # Assuming 'LINK_PUBLICACAO' is the column name in your CSV
        # Get the shortcode from the link
        shortcode = extract_shortcode(link)
        
        # Get comments for the post with this link
        comments = get_comments_from_post(driver, link)
        
        # Save the comments to a CSV file named after the shortcode
        save_comments_to_csv(comments, shortcode)
        
        time.sleep(2)  # Wait 2 seconds before processing the next post

    driver.quit()
    print("Scraping completed!")

# Run the main function
if __name__ == "__main__":
    main()
