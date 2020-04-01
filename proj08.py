''' Your header goes here '''

import csv
import pylab
from operator import itemgetter


def open_file():
    '''
        WRITE DOCSTRING HERE!
    '''
    try:
        file_name = 'video_game_sales_small.csv'
        fp = open(file_name, encoding='utf-8')
        print("Opening the %s file" % file_name)
        return fp
    except FileNotFoundError:
        print("Error: Couldn't open the %s file" % file_name)


def read_file(fp):
    '''
        WRITE DOCSTRING HERE!
    '''
    csv_reader = csv.reader(fp, delimiter=',')
    lines = list(csv_reader)
    data = []
    total_global_sales = 0

    _name_col_no = 0
    _platform_col_no = 1
    _year_col_no = 2
    _genre_col_no = 3
    _publisher_col_no = 4
    _na_sales_col_no = 5
    _eur_sales_col_no = 6
    _jpn_sales_col_no = 7
    _other_sales_col_no = 8
    _total_global_sales_col_no = 9

    for line in lines[1:]:
        # print(line)
        name = line[0].lower().strip()
        platform = line[1].lower().strip()
        # Neglecting the data with N/A literal
        if line[2] != 'N/A':
            year = int(line[2])
        else:
            continue
        genre = line[3].lower().strip()
        publisher = line[4].lower()
        na_sales = float(line[5]) * 1e+6
        europe_sales = float(line[6]) * 1e+6
        japan_sales = float(line[7]) * 1e+6
        other_sales = float(line[8]) * 1e+6

        total_global_sales += na_sales + europe_sales + japan_sales + other_sales

        # The regional sales values are multiplied by 1,000,000.
        data.append([name, platform, year, genre, publisher,
                     na_sales, europe_sales, japan_sales, other_sales,
                     total_global_sales])

    D1 = {}
    D2 = {}
    D3 = {}

    # Update D1
    for row in data:
        D1[row[_name_col_no]] = [
            (row[_name_col_no],
             row[_platform_col_no],
             row[_year_col_no],
             row[_genre_col_no],
             row[_publisher_col_no],
             row[_total_global_sales_col_no])
        ]
    # print(D1)

    for row in data:
        # If genre already exits
        if row[_genre_col_no] in D2:
            # if same year exists update it
            if D2[row[_genre_col_no]][0][1] == row[_year_col_no]:
                # update the same
                D2[row[_genre_col_no]][0][2] += row[_na_sales_col_no]
                D2[row[_genre_col_no]][0][3] += row[_eur_sales_col_no]
                D2[row[_genre_col_no]][0][4] += row[_jpn_sales_col_no]
                D2[row[_genre_col_no]][0][5] += row[_other_sales_col_no]
                D2[row[_genre_col_no]][0][6] += row[_total_global_sales_col_no]
            else:
                D2[row[_genre_col_no]].append(
                    [
                        row[_genre_col_no],
                        row[_year_col_no],
                        row[_na_sales_col_no],
                        row[_eur_sales_col_no],
                        row[_jpn_sales_col_no],
                        row[_other_sales_col_no],
                        row[_total_global_sales_col_no]
                    ]
                )


        else:
            # Create it
            D2[row[_genre_col_no]] = [[
                row[_genre_col_no],
                row[_year_col_no],
                row[_na_sales_col_no],
                row[_eur_sales_col_no],
                row[_jpn_sales_col_no],
                row[_other_sales_col_no],
                row[_total_global_sales_col_no]
            ]
            ]
    # print(D2)

    for key, _ in D2.items():
        D2[key][0] = tuple(D2[key][0])
    # print(D2)

    for row in data:
        if row[_publisher_col_no] in D3:
            D3[row[_publisher_col_no]].append(
                (row[_publisher_col_no],
                 row[_name_col_no],
                 row[_year_col_no],
                 row[_na_sales_col_no],
                 row[_eur_sales_col_no],
                 row[_jpn_sales_col_no],
                 row[_other_sales_col_no],
                 row[_total_global_sales_col_no]
                 )
            )
        else:
            D3[row[_publisher_col_no]] = [
                (row[_publisher_col_no],
                 row[_name_col_no],
                 row[_year_col_no],
                 row[_na_sales_col_no],
                 row[_eur_sales_col_no],
                 row[_jpn_sales_col_no],
                 row[_other_sales_col_no],
                 row[_total_global_sales_col_no]
                 )
            ]

    # Sort Dictionaries by Keys 'Ascending' and total global sales 'Descending'
    for _dict in [D1, D2, D3]:
        _temp = {}
        for key in sorted(_dict.keys()):
            _dict[key].sort(key=lambda tup: tup[-1], reverse=True)
            _temp[key] = _dict[key]
        _dict = _temp
    # print(D1)
    return D1, D2, D3


def get_data_by_column(D1, indicator, c_value):
    '''
        WRITE DOCSTRING HERE!
    '''
    return_list = []

    if indicator is 'year':
        col_num = 2
        c_value = int(c_value)
    elif indicator is 'platform':
        col_num = 1

    for key in D1.keys():
        if D1[key][0][col_num] == c_value:
            return_list.append(D1[key][0])

    # global sales in descending order
    return_list.sort(key=lambda tup: tup[-1], reverse=True)
    # return_list.sort(key=lambda tup: tup[1])

    return return_list


def get_publisher_data(D3, publisher):
    '''
        WRITE DOCSTRING HERE!
    '''
    if publisher in D3:
        # Sorting by Global sales
        return D3[publisher]

    return []


def display_global_sales_data(L, indicator):
    '''
        WRITE DOCSTRING HERE!
    '''

    header1 = ['Name', 'Platform', 'Genre', 'Publisher', 'Global Sales']
    header2 = ['Name', 'Year', 'Genre', 'Publisher', 'Global Sales']
    total_global_sales = 0
    if indicator is 'year':
        print("{:30s}{:10s}{:20s}{:30s}{:12s}".format(*header1))
        for element in L:
            print("{:30s}{:10s}{:20s}{:30s}{:<12,.02f}".format(element[0],
                                                               element[1], element[3], element[4], element[5])
                  )
            total_global_sales += element[5]
    elif indicator is 'platform':
        print("{:30s}{:10s}{:20s}{:30s}{:12s}".format(*header2))
        for element in L:
            print("{:30s}{:10s}{:20s}{:30s}{:<12,.02f}".format(element[0],
                                                               str(element[2]), element[3], element[4], element[5])
                  )
            total_global_sales += element[5]

    print("\n{:90s}{:<12,.02f}".format('Total Sales', total_global_sales))


def get_genre_data(D2, year: int):
    '''
        WRITE DOCSTRING HERE!
    '''
    # print(D2)
    genre_list = []
    for key in D2.keys():
        for element in D2[key]:
            if element[1] == year:
                genre_list.append(element)

    genre_dict = {}
    for item in genre_list:
        if item[0] in genre_dict:
            genre_dict[item[0]][1] += 1
            genre_dict[item[0]][2] += item[2]
            genre_dict[item[0]][3] += item[3]
            genre_dict[item[0]][4] += item[4]
            genre_dict[item[0]][5] += item[5]
            genre_dict[item[0]][6] += item[6]
        else:
            genre_dict[item[0]] = [
                item[0],
                1,
                item[2],
                item[3],
                item[4],
                item[5],
                item[6],
            ]

    genre_list = [tuple(v) for _, v in genre_dict.items()]
    genre_list.sort(key=lambda tup: tup[-1], reverse=True)

    return genre_list


def display_genre_data(genre_list):
    '''
        WRITE DOCSTRING HERE!
    '''
    total_global_sales = 0
    header = ['Genre', 'North America', 'Europe', 'Japan', 'Other', 'Global']

    print("{:15s}{:15s}{:15s}{:15s}{:15s}{:15s}".format(*header))

    for genre in genre_list:
        print("{:15s}{:<15,.02f}{:<15,.02f}{:<15,.02f}{:<15,.02f}{:<15,.02f}".format(
            genre[0], genre[2], genre[3], genre[4], genre[5], genre[6]
        ))
        total_global_sales += genre[6]
    print("\n{:75s}{:<15,.02f}".format('Total Sales', total_global_sales))


def display_publisher_data(pub_list):
    '''
        WRITE DOCSTRING HERE!
    '''
    pub = pub_list[0][0]
    # print(pub_list)
    total_global_sales = 0
    header = ['Title', 'North America', 'Europe', 'Japan', 'Other', 'Global']
    print("{:30s}{:15s}{:15s}{:15s}{:15s}{:15s}".format(*header))
    for publisher in pub_list:
        print("{:30s}{:<15,.02f}{:<15,.02f}{:<15,.02f}{:<15,.02f}{:<15,.02f}".format(
            publisher[1], publisher[3], publisher[4], publisher[5], publisher[6], publisher[7],
        ))
        total_global_sales += publisher[7]
    print("\n{:90s}{:<15,.02f}".format('Total Sales', total_global_sales))


def get_totals(L, indicator):
    '''
        WRITE DOCSTRING HERE!
    '''

    list_1 = []
    list_2 = []

    if indicator is 'year':
        L.sort()
        list_1_col_number = 1  # platform column
    elif indicator is 'platform':
        L.sort(key=lambda tup: tup[2])
        list_1_col_number = 2  # year column

    print(L)
    for element in L:
        list_1.append(element[list_1_col_number])
        list_2.append(element[-1])

    return list_1, list_2


def prepare_pie(genres_list):
    '''
        WRITE DOCSTRING HERE!
    '''
    # Descending sorting by the global sales values descending
    genres_list.sort(key=lambda tup: tup[-1], reverse=True)
    # Genre Names
    list_1 = [element[0] for element in genres_list]
    # Global sales
    list_2 = [element[-1] for element in genres_list]

    return list_1, list_2


def plot_global_sales(x, y, indicator, value):
    """
        This function plots the global sales per year or platform.

        parameters:
            x: list of publishers or year sorted in ascending order
            y: list of global sales that corresponds to x
            indicator: "publisher" or "year"
            value: the publisher name (str) or year (int)

        Returns: None
    """

    if indicator == 'year':
        pylab.title("Video Game Global Sales in {}".format(value))
        pylab.xlabel("Platform")
    elif indicator == 'platform':
        pylab.title("Video Game Global Sales for {}".format(value))
        pylab.xlabel("Year")

    pylab.ylabel("Total copies sold (millions)")

    pylab.bar(x, y)
    pylab.show()


def plot_genre_pie(genre, values, year):
    '''
        This function plots the global sales per genre in a year.
        
        parameters: 
            genre: list of genres that corresponds to y order
            values: list of global sales sorted in descending order 
            year: the year of the genre data (int)
        
        Returns: None
    '''

    pylab.pie(values, labels=genre, autopct='%1.1f%%')
    pylab.title("Video Games Sales per Genre in {}".format(year))
    pylab.show()


def main():
    # Menu options for the program
    MENU = '''Menu options

    1) View data by year
    2) View data by platform
    3) View yearly regional sales by genre
    4) View sales by publisher
    5) Quit

    Enter choice: '''

    D1, D2, D3 = read_file(open_file())

    choice = input(MENU)

    while choice != '5':

        # Option 1: Display all platforms for a single year
        try:
            if choice == '1':
                choice = 0
                year = int(input("Enter year: "))
                l = get_data_by_column(D1, 'year', year)
                display_global_sales_data(l, 'year')
                is_to_plot = input("Do you want to plot (y/n)? ")
                if is_to_plot is 'y':
                    l1, l2 = get_totals(l, 'year')
                    plot_global_sales(l1, l2, 'year', year)
            # if the list of platforms for a single year is empty, show an error message
        except ValueError:
            print("Invalid year.")
        try:
            if choice == '2':
                choice = 0
                platform = input("Enter platform: ")
                l = get_data_by_column(D1, 'platform', platform)
                display_global_sales_data(l, 'platform')
                is_to_plot = input("Do you want to plot (y/n)? ")
                if is_to_plot is 'y':
                    l1, l2 = get_totals(l, 'platform')
                    plot_global_sales(l1, l2, 'platform', platform)
        except ValueError:
            print("Invalid platform.")

        try:
            if choice == '3':
                choice = 0
                year = int(input("Enter year: "))
                gen_list = get_genre_data(D2, year)
                display_genre_data(gen_list)
                l1, l2 = prepare_pie(gen_list)
                plot_genre_pie(l1, l2, year)
        except ValueError:
            print("Invalid year.")

        # Option 4: Display publisher data
        if choice == '4':
            choice = 0
            # Enter keyword for the publisher name
            publisher = input('Enter keyword for publisher: ')
            # search all publisher with the keyword
            match = []
            for pub in D3.keys():
                if publisher in pub:
                    match.append(pub)

            # print the number of matches found with the keywords
            if len(match) > 1:
                print("There are {} publisher(s) with the requested keyword!".format(len(match)))
                for i, t in enumerate(match):
                    print("{:<4d}{}".format(i, t))
                # PROMPT USER FOR INDEX
                index = int(input('Select the index for the publisher to use: '))
                publisher = match[index]

                display_publisher_data(get_publisher_data(D3, publisher))
            else:
                index = 0

        choice = input(MENU)

    print("\nThanks for using the program!")
    print("I'll leave you with this: \"All your base are belong to us!\"")


if __name__ == "__main__":
    main()
