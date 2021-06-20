# import os
# from googleapi import google

# print("hello world")

# num_page = 3
# search_results = google.search("This is my query", num_page)

# print(type(search_results))
# print(search_results)

# google.calculate("157.3kg in grams")


# Import the beautifulsoup
# and request libraries of python.
import csv
import requests
import bs4
import re

# Make two strings with default google search URL
# 'https://google.com/search?q=' and
# our customized search keyword.
# Concatenate them
text = "Iain	Donnison 'Aberystwyth University' UK email"
url = 'https://google.com/search?q=' + text

# Fetch the URL data using requests.get(url),
# store it in a variable, request_result.
request_result = requests.get(url)

# Creating soup from the fetched request
soup = bs4.BeautifulSoup(request_result.text,
                         "html.parser")
# print(soup)
# print(type(soup))
# print(soup.prettify)
# print(type(soup.get_text()))

# print(soup.get_text())


# soup.find.all( h3 ) to grab
# all major headings of our search result,
heading_object = soup.find_all('h3')

# Iterate through the object
# and print it as a string.
# for info in heading_object:
#     print(info.getText())
#     print("------")

txt = soup.get_text()
# x = re.findall("isd@aber.ac.uk", txt)
# print(x)

print()
print("---"*10)
print()

# x = re.findall("\s.+@.+\..+\s", txt)
x = re.findall("[^\s]+@[^\s]+\.[^\s]+", txt)
# print(x)
# for e in x:
#     print(e)
#     print()

with open('TestCaseEmailScript.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    # print(spamreader)
    for row in spamreader:
        # print(', '.join(row))
        if any(row):
            print(row)
