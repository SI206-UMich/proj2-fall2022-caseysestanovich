#Worked with Ansley Lewis and Mari Jaoshvili!

from xml.sax import parseString
from bs4 import BeautifulSoup
import re
import os
import csv
import unittest


def get_listings_from_search_results(html_file):
    #open file
    f = open(html_file)
 
    title = []
    costPerNight = []
    l_id = []

    soup = BeautifulSoup(f, 'html.parser')

    info = soup.find_all('div', class_ = "t1jojoys dir dir-ltr")
    cost = soup.find_all('span', class_ = "a8jt5op dir dir-ltr")

    for i in info: 
        title.append(i.text.strip())
        l_id.append(i.get('id')[6:])
    
    for i in cost:
        if (i.text.strip()[0] == '$'):
            costPerNight.append(int(i.text.strip()[1:4]))
    
    final_list = []
    for i in range(len(title)):
        tup = (title[i], costPerNight[i], l_id[i])
        final_list.append(tup)

    #file close
    f.close()

    return final_list


def get_listing_information(listing_id):

    filename = 'html_files/listing_' + listing_id + ".html"
    f = open(filename)

    soup = BeautifulSoup(f, 'html.parser')

    # policy number from individual listing
    policy_num= soup.find('li', class_="f19phm7j dir dir-ltr")
    policy_num = policy_num.text.strip()[14:]
    policy_num = policy_num.split()
    if ('pending' in policy_num or 'Pending' in policy_num):
        policy_num = 'Pending'
    elif (policy_num[0] == 'License'):
        policy_num = 'Exempt'
    else:
        policy_num = policy_num[0]

    # room type from individual listing 
    rm_t = soup.find('h2', class_="_14i3z6h")
    rm_t = rm_t.text.strip()
    rm_t = rm_t.split()
    rm_t = rm_t[0] + " Room"

    # number of bedrooms from individual listing
    numRoom = str(soup.find_all('li', class_='l7n4lsf dir dir-ltr'))
    reg = '\d*\s*\w*\s*bedroom|Studio' 
    x = re.findall(reg, numRoom)
    
    if x[0] == 'Studio': 
        bedrooms = 1 
    else: 
        bedrooms = int(x[0][0]) #confused here

    #file close
    f.close()
    
    # tuple of each individual listing in a list
    final_list = ()
    tup = (policy_num, rm_t, bedrooms)
    final_list += tup

    return final_list

def get_detailed_listing_database(html_file):

    final_l = []
    frt = get_listings_from_search_results(html_file)

    #make sure list id is same from first search result
    for i in frt: 
        snd = get_listing_information(i[2])
        final_l.append(i + snd)
    
    return final_l

def write_csv(data, filename):

    f = open(filename, 'w')
    f.write("Listing Title,Cost,Listing ID,Policy Number,Place Type,Number of Bedrooms")
    f.write('\n')

    data_sort = sorted(data, key = lambda t:t[1])

    for i in data_sort: 
        row = ""
        for item in i: 
            row += str(item) + ","
        f.write(row.rstrip(','))
        f.write('\n')
    f.close()


def check_policy_numbers(data):

    temp_pol = []
    temp_id = []
    ran_str = ""
    for i in data: 
        ran_str += (i[3] + " ")
        temp_pol.append(i[3])
        temp_id.append(i[2])
    
    regex = 'STR-000\d{4}|20\d{2}-00\d{4}STR|Pending|Exempt'

    #invalid policy numbers
    wrong = []
    x = re.findall(regex, ran_str)
    for i in range(len(temp_pol)):
        if temp_pol[i] not in x:
            wrong.append(temp_id[i])
    return wrong


def extra_credit(listing_id):
    """
    There are few exceptions to the requirement of listers obtaining licenses
    before listing their property for short term leases. One specific exception
    is if the lister rents the room for less than 90 days of a year.

    Write a function that takes in a listing id, scrapes the 'reviews' page
    of the listing id for the months and years of each review (you can find two examples
    in the html_files folder), and counts the number of reviews the apartment had each year.
    If for any year, the number of reviews is greater than 90 (assuming very generously that
    every reviewer only stayed for one day), return False, indicating the lister has
    gone over their 90 day limit, else return True, indicating the lister has
    never gone over their limit.
    """
    pass


class TestCases(unittest.TestCase):

    def test_get_listings_from_search_results(self):

        get_listings_from_search_results("html_files/mission_district_search_results.html")
        # and save to a local variable
        listings = get_listings_from_search_results("html_files/mission_district_search_results.html")

        # check that the number of listings extracted is correct (20 listings)
        self.assertEqual(len(listings), 20)

        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(listings), list)

        # check that each item in the list is a tuple
        for item in listings: 
            self.assertEqual(type(item), tuple)

        # check that the first title, cost, and listing id tuple is correct (open the search results html and find it)
        self.assertEqual(listings[0], ('Loft in Mission District', 210, '1944564'))
        
        # check that the last title is correct (open the search results html and find it)
        self.assertEqual(listings[-1], ('Guest suite in Mission District', 238, '32871760'))

    def test_get_listing_information(self):

        html_list = ["1623609",
                     "1944564",
                     "1550913",
                     "4616596",
                     "6600081"]
        # call get_listing_information for i in html_list:
        listing_informations = [get_listing_information(id) for id in html_list]

        # check that the number of listing information is correct (5)
        self.assertEqual(len(listing_informations), 5)

        for listing_information in listing_informations:
            # check that each item in the list is a tuple
            self.assertEqual(type(listing_information), tuple)
            # check that each tuple has 3 elements
            self.assertEqual(len(listing_information), 3)
            # check that the first two elements in the tuple are string
            self.assertEqual(type(listing_information[0]), str)
            self.assertEqual(type(listing_information[1]), str)
            # check that the third element in the tuple is an int
            self.assertEqual(type(listing_information[2]), int)

        # check that the first listing in the html_list has policy number 'STR-0001541'
        self.assertEqual(listing_informations[0][0], 'STR-0001541')

        # check that the last listing in the html_list is a "Private Room"
        self.assertEqual(listing_informations[-1][1], "Private Room")

        # check that the third listing has one bedroom
        self.assertEqual(listing_informations[2][2], 1)


    def test_get_detailed_listing_database(self):
        # call get_detailed_listing_database on "html_files/mission_district_search_results.html"
        # and save it to a variable
        detailed_database = get_detailed_listing_database("html_files/mission_district_search_results.html")

        # check that we have the right number of listings (20)
        self.assertEqual(len(detailed_database), 20)
        for item in detailed_database:
            # assert each item in the list of listings is a tuple
            self.assertEqual(type(item), tuple)
            # check that each tuple has a length of 6

        # check that the first tuple is made up of the following:
        # 'Loft in Mission District', 210, '1944564', '2022-004088STR', 'Entire Room', 1
        self.assertEqual(detailed_database[0], ('Loft in Mission District', 210, '1944564', '2022-004088STR', 'Entire Room', 1))

        # check that the last tuple is made up of the following:
        # 'Guest suite in Mission District', 238, '32871760', 'STR-0004707', 'Entire Room', 1
        self.assertEqual(detailed_database[-1], ('Guest suite in Mission District', 238, '32871760', 'STR-0004707', 'Entire Room', 1))


    def test_write_csv(self):
        # call get_detailed_listing_database on "html_files/mission_district_search_results.html"
        # and save the result to a variable
        detailed_database = get_detailed_listing_database("html_files/mission_district_search_results.html")

        # call write csv on the variable you saved
        write_csv(detailed_database, "test.csv")

        # read in the csv that you wrote
        csv_lines = []
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.csv'), 'r') as f:
            csv_reader = csv.reader(f)
            for i in csv_reader:
                csv_lines.append(i)
        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines), 21)

        # check that the header row is correct
        header = ['Listing Title','Cost','Listing ID','Policy Number','Place Type','Number of Bedrooms']
        self.assertEqual(csv_lines[0], header)  

        # check that the next row is Private room in Mission District,82,51027324,Pending,Private Room,1
        nxt = ['Private room in Mission District','82','51027324','Pending','Private Room','1']
        self.assertEqual(csv_lines[1], nxt)

        # check that the last row is Apartment in Mission District,399,28668414,Pending,Entire Room,2
        last = ['Apartment in Mission District','399','28668414','Pending','Entire Room','2']
        self.assertEqual(csv_lines[-1], last)


    def test_check_policy_numbers(self):
        # call get_detailed_listing_database on "html_files/mission_district_search_results.html"
        # and save the result to a variable
        detailed_database = get_detailed_listing_database("html_files/mission_district_search_results.html")

        # call check_policy_numbers on the variable created above and save the result as a variable
        invalid_listings = check_policy_numbers(detailed_database)
        
        # check that the return value is a list
        self.assertEqual(type(invalid_listings), list)

        # check that there is exactly one element in the string
        self.assertEqual(len(invalid_listings),1)

        # check that the element in the list is a string
        self.assertEqual(type(invalid_listings[0]),str)

        # check that the first element in the list is '16204265'
        self.assertEqual(invalid_listings[0], '16204265')


if __name__ == '__main__':
    database = get_detailed_listing_database("html_files/mission_district_search_results.html")
    write_csv(database, "airbnb_dataset.csv")
    check_policy_numbers(database)
    unittest.main(verbosity=2)
