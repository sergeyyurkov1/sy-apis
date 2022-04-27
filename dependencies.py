from fastapi.security.api_key import APIKeyHeader
from fastapi import HTTPException, Security
import os

API_KEY = os.environ["API_KEY"]
API_KEY_NAME = "Authorization"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(status_code=403)


def get_driver():
    from selenium.webdriver import Chrome
    from selenium.webdriver import ChromeOptions

    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("log-level=2")

    # Heroku bits
    import sys

    if sys.platform.startswith("linux"):
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    CHROMEDRIVER_PATH = os.environ.get("CHROMEDRIVER_PATH")
    driver = Chrome(
        executable_path=r"{}".format(CHROMEDRIVER_PATH),
        chrome_options=chrome_options,
    )

    return driver
