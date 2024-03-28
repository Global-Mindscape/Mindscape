import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Define the URL of the WHO Mental Health Atlas page
url = 'https://www.who.int/teams/mental-health-and-substance-use/data-research/mental-health-atlas'

print(f"Fetching content from {url}...")
# Send a GET request to fetch the webpage content
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    print("Successfully fetched the webpage content!") 
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    print("Searching for the specific content block using CSS selector...")
    # Find the specific content block based on the provided CSS selector
    content_block = soup.select("#PageContent_C041_Col01 > div:nth-child(5)")
    
    # Initialize a list to store the extracted links
    extracted_links = []
    
    # Check if the content block was found
    if content_block:
        print("Content block found! Searching for links...")
        
        # Find all anchor tags within the content block
        links = content_block[0].find_all('a')
        
        # Loop through each link to extract and store the URLs
        for link in links:
            href = link.get('href', '')
            
            # Check if the link follows the specified structure
            if href.startswith('https://www.who.int/publications/m/item/'):
                extracted_links.append(href)
        
        print(f"Found {len(extracted_links)} links that match the specified structure.")
        
        # Print the extracted links
        print("Extracted links:")
        for idx, link in enumerate(extracted_links, 1):
            print(f"{idx}. {link}")
            
    else:
        print("Content block not found. Please check the provided CSS selector.")
        
else:
    print(f"Failed to fetch the webpage. Status code: {response.status_code}")

# Create a directory to save PDFs
os.makedirs('pdf_files', exist_ok=True)

# Initialize the Selenium webdriver with the correct executable path
driver_path = '/opt/homebrew/bin/chromedriver'  # Update with your chromedriver path

# Initialize the Selenium webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"executable_path={driver_path}")  # Specify the path to the Chrome driver

# Initialize the Selenium webdriver
driver = webdriver.Chrome(options=chrome_options)

# Debugging print to verify the type of the driver object
print(f"Type of driver: {type(driver)}")

for idx, link in enumerate(extracted_links, 1):
    print(f"Processing link {idx}/{len(extracted_links)}: {link}")
    
    # Navigate to the link
    driver.get(link)
    
    time.sleep(5)  # Wait for the page to load
    
    try:
        # Wait for the download link to become available
        download_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Download")]'))
        )
        
        # Fetch the PDF URL
        pdf_url = download_link.get_attribute('href')
        
        # Download the PDF using requests
        response = requests.get(pdf_url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Save the PDF to the pdf_files folder
            pdf_path = f'pdf_files/{os.path.basename(pdf_url.split("?")[0])}'
            with open(pdf_path, 'wb') as f:
                f.write(response.content)
            
            print(f"Downloaded PDF saved to {pdf_path}")
        else:
            print(f"Failed to download PDF: {response.status_code}")
        
    except Exception as e:
        print(f"Error downloading PDF: {e}")

# Close the webdriver
driver.quit()

print("All PDFs downloaded successfully!")
