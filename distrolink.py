import os
import re
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# URL to DistroKid's official form for profile linking
URL = "https://docs.google.com/forms/d/e/1FAIpQLSe9C_btqqUr9zQoQEwH525_z2ZAQazP5wU4ysTCyNo0KXmu9g/viewform"

# XPATHs associated with the google form
ARTIST = "//*[@id='mG61Hd']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input"
ISRC = "//*[@id='mG61Hd']/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input"
INSTAGRAM = "//*[@id='mG61Hd']/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input"
EMAILADDRESS = "//*[@id='mG61Hd']/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div/div[1]/input"
SUBMIT = "//*[@id='mG61Hd']/div[2]/div/div[3]/div[1]/div[1]/div/span/span"
REPEAT = "//a[text()='Submit another response']"

def main():
    isrc_codes = []
    correct = False

    print("\n>>> NOTICE: Please ensure you have a high-speed internet connection <<<\n")

    while not correct:
        print("Please input...")

        artist = input("Artist Name (associated with the ISRC): ") 

        instagram = input("Instagram Handle: ")
        while not re.match("@[A-Za-z0-9_.]+", instagram):
            instagram = input("\n> Error with Instagram Handle <\nPlease enter an '@' followed by your username: ")

        email = input("Email Address (associated with DistroKid account): ")
        while not re.match("[A-Za-z0-9]+@[A-Za-z0-9]+[.][a-z]{3}", email):
            email = input("\n> Error with email <\nPlease check to make sure your email was entered correctly, then re-enter: ")

        print("\nPlease confirm your information is correct before the script runs:")
        print("\tArtist Name (associated with the ISRC): " + artist)
        print("\tInstagram Handle: " + instagram)
        print("\tEmail Address (associated with DistroKid account): " + email + "\n")

        response = input("Is your information correct as displayed above? [y] / [n]: ")    
        while not re.match("y|n|Y|N", response):
            response = input("Please enter a valid response [y] / [n]: ")

        if response == "y" or response == "Y":
            print("Filling form...")
            correct = True
        else:
            print("Restarting form entry...")    

    service = Service(os.path.abspath("chromedriver.exe"))

    chrome_options = webdriver.ChromeOptions()                                              # Initialize Chromedriver options         
    chrome_options.add_argument('--headless')                                               # No GUI
    chrome_options.add_argument("--log-level=3")                                            # Cleaner console log
    chrome_options.add_argument("disable-infobars")                                         # Masking automation
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')            # Masking automation
    chrome_options.add_experimental_option('useAutomationExtension', False)                 # Masking automation
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])        # Masking automation
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])           # Masking automation
    chrome_options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])   # Masking automation
    
    # Read ISRC codes
    with open("isrc.txt", "r+") as file:
        lines = file.readlines()
        for line in lines:
            isrc_codes.append(line)
        file.truncate(0)

    web = webdriver.Chrome(service=service, options=chrome_options)
    web.get(URL) 
    time.sleep(random.randint(2,7))  

    for isrc in isrc_codes:
        web.find_element(By.XPATH, ARTIST).send_keys(artist)
        time.sleep(random.randint(2,7)) 

        web.find_element(By.XPATH, ISRC).send_keys(isrc)
        time.sleep(random.randint(2,7)) 

        web.find_element(By.XPATH, INSTAGRAM).send_keys(instagram)
        time.sleep(random.randint(2,7))

        web.find_element(By.XPATH, EMAILADDRESS).send_keys(email)
        time.sleep(random.randint(2,7)) 

        web.find_element(By.XPATH, SUBMIT).click()
        time.sleep(random.randint(5,12))

        print("Succesfully submitted request for ISRC " + isrc)

        web.find_element(By.XPATH, REPEAT).click()
        time.sleep(random.randint(5,12))

    print("Succesfully submitted requests for " + str(len(isrc_codes)) + " songs. Exiting...")
    web.quit()

if __name__ == "__main__":
    main()    