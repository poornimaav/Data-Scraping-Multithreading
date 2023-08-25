from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from main_table import scrape_data_from_current_page
from config_utils import config, write_config
import time
import logging_utils
import threading


def process_range(start_diary_number, end_diary_number, logger, t):
    try:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)

        count = 1
        for diary_number in range(start_diary_number, end_diary_number):
            config_copy = config.copy()
            config_copy['diaryno'] = str(diary_number)
            write_config(config_copy)
            
            logger.info("%s - Iteration - %d started for thread %d", config_copy["diaryno"], count, t)

            start_time = time.time()
            scrape_data_from_current_page(driver, config_copy, logger, t)
            end_time = time.time()

            loop_time = end_time - start_time

            logger.info("%s - Iteration - %d completed in %s seconds for thread %d", config_copy["diaryno"], count, round(loop_time, 2), t)

            count += 1

    except WebDriverException as e:
        if "ERR_INTERNET_DISCONNECTED" in str(e):
            logger.error("Internet connection lost. Please check your connection.")
        else:
            logger.error("An error occurred: ", str(e))

    except KeyboardInterrupt:
        logger.error("Script interrupted by the user.")   

    except Exception as e:
        logger.error("An error occurred: %s", str(e))

    finally:
        driver.quit()

if __name__ == "__main__":
    logger = logging_utils.setup_logging('scraping_log.log')
    t1 = 1
    t2 = 2

    total_time = 0
    
    start_number1 = int(config["diaryno"]) + 1  # Convert to integer
    end_number1 = start_number1 + 1

    start_number2 = end_number1
    end_number2 = start_number2 + 1

    
    start_time = time.time()

    t1 = 1
    thread1 = threading.Thread(target = process_range, args = (start_number1, end_number1, logger, t1))
    
    t2 = 2
    thread2 = threading.Thread(target = process_range, args = (start_number2 , end_number2, logger, t2))
    
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    end_time = time.time()
    total_time = end_time - start_time

    logger.info("Total time taken for all iterations: %s seconds", round(total_time, 2))
        


