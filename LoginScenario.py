from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from helium import *
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import time

username = "username"
password = "password"

default_options = ["--disable-extensions", "--disable-user-media-security=true",
                   "--allow-file-access-from-files", "--use-fake-device-for-media-stream",
                   "--use-fake-ui-for-media-stream", "--disable-popup-blocking",
                   "--disable-infobars", "--enable-usermedia-screen-capturing",
                   "--disable-dev-shm-usage", "--no-sandbox",
                   "--auto-select-desktop-capture-source=Screen 1",
                   "--disable-blink-features=AutomationControlled"]
headless_options = ["--headless", "--use-system-clipboard",
                    "--window-size=1920x1080"]


def browser_options(chrome_type):
    webdriver_options = webdriver.ChromeOptions()
    notification_opt = {"profile.default_content_setting_values.notifications": 1}
    webdriver_options.add_experimental_option("prefs", notification_opt)

    if chrome_type == "headless":
        var = default_options + headless_options
    else:
        var = default_options

    for d_o in var:
        webdriver_options.add_argument(d_o)
        return webdriver_options


def get_webdriver_instance(browser=None):
    base_url = "https://accounts.teachmint.com/"
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "normal"
    # driver = webdriver.Chrome(desired_capabilities=caps,executable_path=driver_path(), chrome_options=browser_options(browser))
    # driver = Chrome(service=ChromeService(ChromeDriverManager().install()),
    #                 options=browser_options(browser))
    driver = webdriver.Chrome(options=browser_options(browser))
    driver.command_executor._commands["send_command"] = ("POST",
                                                         '/session/$sessionId/chromium/send_com,mand')
    driver.maximize_window()
    driver.get(base_url)
    set_driver(driver)
    return driver


def enter_phone_number_otp(driver, creds):
    driver.find_element("xpath", "//input[@type='text']").send_keys(creds[0])
    time.sleep(1)
    print("entered user phone number {}".format(creds[0]))
    driver.find_element("id", "send-otp-btn-id").click()
    WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CSS_SELECTOR, "loader")))
    WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CLASS_NAME, "loader")))
    time.sleep(1)
    _input_otp_field = "//input[@data-group-idx='{}']"

    for i, otp in enumerate(creds[1]):
        otp_field = _input_otp_field.format(str(i))
        write(otp, into=S(otp_field))

    print("entered otp {}".format(creds[1]))
    time.sleep(1)
    driver.find_element("id", "submit-otp-btn-id").click()
    time.sleep(2)

    driver.find_element("xpath", '//img[@alt="arrow"]').click()
    WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CSS_SELECTOR, "loader")))
    WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CLASS_NAME, "loader")))
    time.sleep(1)
    print("successfully entered user phone number and otp")


def navigate_to_certificate(driver):
    element = driver.find_element('xpath', '//a[@class="Sidebar_sidebarLink__39rXm Sidebar_activeGroup__3dvZD"]')
    action_obj = ActionChains(driver)
    action_obj.move_to_element(element).perform()
    # click on certificate
    driver.find_element('xpath', '(//div[@role="presentation"])[6]').click()
    driver.find_element('xpath', '//a[text()="Certificates"]').click()
    return driver


# # to select certificate type
def select_certificate_type(driver):
    driver.find_element('xpath', "//a[text()='Students']").click()
    driver.find_element('xpath', "//h6[text()='School leaving certificate']").click()
    time.sleep(5)
    # click on generate
    driver.find_element('xpath', "//div[text()='Generate']").click()
    return driver


# # to search and select student
def search_and_select_student(driver):
    driver.find_element('xpath', '//input[@name="search"]').send_keys("Sam")
    driver.find_element('xpath', "//div[text()='Generate']").click()
    return driver


# # update remarks
def update_remarks(driver):
    time.sleep(3)
    driver.find_element('xpath', '//input[@placeholder="Remarks"]').send_keys(
        "Has a cheerful attitude that benefits her teammates")
    return driver


# # to generate and download
def generate_and_download(driver):
    driver.find_element('xpath', '//div[text()="Generate"]').click()
    time.sleep(5)
    driver.find_element('xpath', "//div[text()='Download']").click()
    return driver


def validate_the_history_certificate(driver):
    is_disply = driver.find_element('xpath', "//h2[text()='Generate School leaving certificate']").is_displayed()
    assert is_disply, 'not displayed'
    print('VALIDATION DONE')


def login(admin_credentials=["0000020232", "120992", "@Automation-2"], account_name="@Automation-2"):
    driver = get_webdriver_instance()
    driver.implicitly_wait(5)
    WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CSS_SELECTOR, "loader")))
    WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CLASS_NAME, "loader")))
    time.sleep(1)
    enter_phone_number_otp(driver, admin_credentials)
    # user_name = "//div[@class='profile-user-name']/..//div[text()='" + account_name + "']"
    # WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, user_name)))
    # driver.find_element("xpath", user_name).click()

    dashboard_xpath = "//a[text()='Dashboard']"
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, dashboard_xpath)))
    time.sleep(5)
    refresh()
    time.sleep(2)
    navigate_to_certificate(driver)
    select_certificate_type(driver)
    search_and_select_student(driver)
    update_remarks(driver)
    generate_and_download(driver)
    validate_the_history_certificate(driver)
    time.sleep(5)

    return driver


def main():
    driver = login()


# driver.quit()

if __name__ == "__main__":
    print("start")
    main()
    print("end")
