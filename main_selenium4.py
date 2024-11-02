import pandas as pd
import re
from dotenv import load_dotenv
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

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



    # Locate all comment items
    comment_items = driver.find_elements(By.XPATH, "//li[contains(@class, '_a9zj') or contains(@class, '_a9zl') or contains(@class, '_a9z5')]")


    for item in comment_items:
        try:
            # Use XPath to locate username and comment text
            username = item.find_element(By.XPATH, "//a[contains(@class, 'x1i10hfl') or contains(@class, 'xjqpnuy') or contains(@class, 'xa49m3k') or contains(@class, 'xqeqjp1') or contains(@class, 'x2hbi6w') or contains(@class, 'xdl72j9') or contains(@class, 'x2lah0s') or contains(@class, 'xe8uvvx') or contains(@class, 'xdj266r') or contains(@class, 'x11i5rnm') or contains(@class, 'xat24cr') or contains(@class, 'x1mh8g0r') or contains(@class, 'x2lwn1j') or contains(@class, 'xeuugli') or contains(@class, 'x1hl2dhg') or contains(@class, 'xggy1nq') or contains(@class, 'x1ja2u2z') or contains(@class, 'x1t137rt') or contains(@class, 'x1q0g3np') or contains(@class, 'x1lku1pv') or contains(@class, 'x1a2a7pz') or contains(@class, 'x6s0dn4') or contains(@class, 'xjyslct') or contains(@class, 'x1ejq31n') or contains(@class, 'xd10rxx') or contains(@class, 'x1sy0etr') or contains(@class, 'x17r0tee') or contains(@class, 'x9f619') or contains(@class, 'x1ypdohk') or contains(@class, 'x1f6kntn') or contains(@class, 'xwhw2v2') or contains(@class, 'xl56j7k') or contains(@class, 'x17ydfre') or contains(@class, 'x2b8uid') or contains(@class, 'xlyipyv') or contains(@class, 'x87ps6o') or contains(@class, 'x14atkfc') or contains(@class, 'xcdnw81') or contains(@class, 'x1i0vuye') or contains(@class, 'xjbqb8w') or contains(@class, 'xm3z3ea') or contains(@class, 'x1x8b98j') or contains(@class, 'x131883w') or contains(@class, 'x16mih1h') or contains(@class, 'x972fbf') or contains(@class, 'xcfux6l') or contains(@class, 'x1qhh985') or contains(@class, 'xm0m39n') or contains(@class, 'xt0psk2') or contains(@class, 'xt7dq6l') or contains(@class, 'xexx8yu') or contains(@class, 'x4uap5') or contains(@class, 'x18d9i69') or contains(@class, 'xkhd6sd') or contains(@class, 'x1n2onr6') or contains(@class, 'x1n5bzlp') or contains(@class, 'xqnirrm') or contains(@class, 'xj34u2y') or contains(@class, 'x568u83')]").text
            comment_text = item.find_element(By.XPATH, ".//span").text

            comments.append({
                'username': username,
                'text': comment_text
            })
        except Exception as e:
            continue  # Skip if any element is not found

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
        print(shortcode)
        
        # Get comments for the post with this link
        comments = get_comments_from_post(driver, link)
        print(comments)
        
        # Save the comments to a CSV file named after the shortcode
        save_comments_to_csv(comments, shortcode)
        
        time.sleep(2)  # Wait 2 seconds before processing the next post

    driver.quit()
    print("Scraping completed!")

# Run the main function
if __name__ == "__main__":
    main()