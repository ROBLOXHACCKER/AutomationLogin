import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv, dotenv_values
import logging

# conf - log records
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# env var declaring
load_dotenv()
config = dotenv_values(".env")

# varUsers .env
EMAIL = config.get('EMAIL')
PASSWORD = config.get('PASSWORD')
#var site .env
ID_USERNAME = config.get('ID_USERNAME')
ID_PASSWORD = config.get('ID_PASSWORD')
CL_BTN_CONTINUE = config.get('CL_BTN_CONTINUE')
CL_BTN_LOGIN = config.get('CL_BTN_LOGIN')
CL_WELLHUBAGE = config.get('CL_WELLHUBAGE')
SITE_URL = "https://account.com/"

EMAILS = EMAIL.split(',')
PASSWORDS = PASSWORD.split(',')

if len(EMAILS) == len(PASSWORDS):
    logging.info("CREDENTIALS: OK")
else:
    logging.error(f"CREDENTIALS ERR: email count [{len(EMAILS)}] password count [{len(PASSWORDS)}]")


# Chrome setup
def setup_driver():
    logging.info("setup chrome...")
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    return driver


# fun log-in
def login_to_site(driver, email, password):
    try:
        logging.info(f"searching for site: {SITE_URL}")
        driver.get(SITE_URL)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, ID_USERNAME))
        )
        username_field = driver.find_element(By.ID, ID_USERNAME)
        username_field.send_keys(email)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, CL_BTN_CONTINUE))
        )
        continue_button = driver.find_element(By.CLASS_NAME, CL_BTN_CONTINUE)
        continue_button.click()
        # captcha wait
        WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.ID, ID_PASSWORD))
        )
        password_field = driver.find_element(By.ID, ID_PASSWORD)
        password_field.send_keys(password)
        #captcha wait
        WebDriverWait(driver, 50).until(
            EC.element_to_be_clickable((By.CLASS_NAME, CL_BTN_LOGIN))
        )
        login_button = driver.find_element(By.CLASS_NAME, CL_BTN_LOGIN)
        login_button.click()
        #check for an element of the user page after login
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, CL_WELLHUBAGE))
        )
        logging.info("Wellhubage element found, saving credentials to login_records.txt.")
        return True

    except Exception as e:
        logging.error(f"Login error: {str(e)}")
        return False


def main():
    for i in range(len(EMAILS)):
        email = EMAILS[i]
        password = PASSWORDS[i]
        driver = setup_driver()  # CREATE NEW DRIVER EACH SESSION FOR SAFE

        try:
            credential_ok = login_to_site(driver, email, password)

            if credential_ok:
                logging.info("Saving EMAIL and PASSWORD to file...")
                with open("login_records.txt", "a") as file:
                    file.write(f"EMAIL: {email}, PASSWORD: {password}\n")
            else:
                logging.info("Saving EMAIL and PASSWORD to failed credentials file...")
                with open("loginfailed.txt", "a") as file:
                    file.write(f"EMAIL: {email}, PASSWORD: {password}\n")
                logging.info("Credentials saved in loginfailed.txt.")

        finally:
            logging.info("Driver Closing...")

    logging.info("All credentials have been processed.")


if __name__ == "__main__":
    main()
