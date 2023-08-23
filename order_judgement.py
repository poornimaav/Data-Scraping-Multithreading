import pandas as pd
from selenium.webdriver.common.by import By
import os
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging_utils
import threading

file_lock = threading.Lock()

def scrape_order_judgment_table(driver, filing_number, diary_number):
    logger = logging_utils.setup_logging('scraping_log.log')
    try: 
        serial_number = 1  
        expand_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="headingTwo"]/h2/button'))) 
        # expand_button = driver.find_element(By.XPATH, '//*[@id="headingTwo"]/h2/button')
        expand_button.click()
        
        # Parse the page source with BeautifulSoup
        table_xpath = '//*[@id="collapseTwo"]/div/div/table'
        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, table_xpath)))
        
        # table = driver.find_element(By.XPATH, table_xpath)

        
        # Extract the data from the table rows
        header_row = table.find_element(By.TAG_NAME, "thead").find_element(By.TAG_NAME, "tr")
        header_cells = header_row.find_elements(By.TAG_NAME, "th")
        headers = [cell.text.strip() for cell in header_cells]

        
        # Extract the table data
        table_data = []
        rows = table.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) == len(headers):
                row_data = {}
                for i, cell in enumerate(cells):
                    if cell.find_elements(By.TAG_NAME, "a"):  # Check if the cell contains a link
                        pdf_link_element = cell.find_element(By.TAG_NAME, "a")
                        pdf_link = pdf_link_element.get_attribute("href")
                        row_data[headers[i]] = pdf_link
                    else:
                        row_data[headers[i]] = cell.text.strip()
                  
                table_data.append(row_data)

        df3 = pd.DataFrame(table_data)

        csv_filename = "outputs/order_judgement.csv"


        if os.path.isfile(csv_filename) and os.path.getsize(csv_filename) > 0:
            existing_df = pd.read_csv(csv_filename)
            last_serial_number = existing_df['S. No'].max()
            if not pd.isna(last_serial_number):
                serial_number = int(last_serial_number) + 1   
        
        if not df3.empty: 
            df3.drop("S.No.", axis=1, inplace=True)
            df3.insert(0, "S. No", range(serial_number, serial_number + len(df3)))
            df3.insert(1, "Filing Number", filing_number)    
            # Create a DataFrame from the extracted table data           
            if not os.path.isfile(csv_filename) or os.path.getsize(csv_filename) == 0:
                 df3.to_csv(csv_filename, index=False, mode='w')  # Save with header
            else:
                df3.to_csv(csv_filename, index=False, mode='a', header=False)  # Append without header

            logger.info("%s - Order/Judgement table data (including links) saved to %s",diary_number, csv_filename)
        else:
           logger.info("%s - Order/Judgement table is empty. Not saving to CSV.", diary_number)


    except NoSuchElementException as e:
       logger.error("%s - Error while scraping Order/Judgment table: %s", diary_number, str(e))

    except Exception as e:
        logger.error("%s - Error while scraping Order/Judgment table: %s", diary_number, str(e))