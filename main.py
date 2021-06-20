import os
import csv
import requests
import bs4
import re
import time


def findemail(text="default text"):
    # This function google searches the inputed text and returns all the text on the google search page

    url = 'https://google.com/search?q=' + text
    request_result = requests.get(url)
    soup = bs4.BeautifulSoup(request_result.text,
                             "html.parser")
    txt = soup.get_text()

    # This print statement shows the raw text that is actually found for debugging (i.e. you have been flagged as a bot)
    # print(txt)
    botMessage = "This page checks to see if it's really you sending the requests, and not a robot."
    if len(re.findall(botMessage, txt)) > 0:
        print("\nWARNING: You may have been flagged as a bot. Uncomment `print(txt)` in the findemail() function to check\n")

    # this is the regular expression that finds the email
    # myRegularExpression = "[^\s]+@[^\s]+\.[^\s]+"
    myRegularExpression = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
    return re.findall(myRegularExpression, txt)


# create a txt file to write the found emails to
current_time = time.strftime("h%H-m%M-s%S", time.localtime())
f = open(f"foundemails-{current_time}.csv", "a")

# These are only for testing
num_tries = 5  # the number of google searches it will do
try_num = 0

# this selects what column to add quotes around in the google search
# the columns corresond to the columns of the input csv.
# Note it is zero indexed, so the first row is 0, second row is 1, third row is 2
row_quote = 2
input_csv = 'TestCaseEmailScript.csv'

with open(input_csv, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        # added delay to attempt to not be flagged as bot
        time.sleep(1.5)

        # this unreadable logic is to ignore empty rows read in by the csv reader
        ignore_empty = ' '.join(row).replace(',', ' ').strip()
        if ignore_empty != '':
            # here, the row variable is now a list of the current row of the csv where each element is one cell

            # change row into a string to search
            my_str = ''
            for i, elem in enumerate(row):
                row[i] = elem.replace(',', ' ')
            for i, elem in enumerate(row):
                if i == row_quote:
                    my_str += " \"" + elem + "\""
                else:
                    my_str += " " + elem
            my_str += " email"

            # output
            print(f"{try_num} " + "---" * 9)
            print(f"query list: {row}")
            print(f"search query: {my_str}")
            foundTerms = findemail(my_str)  # runs search
            if foundTerms:
                f.write(f"{', '.join(foundTerms)}\n")  # writes to file
            print(f"found terms: {foundTerms}")
            print("---" * 10)
            print()

            # logic to limit number of searches for testing
            try_num += 1
            if try_num >= num_tries:
                break

f.close()
