import pygsheets
import pandas as pd
import io


# authorization
gsheets = pygsheets.authorize(service_file='keys.json')


def add_data_to_gsheets(data, rows):
    # Create empty dataframe
    df = pd.DataFrame()


    name, address, room, availability, price, tax, total_cost, rating, score = zip(*data)

    df['Hotel Name'] = list(name)
    df['Hotel Address'] = list(address)
    df['Room Type'] = list(room)
    df['Availability Link'] = list(availability)
    df['Hotel Price'] = list(price)
    df['Tax'] = list(tax)
    df['Hotel Total Cost'] = list(total_cost)
    df['Hotel Rating'] = list(rating)
    df['Hotel Score'] = list(score)

    print(df)

    # if rows != 1:
    #     df = pd.read_csv(io.StringIO(u""+df.to_csv(header=None, index=False)), header=None)

    # open the Google spreadsheet (where 'Booking.com Hotels Sheet' is the name of my sheet)
    sheet = gsheets.open_by_url('https://docs.google.com/spreadsheets/d/1GBRzYjhxiPVm0x1oE1wtVqi_gLMZRax00OUZSrxSycY/edit#gid=0')

    # select the first sheet
    wks = sheet[0]

    if rows == 1:
        # update the first sheet with df, starting at cell A!.
        wks.set_dataframe(df, (rows, 1))
    else:
        wks.set_dataframe(df, (rows, 1), copy_head=False, extend=True)
