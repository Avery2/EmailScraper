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

input_csv = 'input/TestCaseEmailScript.csv'
row_quote = 2  # Selects column/term to quote. The columns correspond to the columns of the input csv. (zero indexed)

# delay between searches (to hopefully avoid bot)
delaySeconds = 0.01
# row to start from
rowStart = 1

# ==== PROBABLY LEAVE ALONE ====

runSecondaryEmailCheck = True
runSlowEmailCheck = False  # this doesn't actually work rn

# Initialize values
try_num = 0
GOOGLE_QUERY_URL = 'https://google.com/search?q='
BING_QUERY_URL = 'https://bing.com/search?q='
GOOGLE_BOT_MESSAGE = "This page checks to see if it's really you sending the requests, and not a robot."


def getQueryText(text="default text", queryurl=BING_QUERY_URL):
    headers = {  # This helps being not marked as bot see https://pknerd.medium.com/5-strategies-to-write-unblock-able-web-scrapers-in-python-5e40c147bdaf for more
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }
    url = queryurl + text.strip().replace(' ', '%20').replace('"', '%22')
    request_result = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(request_result.text,
                             "html.parser")
    txt = soup.get_text()

    # print(txt)
    return txt


def findemail(text="default text"):
    txt = ''
    if doBingSearch:
        txt += getQueryText(text, BING_QUERY_URL)
    if doGoogleSearch:
        txt += getQueryText(text, GOOGLE_QUERY_URL)
    if len(re.findall(GOOGLE_BOT_MESSAGE, txt)) > 0:
        print("\nWARNING: You may have been flagged as a bot (by Google). Uncomment `print(txt)` in the findemail() function to check.\n")

    # myRegularExpression = "[^\s]+@[^\s]+\.[^\s]+"
    myRegularExpression = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
    return re.findall(myRegularExpression, txt)


def rowToStr(row):
    my_str = ''
    for i, elem in enumerate(row):
        row[i] = elem.replace(',', ' ')
    for i, elem in enumerate(row):
        if i == row_quote:
            my_str += " \"" + elem + "\""
        else:
            my_str += " " + elem
    my_str += " email"
    return my_str


def filterFoundTerms(foundTerms):
    foundTermsFiltered = []
    for mail in foundTerms:
        is_valid_address = validate_email(email_address=mail, check_format=True, check_blacklist=False, check_dns=False, dns_timeout=10, check_smtp=False, smtp_timeout=10, smtp_helo_host=None, smtp_from_address=None, smtp_debug=False)
        print(f"{is_valid_address} : {mail}")
        if runSecondaryEmailCheck:
            if is_valid_address:
                foundTermsFiltered.append(mail)
            if runSlowEmailCheck:
                is_valid = validate_email(email_address=mail, check_format=True, check_blacklist=True, check_dns=False, dns_timeout=10, check_smtp=True, smtp_timeout=10, smtp_helo_host=None, smtp_from_address=None, smtp_debug=True)
                print(f"{is_valid} : {mail}")
        else:
            foundTermsFiltered.append(mail)

    foundTermsFiltered = list(set(foundTermsFiltered))  # remove duplicates
    return foundTermsFiltered


current_time = time.strftime("h%H-m%M-s%S", time.localtime())
f = open(f"output/foundemails-{current_time}.csv", "a")

# output: do search and write to a csv
with open(input_csv, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    # iterate through rows of CSV
    for rowIndex, row in enumerate(spamreader):
        if rowIndex < rowStart:
            f.write(f"\n")
            continue
        time.sleep(delaySeconds)
        isNotEmptyRow = ' '.join(row).replace(',', ' ').strip() != ''
        if isNotEmptyRow:
            searchTerm = rowToStr(row)
            print(f"{try_num} " + "---" * 9)
            print(f"query list: {row}")
            print(f"search query: {searchTerm}")
            foundTerms = findemail(searchTerm)
            print(f"found terms: {foundTerms}")
            foundTerms = filterFoundTerms(foundTerms)
            print(f"valid emails: {foundTerms}")
            f.write(f"{', '.join(foundTerms)}\n")
            print("---" * 10 + "\n")
            try_num += 1
            if num_tries == 0:
                pass
            elif try_num >= num_tries:
                break

# output: write a new combined csv
with open(input_csv, 'r') as f1, open(f"output/foundemails-{current_time}.csv", 'r') as f2, open(f"output/foundemails-combined-{current_time}.csv", 'w') as w:
    writer = csv.writer(w)
    r1, r2 = csv.reader(f1), csv.reader(f2)
    while True:
        try:
            writer.writerow(next(r1)+next(r2))
        except StopIteration:
            break

csvfile.close()
f.close()
f1.close()
f2.close()
w.close()
