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
    #driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome()
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
    #comment_items = driver.find_element(By.CLASS_NAME, '_a9zj _a9zl  _a9z5')
    comment_items = driver.find_element(By.CSS_SELECTOR, 'li._a9zj._a9zl._a9z5')

    
    for item in comment_items:
        try:
            #username = item.find_element(By.CLASS_NAME, 'x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1f6kntn xwhw2v2 xl56j7k x17ydfre x2b8uid xlyipyv x87ps6o x14atkfc xcdnw81 x1i0vuye xjbqb8w xm3z3ea x1x8b98j x131883w x16mih1h x972fbf xcfux6l x1qhh985 xm0m39n xt0psk2 xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x1n5bzlp xqnirrm xj34u2y x568u83')
            username = item.find_element(By.CSS_SELECTOR, 'a.x1i10hfl.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w.xdl72j9.x2lah0s.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x2lwn1j.xeuugli.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1q0g3np.x1lku1pv.x1a2a7pz.x6s0dn4.xjyslct.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x9f619.x1ypdohk.x1f6kntn.xwhw2v2.xl56j7k.x17ydfre.x2b8uid.xlyipyv.x87ps6o.x14atkfc.xcdnw81.x1i0vuye.xjbqb8w.xm3z3ea.x1x8b98j.x131883w.x16mih1h.x972fbf.xcfux6l.x1qhh985.xm0m39n.xt0psk2.xt7dq6l.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.x1n5bzlp.xqnirrm.xj34u2y.x568u83')

            #comment_text = item.find_element(By.CLASS_NAME, '_ap3a _aaco _aacu _aacx _aad7 _aade')
            comment_text = item.find_element(By.CSS_SELECTOR, 'span._ap3a._aaco._aacu._aacx._aad7._aade')

            comments.append({
                'username': username,
                'text': comment_text
            })
        except:
            continue  # Skip if any element is not found

    print(comments)

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
        
        # Save the comments to a CSV file named after the shortcode
        save_comments_to_csv(comments, shortcode)
        
        time.sleep(2)  # Wait 2 seconds before processing the next post

    driver.quit()
    print("Scraping completed!")

# Run the main function
if __name__ == "__main__":
    main()
