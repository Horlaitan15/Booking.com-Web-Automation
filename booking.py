from selenium import webdriver
from selenium.webdriver.common.by import By
from filter import BookingFiltration
import os
import time

try:
    os.mkdir("Data Output files")
    os.mkdir("Screenshots")
except FileExistsError:
    pass


class Booking(webdriver.Firefox):
    def __init__(self):
        super(Booking, self).__init__()

    # This is the first function that will get the booking.com homepage.
    def get_booking_first_page(self):
        self.maximize_window()
        self.get('https://booking.com')
        self.implicitly_wait(10)
        self.save_full_page_screenshot("Screenshots/booking_home_page.png")

    # This is the function that changes the currency to the preferred one.
    def change_currency(self, currency='NGN'):
        currency_box = self.find_element(by=By.CSS_SELECTOR,
                                         value="button[data-modal-header-async-type='currencyDesktop']"
                                         )
        currency_box.click()

        self.implicitly_wait(10)
        my_currency = self.find_element(by=By.CSS_SELECTOR,
                                        value=f"a[data-modal-header-async-url-param*='selected_currency={currency}']"
                                        )
        my_currency.click()

    # This is te function that will select the destination of the lodger.
    def select_destination(self, destination='CANADA'):
        destination_search = self.find_element(by=By.NAME, value="ss")
        destination_search.clear()  # Clears the input box of any leftover text.

        time.sleep(3)
        destination_search.send_keys(destination)  # sends the desired input.
        time.sleep(3)
        hotels_locations = self.find_element(by=By.CSS_SELECTOR, value="li[data-i='0']")
        hotels_locations.click()

    # This is the function that will select the check in and check out dates.
    def select_check_in_and_out(self, check_in="2022-11-10", check_out="2022-11-29"):
        check_in = self.find_element(by=By.CSS_SELECTOR, value=f"td[data-date='{check_in}']")
        check_in.click()

        check_out = self.find_element(by=By.CSS_SELECTOR, value=f"td[data-date='{check_out}']")
        check_out.click()

    # This is the function that will select the number of lodgers and rooms.
    def select_guest_count(self, adults):
        guest_count_element = self.find_element(by=By.CLASS_NAME, value='xp__guests__count')
        guest_count_element.click()

        decrease_adults_counts = self.find_element(by=By.CSS_SELECTOR,
                                                   value="button[aria-label='Decrease number of Adults']"
                                                   )
        increase_adults_counts = self.find_element(by=By.CSS_SELECTOR,
                                                   value="button[aria-label='Increase number of Adults']"
                                                   )

        # Returns the adults input value to 1
        while True:
            decrease_adults_counts.click()
            adult_count_element = self.find_element(by=By.ID, value='group_adults')
            adult_count = adult_count_element.get_attribute('value')

            if int(adult_count) == 1:
                break

        # Increases the adults input value by the number of lodgers.
        for _ in range(adults - 1):
            increase_adults_counts.click()

    # This is the function that will click on the serch button.
    def search(self):
        search_button = self.find_element(by=By.CLASS_NAME,
                                          value='sb-searchbox__button '
                                          )
        search_button.click()

    # This function will call the instance of the BookingFiltration class.
    def filtration(self):
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating()
        filtration.sort_by_highest_rating_and_lowest_price()
        filtration.call_the_scraper()
