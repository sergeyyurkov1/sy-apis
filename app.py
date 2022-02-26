def get_data(id):
    import time, random, os

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
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(e)

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

if __name__ == "__main__":
    app.run()
