def get_data(id):
    import time, random, os

    from selenium.webdriver import Chrome
    from selenium.webdriver import ChromeOptions

    from selenium.webdriver.common.keys import Keys
    from selenium.common.exceptions import ElementClickInterceptedException
    from selenium.common.exceptions import NoSuchElementException
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("log-level=2")

    driver = Chrome(executable_path=r"C:\Users\Sergey\Desktop\New folder\chromedriver_win32\chromedriver.exe", chrome_options=chrome_options)

    url = f"https://flightaware.com/live/flight/{id}"
    driver.get(url)

    try:
        aircraft_type_xpath = r"/html/body/div[1]/div[1]/div[2]/div[4]/div[9]/div[1]/div/div[1]/div[2]"
        aircraft_type = driver.find_element_by_xpath(aircraft_type_xpath).text

        airline_xpath = r'//*[@id="mainBody"]/div[1]/div[2]/div[4]/div[9]/div[2]/div/div/div[2]/a'
        airline = driver.find_element_by_xpath(airline_xpath).text

        # photos_xpath = r'//*[@id="mainBody"]/div[1]/div[2]/div[4]/div[9]/div[4]/div/span/a'
        # driver.find_element_by_xpath(photos_xpath).click()

        carouselImages = driver.find_elements_by_class_name("carouselImage")

        image_urls = []
        for i in carouselImages:
            image_urls.append(i.get_attribute("src"))
    except:
        return False

    driver.close()

    exceptions = ["Upgrade account to see tail number", "Are you the operator? Purchase FlightAware Global to see tail number and more."]
    if aircraft_type in exceptions:
        aircraft_type = ""
    
    data = {
        "aircraft_type": aircraft_type,
        "airline": airline,
        "image_urls": image_urls
    }

    return data

import flask
from flask import request, jsonify, abort

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route("/api/v1/data", methods=["GET"])
def data():
    if "id" in request.args:
        id = request.args["id"]
    else:
        abort(410)
    
    d = get_data(id)
    if d == False:
        abort(404)
    else:
        return jsonify(d)

app.run()
