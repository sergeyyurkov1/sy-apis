from dependencies import *
from typing import (
    Union,
    List,
)
from pydantic import (
    BaseModel,
    validator,
)
from fastapi import (
    Path,
)


# class Flight(BaseModel):
#     id: str = Path(...)

#     @validator("id")
#     def validate(cls, val):
#         if not 2 <= len(val) <= 6:
#             raise HTTPException(
#                 status_code=400, detail="ensure this value is 2 - 6 characters long"
#             )
#             # raise ValueError("ensure this value is 2 - 6 characters long")
#         return val


class Data(BaseModel):
    aircraft_type: str
    airline: str
    image_urls: List[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "aircraft_type": "Boeing 747-400 (quad-jet)",
                "airline": "Kalitta Air",
                "image_urls": [
                    "https://photos-e1.flightcdn.com/photos/retriever/ec4904492dfe68b511fd60256009fe486f90de9c",
                ],
            }
        }


class Flight:
    def __init__(
        self,
        flight: str = Path(..., description="2 - 6 char. flight ID", example="CKS852"),
    ):
        self.id = flight
        if not 2 <= len(self.id) <= 6:
            raise HTTPException(
                status_code=422,
                detail=f"flight_id: ensure this value is 2 - 6 characters long",
            )


def get_data(id: str) -> Union[dict, bool]:
    """Gets `aircraft_type`, `airline`, and `image_urls` from a flight ID"""

    try:
        driver = get_driver()

        url = f"https://flightaware.com/live/flight/{id}"

        driver.get(url)

        aircraft_type_xpath = r'//*[@id="mainBody"]/div[1]/div[1]/div[2]/div[4]/div[9]/div[1]/div/div[1]/div[2]'
        aircraft_type = driver.find_element_by_xpath(aircraft_type_xpath).text

        airline_xpath = r'//*[@id="mainBody"]/div[1]/div[1]/div[2]/div[4]/div[9]/div[2]/div/div/div[2]/a'
        airline = driver.find_element_by_xpath(airline_xpath).text

        # photos_xpath = r'//*[@id="mainBody"]/div[1]/div[2]/div[4]/div[9]/div[4]/div/span/a'
        # driver.find_element_by_xpath(photos_xpath).click()

        carouselImages = driver.find_elements_by_class_name("carouselImage")

        image_urls = []
        for i in carouselImages:
            image_urls.append(i.get_attribute("src"))

        driver.close()

        exceptions = [
            "Upgrade account to see tail number",
            "Are you the operator? Purchase FlightAware Global to see tail number and more.",
        ]
        if aircraft_type in exceptions:
            aircraft_type = ""

        return {
            "aircraft_type": aircraft_type,
            "airline": airline,
            "image_urls": image_urls,
        }

    except Exception as e:
        import traceback

        traceback.print_exc()
        print(e)

        driver.close()

        return False


def get_data_requests(id: str, full: bool = False) -> Union[dict, bool]:
    """
    Gets `aircraft_type`, `airline`, and `image_urls` from a flight ID
    Uses `requests` library instead of `selenium`
    """

    try:
        import requests

        url = f"https://flightaware.com/live/flight/{id}"

        # driver = get_driver()
        # driver.get(url)
        # page_source = driver.page_source

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
        }
        page_source = requests.get(url, headers=headers).text

        import re

        scripts = re.findall(r"<script>(.*)</script>", page_source)

        script = scripts[-1].strip(";").removeprefix("var trackpollBootstrap = ")

        import json

        data = json.loads(script)

        if full == False:
            data = data["flights"][next(iter(data["flights"]))]

            aircraft_type = data["aircraft"]["friendlyType"]
            airline = data["airline"]["shortName"]
            image_urls = [i["thumbnail"] for i in data["relatedThumbnails"]]

            return {
                "aircraft_type": aircraft_type,
                "airline": airline,
                "image_urls": image_urls,
            }
        else:
            return data

    except Exception as e:
        import traceback

        traceback.print_exc()
        print(e)

        return False
