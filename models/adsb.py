from dependencies import *
from typing import Union, List
from pydantic import (
    BaseModel,
    # validator,
    # ValidationError
)


class Data(BaseModel):
    aircraft_type: str
    airline: str
    image_urls: List[str]

# class Id(BaseModel):
#     id: str = Path(...)

#     @validator("id")
#     def validate(cls, val):
#         if <>:
#             # raise HTTPException(status_code=400)
#             raise ValidationError
#         return val


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