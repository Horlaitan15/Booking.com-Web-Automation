import json


def write_booking_json(data, rows):
    hotels = {}
    counts = rows

    for hotel in data:
        hotels[f'Hotel{counts}'] = {
            "Hotel Name":           hotel[0],
            "Hotel Address":        hotel[1],
            "Room Type":            hotel[2],
            "Availability Link":    hotel[3],
            "Hotel Price":          hotel[4],
            "Tax":                  hotel[5],
            "Hotel Total Cost":     hotel[6],
            "Hotel Rating":         hotel[7],
            "Hotel Score":          hotel[8]
                                    }
        counts += 1

    print(hotels)

    if rows == 1:
        with open('Booking.json', 'w') as json_output:
            json.dump(hotels, json_output, indent=4)
    else:
        with open('Booking.json', 'r+') as json_file:
            json_output = json.load(json_file)
            json_output.update(hotels)
            json_file.seek(0)
            json.dump(json_output, json_file, indent=4)
