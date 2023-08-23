from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def automate_selection(driver, element_id, value):
    select_element = Select(driver.find_element(By.ID, element_id))
    select_element.select_by_value(value)   

def automate_input_element(driver, element_id, value):
    input_element = driver.find_element(By.ID, element_id)
    input_element.clear()
    input_element.send_keys(value)