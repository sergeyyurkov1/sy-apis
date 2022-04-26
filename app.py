from typing import Union, List

import os
API_KEY = os.environ["API_KEY"]
API_KEY_NAME = "Authorization"

def get_driver():
    import os

    from selenium.webdriver import Chrome
    from selenium.webdriver import ChromeOptions

    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("log-level=2")

    # Heroku bits
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    driver = Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    return driver


def get_data(id: str) -> Union[dict, bool]:
    """Gets aircraft_type, airline, and image_urls from a flight ID"""
    
    driver = get_driver()

    url = f"https://flightaware.com/live/flight/{id}"

    driver.get(url)

    try:
        aircraft_type_xpath = r'//*[@id="mainBody"]/div[1]/div[2]/div[4]/div[9]/div[1]/div/div[1]/div[2]'
        aircraft_type = driver.find_element_by_xpath(aircraft_type_xpath).text

        airline_xpath = r'//*[@id="mainBody"]/div[1]/div[2]/div[4]/div[9]/div[2]/div/div/div[2]/a'
        airline = driver.find_element_by_xpath(airline_xpath).text

        # photos_xpath = r'//*[@id="mainBody"]/div[1]/div[2]/div[4]/div[9]/div[4]/div/span/a'
        # driver.find_element_by_xpath(photos_xpath).click()

        carouselImages = driver.find_elements_by_class_name("carouselImage")

        image_urls = []
        for i in carouselImages:
            image_urls.append(i.get_attribute("src"))
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(e)

        return False

    driver.close()

    exceptions = ["Upgrade account to see tail number", "Are you the operator? Purchase FlightAware Global to see tail number and more."]
    if aircraft_type in exceptions:
        aircraft_type = ""
    
    return {
        "aircraft_type": aircraft_type,
        "airline": airline,
        "image_urls": image_urls
    }


from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader, APIKey
from pydantic import BaseModel

app = FastAPI()

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(status_code=403)

class Data(BaseModel):
    aircraft_type: str
    airline: str
    image_urls: List[str]

@app.get("/adsb/v1/flight/{id}", response_model=Data)
def data(id: str, api_key: APIKey = Depends(get_api_key)):
    # if id == "":
    #     raise HTTPException(status_code=400)
    
    data = get_data(id)
    if data == False:
        raise HTTPException(status_code=404)
    else:
        return data