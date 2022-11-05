from booking import Booking
import pyfiglet
from colorama import Fore

# currency = input("Please enter your preferred currency: ")
# destination = input("Please enter your preferred destination: ")
# adults = int(input("KIndly the number of adults: "))


currency = "CAD"
destination = "Canada"
adults = 4


if __name__ == "__main__":
    print(pyfiglet.figlet_format("Web Automation and Scraping.", font='doh', width=200))
    print(Fore.YELLOW + "This script automates searching for hotels at a particular location using the specified info https://booking.com.")
    print(Fore.BLUE + "It automatically select currency, location, check-in and check-out dates, number of adults to be lodged and uses the search  button to apply the remaining filterations.")
    print(Fore.CYAN + "It then saves the information about the available hotels in a CSV file.")
    booking = Booking()
    booking.get_booking_first_page()
    booking.change_currency(currency)
    booking.select_destination(destination)
    booking.select_check_in_and_out()
    booking.select_guest_count(adults)
    booking.search()
    booking.filtration()
