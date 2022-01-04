# Tools to clean the bookings data and separate bookings by year (at least for now)

import csv

zip_codes = set(["33160","33139","33186","33027","33012","33157","33178","33015",
                 "33141","33033","33125","33176","33032","33180","33142","33179",
                 "33126","33130","33018","33165","33161","33177","33175","33134",
                 "33196","33131","33172","33155","33016","33133","33193","33014",
                 "33147","33137","33010","33143","33135","33162","33140","33169",
                 "33156","33055","33138","33183","33173","33132","33145","33056",
                 "33030","33174","33166","33054","33150","33127","33154","33144",
                 "33013","33189","33185","33181","33129","33168","33136","33034",
                 "33149","33184","33167","33146","33035","33187","33170","33190",
                 "33182","33128","33158","33031","33194","33261","33122","33114",
                 "33017","33101","33247","33256","33197","33090","33269","33238",
                 "33283","33109","33265","33242","33152","33116","33222","33245",
                 "33093","33011","33092","33296","33002","33119","33255","33153",
                 "33243","33233","33164","33231","33257","33239","33266","33280",
                 "33234","33163","33124","33039","33107","33102","33110","33112",
                 "33111","33121","33148","33151","33159","33188","33192","33199",
                 "33299","33191","33206","33198","33195","33106"])

def clean_bookings_data(filename):
    cleaned_bookings, discarded_bookings = [], []
    with open(filename, newline='') as bookings_file:
        bookings_reader = csv.DictReader(bookings_file)
        for arrest in bookings_reader:
            if is_in_dade_county(arrest):
                cleaned_bookings.append(arrest)
            else:
                discarded_bookings.append(arrest)

    return ( cleaned_bookings, discarded_bookings )


def is_in_dade_county(arrest):
    has_dade_zip = arrest['Zip'].strip() in zip_codes
    is_in_florida = arrest['State'].strip() == 'FL'
    has_address = arrest['Address'].strip() not in ('', 'HOMELESS', 'ADDRESS UNKNOWN')

    if has_dade_zip and is_in_florida and has_address:
        return True

    return False

def write_cleaned_bookings_data(cleaned_bookings, new_filename):
    with open(new_filename, 'w', newline='') as new_bookings_file:
        fieldnames = cleaned_bookings[0].keys()
        new_bookings_writer = csv.DictWriter(new_bookings_file, fieldnames=fieldnames)

        new_bookings_writer.writeheader()
        for arrest in cleaned_bookings:
            new_bookings_writer.writerow(arrest)

def write_discarded_bookings_data(cleaned_bookings, discarded_filename):
    with open(discarded_filename, 'w', newline='') as discarded_bookings_file:
        fieldnames = cleaned_bookings[0].keys()
        discarded_bookings_writer = csv.DictWriter(discarded_bookings_file, fieldnames=fieldnames)

        discarded_bookings_writer.writeheader()
        for arrest in cleaned_bookings:
            discarded_bookings_writer.writerow(arrest)

def main():
    raw_filenames = [f'{year}_bookings.csv' for year in range(2015,2021)]
    cleaned_filenames = [f'{year}_cleaned_bookings.csv' for year in range(2015,2021)]
    discarded_filenames = [f'{year}_discarded_bookings.csv' for year in range(2015,2021)]

    for i, file in enumerate( raw_filenames ):
        cleaned_bookings, discarded_bookings = clean_bookings_data(file)
        write_cleaned_bookings_data(cleaned_bookings, cleaned_filenames[i])
        write_discarded_bookings_data(discarded_bookings, discarded_filenames[i])

if __name__ == "__main__":
    main()
