from bs4 import BeautifulSoup
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from googlesheet import add_data_to_gsheets
from to_csv import write_csv
import re
from to_excel import write_sheet_headers
from to_json import write_booking_json


def scraper(driver: WebDriver, rows=1):
    driver.refresh()
    next_page = driver.find_element(by=By.CSS_SELECTOR,
                                    value="button[aria-label='Next page']"
                                    )
    hotel_attributes_list = []
    # Create an html file to be parsed by BeautifulSoup.
    with open('page.html', 'w') as f:
        f.write(driver.page_source)

    # Open the page html file.
    page_html = open('page.html', 'r')
    soup = BeautifulSoup(page_html, 'lxml')

    hotels = soup.select("div[data-testid='property-card']")
    print(len(hotels))

    for hotel in hotels:
        hotel_name = hotel.select_one("div[data-testid='title']").text

        try:
            if hotel.select_one("div[data-testid='review-score'] div[aria-label*='Scored']") is not None:
                hotel_score = hotel.select_one("div[data-testid='review-score'] div[aria-label*='Scored']").text
            else:
                hotel_score = hotel.select_one("div[data-testid='external-review-score'] div div"
                                               ).text
        except AttributeError:
            hotel_score = "No score yet"

        try:
            hotel_rating = len(hotel.select("div[data-testid='rating-stars'] span"))
        except AttributeError:
            hotel_rating = 'No ratings yet'

        hotel_price = hotel.select_one("div[data-testid='price-and-discounted-price'] span" # span[data-testid='price-and-discounted-price']"
                                       ).text.replace('\xa0', ' ')
        # print(hotel_price)
        # print(hotel_price[4:])

        # Gets the amount of tax to be paid
        hotel_tax = hotel.select_one("div[data-testid='taxes-and-charges']"
                                     ).text.replace('\xa0', ' ')
        if hotel_tax != "Includes taxes and fees":
            hotel_tax = re.findall(r'.+?(?=\d)\d{1,}', hotel_tax)[0][1:]
        else:
            hotel_tax = f"{hotel_price[:3]} 0"

        total_cost = int(re.findall(r'\d{1,}', hotel_price.replace(',', ''))[0]) + int(re.findall(r'\d{1,}', hotel_tax.replace(',', 'S'))[0])
        total_cost = re.findall(r'.+?(?=\d)', hotel_price)[0]+str(total_cost)

        # Gets the type of room.
        room_type = hotel.select_one("div[data-testid='recommended-units'] div[role='link'] span"
                                     ).text
        # Get availabity link.
        try:
            availability_link = hotel.select_one("div[data-testid='availability-cta'] a[role='button']"
                                             )['href']
        except:
            availability_link = "no_link"

        hotel_address = hotel.select_one("span[data-testid='address']"
                                         ).text

        hotel_attributes_list.append([hotel_name,
                                    hotel_address,
                                    room_type,
                                    availability_link,
                                    hotel_price,
                                    hotel_tax,
                                    total_cost,
                                    hotel_rating,
                                    hotel_score]
                               )

    # Call the function that writes the json file
    write_booking_json(hotel_attributes_list, rows)

    # Call the function that help write our clean data to Google Sheet.
    add_data_to_gsheets(hotel_attributes_list, rows)

    # Call the function that helps write our clean data to excel file.
    write_sheet_headers(hotel_attributes_list, rows)

    # Call the function that helps write our csv file.
    write_csv(hotel_attributes_list, rows)

    # Increases the number of rows to start writing our Google sheet and excel file.
    rows += len(hotels)
    print(hotel_attributes_list)

    # Checks if there are still pages left to crawl.
    if next_page.get_attribute('disabled') is None:
        next_page.click()
        # Takes the screenshot of the current page.
        driver.save_screenshot(f'Screenshots/{hotel_name}.png')
        scraper(driver, rows)
    else:
        driver.quit()
