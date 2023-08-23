from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from main_table import scrape_data_from_current_page
from config_utils import config, write_config
import time
import logging_utils
import multiprocessing

logger = logging_utils.setup_logging('scraping_log.log')

def process_range(start_diary_number, end_diary_number):
    try:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)


        count = 1
        for diary_number in range(start_diary_number, end_diary_number, 2):
            config_copy = config.copy()
            config_copy['diaryno'] = str(diary_number)
            write_config(config_copy)
            
            logger.info("%s - Iteration - %d started", config_copy["diaryno"], count)

            start_time = time.time()
            scrape_data_from_current_page(driver, config_copy)
            end_time = time.time()

            loop_time = end_time - start_time

            logger.info("%s - Iteration - %d completed in %s seconds", config_copy["diaryno"], count, round(loop_time, 2))
            # time.sleep(5)
            count += 1

    except Exception as e:
        logger.error("An error occurred %s", str(e))

    finally:
        driver.quit()

if __name__ == "__main__":
    num_processes = 2  # Number of processes to run concurrently
    start_diary_number = int(config["diaryno"]) + 1
    end_diary_number = start_diary_number + 6

    processes = []
    start_time = time.time()
    for i in range(num_processes):
        start = start_diary_number + i
        end = end_diary_number
        process = multiprocessing.Process(target=process_range, args=(start, end))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    end_time = time.time()
    total_time = end_time - start_time
    logger.info("Time taken to all iterations %s seconds", round(total_time, 2))