from xlsxwriter import Workbook


workbook = Workbook('booking.xlsx')


def write_sheet_headers(data, rows):
    if rows == 1:
        # Create the worksheet in which data will be stored.
        worksheet = workbook.add_worksheet("Hotels List")
        # Write the title of each column of the worksheet.
        worksheet.write("A1", "Hotel Name")
        worksheet.write("B1", "Hotel Address")
        worksheet.write("C1", "Room Type")
        worksheet.write("D1", "Availability Link")
        worksheet.write("E1", "Hotel Price")
        worksheet.write("F1", "Tax")
        worksheet.write("G1", "Hotel Total Cost")
        worksheet.write("H1", "Hotel Rating")
        worksheet.write("I1", "Hotel Score")
    else:
        worksheet = workbook.get_worksheet_by_name("Hotels List")

    # Unzip the data and pass it into a list.
    data_list = list(zip(*data))

    for data_list_column_count, excel_data in enumerate(data_list):
        for data_list_row_count, excel_row_data in enumerate(excel_data):
            worksheet.write(data_list_column_count, data_list_row_count, excel_row_data)
    # # Iterate through the data_list elements. The data_list contains 9 lists.
    # for data_list_count in range(len(data_list)):
    #     excel_data = data_list[data_list_count]

    #     # Iterate through the excel_data. The excel data_data contains 25 elements.
    #     for excel_data_count in range(len(excel_data)):
    #         # Write in the excel sheet. y-axis          x-axis          data
    #         worksheet.write(excel_data_count + rows, data_list_count, excel_data[excel_data_count])
    #         print(data_list_count, excel_data_count + rows, excel_data[excel_data_count])

    workbook.close()
