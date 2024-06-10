import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.fixture(params=["chrome", "edge"])
def browser(request):
    if request.param == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized") # Максимизируем окно
        driver = webdriver.Chrome(options=options)
    elif request.param == "edge":
        driver = webdriver.Edge()
    else:
        raise ValueError("Invalid browser name")
    
    yield driver

    driver.quit()

def test_log_in_button(browser):
    browser.get("https://www.reddit.com/")
    time.sleep(2)

    # Ждем, пока кнопка "Log In" станет кликабельной
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login-button"]'))).click()
    assert browser.current_url == "https://www.reddit.com/login/"

def test_three_dots_button(browser):
    browser.get("https://www.reddit.com/")
    time.sleep(2)

    # Ждем, пока кнопка с тремя точками станет кликабельной
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="expand-user-drawer-button"]'))).click()
    # Проверяем, что открыто меню с настройками
    assert WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="user-drawer-content"]')))

def test_search(browser):
    browser.get("https://www.reddit.com/")
    time.sleep(2)

    # Ждем, пока поисковая строка станет видимой
    search_input = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="search-input"]//label/div/span[2]/input')))
    search_input.send_keys("Python")
    search_input.send_keys(Keys.RETURN)
    time.sleep(2)

    # Проверяем, что мы перешли на страницу с результатами поиска
    assert "search" in browser.current_url
