from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from scrape import scraper
import pyfiglet


class BookingFiltration:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    # This is the function that will apply the desired rating. default are 3, 4, and 5.
    def apply_star_rating(self, star_ratings=(3, 4, 5)):
        for star_rating in star_ratings:
            star_rating_element = self.driver.find_element(by=By.CSS_SELECTOR,
                                                           value=f'div[data-filters-item="class:class={star_rating}"]'
                                                           )
            star_rating_element.click()

    # This is the function that will sort by highest rating and lowest price.
    def sort_by_highest_rating_and_lowest_price(self):
        self.driver.refresh()
        try:
            highest_rating_and_lowest_price_element = self.driver.find_element(by=By.CSS_SELECTOR,
                                                                               value="a[data-type='review_score_and_price']"
                                                                               )
            highest_rating_and_lowest_price_element.click()
        except NoSuchElementException:
            pass


    # This function will call the scrapper function.
    def call_the_scraper(self):
        scraper(driver=self.driver)
        print(pyfiglet.figlet_format("Thanks,\nAjani", font='doh', width=200))

