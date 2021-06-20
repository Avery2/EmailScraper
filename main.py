# import os
# from googleapi import google

# Import the beautifulsoup
# and request libraries of python.
import csv
import requests
import bs4
import re
import time


def findemail(text):
    # text = "Iain	Donnison 'Aberystwyth University' UK email"
    url = 'https://google.com/search?q=' + text
    request_result = requests.get(url)
    soup = bs4.BeautifulSoup(request_result.text,
                             "html.parser")
    # print(soup.get_text())

    # soup.find.all( h3 ) to grab
    # all major headings of our search result,
    # heading_object = soup.find_all('h3')

    # Iterate through the object
    # and print it as a string.
    # for info in heading_object:
    #     print(info.getText())
    #     print("------")

    txt = soup.get_text()
    # x = re.findall("isd@aber.ac.uk", txt)
    # print(x)
    # print(txt)

    # print()
    # print("---"*10)
    # print()

    # x = re.findall("\s.+@.+\..+\s", txt)
    x = re.findall("[^\s]+@[^\s]+\.[^\s]+", txt)
    # print(x)
    # for e in x:
    #     print(e)
    #     print()
    return x


f = open("demofile2.txt", "a")
num_tries = 2
try_num = 0

row_quote = 2
with open('TestCaseEmailScript.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    # print(spamreader)
    for row in spamreader:
        time.sleep(1.5)

        foo = ' '.join(row).replace(',', ' ').strip()
        if foo != '':
            for i, elem in enumerate(row):
                row[i] = elem.replace(',', ' ')
            # here no blanks
            # print(row[0] + " " + row[1])
            my_str = ''
            for i, elem in enumerate(row):
                if i == row_quote:
                    my_str += "\"" + elem + "\""
                else:
                    my_str += " " + elem
            my_str += " email"
            print("---" * 10)
            print(row)
            print(my_str)
            print(findemail(my_str))
            print("---" * 10)
            print()
            try_num += 1
            if try_num >= num_tries:
                break


# foo = ''
# for word in row:
#     foo += " " + word.replace(',', ' ')
# if foo.strip():
#     print(foo)
#     # print(findemail(foo))
#     # print()
#     print("---"*10)
#     # print()
# print(row.split(""))
# print(', '.join(row))
