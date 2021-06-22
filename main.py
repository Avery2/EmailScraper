import os
import csv
import requests
import bs4
import re
import time
from validate_email import validate_email

# ==== CHANGE THESE AS NEEDED ====
# These are only for testing
num_tries = 0  # the number of google searches it will do, if 0, will go forever
doBingSearch = True
doGoogleSearch = True
verbosePrint = True

# this selects what column to add quotes around in the google search
# the columns corresond to the columns of the input csv.
# Note it is zero indexed, so the first row is 0, second row is 1, third row is 2
input_csv = 'input/TestCaseEmailScript.csv'
row_quote = 2

# delay between searches (to hopefully avoid bot)
delaySeconds = 0.01
# row to start from
rowStart = 1

# ==== PROBABLY LEAVE ALONE ====

runSecondaryEmailCheck = True
runSlowEmailCheck = False  # this doesn't actually work rn
# if True write newlines when no email found for a row
writeBlanks = True

# Initialize values
try_num = 0
GOOGLE_QUERY_URL = 'https://google.com/search?q='
# BING_QUERY_URL = 'https://www.bing.com/search?q='
BING_QUERY_URL = 'https://bing.com/search?q='


def findemailhelper(text="default text", queryurl=BING_QUERY_URL):
    # This function google searches the inputed text and returns all the text on the google search page

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }  # I want to add more headers but heed a header list

    url = queryurl + text.strip().replace(' ', '%20').replace('"', '%22')
    request_result = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(request_result.text,
                             "html.parser")
    txt = soup.get_text()

    # This print statement shows the raw text that is actually found for debugging (i.e. you have been flagged as a bot)
    # print(txt)

    return txt


def findemail(text="default text"):
    txt = ''
    if doBingSearch:
        txt += findemailhelper(text, BING_QUERY_URL)
    if doGoogleSearch:
        txt += findemailhelper(text, GOOGLE_QUERY_URL)

    botMessage = "This page checks to see if it's really you sending the requests, and not a robot."
    if len(re.findall(botMessage, txt)) > 0:
        print("\nWARNING: You may have been flagged as a bot. Uncomment `print(txt)` in the findemail() function to check.\n")

    # this is the regular expression that finds the email
    # myRegularExpression = "[^\s]+@[^\s]+\.[^\s]+"
    myRegularExpression = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
    return re.findall(myRegularExpression, txt)


# create a txt file to write the found emails to
current_time = time.strftime("h%H-m%M-s%S", time.localtime())
f = open(f"output/foundemails-{current_time}.csv", "a")

with open(input_csv, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for rowIndex, row in enumerate(spamreader):
        if rowIndex < rowStart:
            f.write(f"\n")
            continue

        # added delay to attempt to not be flagged as bot
        time.sleep(delaySeconds)

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
            if verbosePrint:
                print(f"{try_num} " + "---" * 9)
                print(f"query list: {row}")
                print(f"search query: {my_str}")
            foundTerms = findemail(my_str)  # runs search
            if verbosePrint:
                print(f"found terms: {foundTerms}")
            foundTermsFiltered = []
            for mail in foundTerms:
                is_valid_address = validate_email(email_address=mail, check_format=True, check_blacklist=False, check_dns=False, dns_timeout=10, check_smtp=False, smtp_timeout=10, smtp_helo_host=None, smtp_from_address=None, smtp_debug=False)
                if verbosePrint:
                    print(f"{is_valid_address} : {mail}")
                if runSecondaryEmailCheck:
                    if is_valid_address:
                        foundTermsFiltered.append(mail)
                    if runSlowEmailCheck:
                        is_valid = validate_email(email_address=mail, check_format=True, check_blacklist=True, check_dns=False, dns_timeout=10, check_smtp=True, smtp_timeout=10, smtp_helo_host=None, smtp_from_address=None, smtp_debug=True)
                        if verbosePrint:
                            print(f"{is_valid} : {mail}")
                else:
                    foundTermsFiltered.append(mail)

            foundTermsFiltered = list(set(foundTermsFiltered))  # remove duplicates

            if verbosePrint:
                print(f"valid emails: {foundTermsFiltered}")
                f.write(f"{', '.join(foundTermsFiltered)}\n")
                print("---" * 10 + "\n")
            # if writeBlanks:
                #     f.write(f"{', '.join(foundTermsFiltered)}\n")  # writes to file
                # elif foundTermsFiltered:
                #     f.write(f"{', '.join(foundTermsFiltered)}\n")  # writes to file

            # logic to limit number of searches for testing
            try_num += 1
            # remove this line if you don't want to limit how many searches you do
            if num_tries == 0:
                pass
            elif try_num >= num_tries:
                break

csvfile.close()
f.close()

with open(input_csv, 'r') as f1, open(f"output/foundemails-{current_time}.csv", 'r') as f2, open(f"output/foundemails-combined-{current_time}.csv", 'w') as w:
    writer = csv.writer(w)
    r1, r2 = csv.reader(f1), csv.reader(f2)
    while True:
        try:
            writer.writerow(next(r1)+next(r2))
        except StopIteration:
            break

f1.close()
f2.close()
w.close()
