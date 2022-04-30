from dependencies import *
from pydantic import AnyUrl
from io import BytesIO


def get_screenshot(site_url: AnyUrl) -> BytesIO:
    try:
        filename = BytesIO()

        driver = get_driver()

        driver.get(site_url)

        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.TAG_NAME, "body"))
        )

        # TODO: For infinite loaders
        # --------------------------
        # for i in range(100):
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     time.sleep(5)

        scrollWidth = driver.execute_script(
            "return document.body.parentNode.scrollWidth"
        )
        scrollHeight = driver.execute_script(
            "return document.body.parentNode.scrollHeight"
        )
        driver.set_window_size(scrollWidth, min(10_000, scrollHeight))
        filename = driver.find_element_by_tag_name("body").screenshot_as_png
    except Exception as e:
        driver.quit()
        print(e)
        return False
    else:
        driver.quit()
        return filename
