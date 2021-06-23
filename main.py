import os
import csv
import requests
import bs4
import re
import time
from validate_email import validate_email

# ==== CHANGE THESE AS NEEDED ====
# the number of google searches it will do, if 0, will go forever
NUM_SEARCH = 5
DO_BING_SEARCH = True
DO_GOOGLE_SEARCH = False
INPUT_CSV = 'input/TestCaseEmailScript.csv'
# Selects column/term to quote. The columns correspond to the columns of the input csv. (zero indexed)
QUOTE_EACH_WORD = True
# delay between searches (to hopefully avoid bot)
DELAY_SECONDS = 0.01
# row to start from
START_ROW = 1

# ==== PROBABLY LEAVE ALONE ====
# Run additional checks on emails
SECONDARY_EMAIL_CHECK = True
SLOW_EMAIL_CHECK = False  # this doesn't actually work rn

# ==== INITIALIZE VALUES ====
GOOGLE_QUERY_URL = 'https://google.com/search?q='
BING_QUERY_URL = 'https://bing.com/search?q='
GOOGLE_BOT_MESSAGE = "This page checks to see if it's really you sending the requests, and not a robot."
current_time = time.strftime("h%Hm%Ms%S", time.localtime())
queryFilename = f"output/foundemails-{current_time}.csv"
combinedFilename = f"output/foundemails-combined-{current_time}.csv"


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


def findemail(terms=["default text"]):
    txt = ''
    for term in terms:
        if DO_BING_SEARCH:
            txt += getQueryText(term, BING_QUERY_URL)
        if DO_GOOGLE_SEARCH:
            txt += getQueryText(term, GOOGLE_QUERY_URL)
    if len(re.findall(GOOGLE_BOT_MESSAGE, txt)) > 0:
        print("\nWARNING: You may have been flagged as a bot (by Google). Uncomment `print(txt)` in the findemail() function to check.\n")

    myRegularExpression = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
    foundTerms = re.findall(myRegularExpression, txt)
    return filterFoundTerms(foundTerms)


def rowToQueries(row):
    for i, elem in enumerate(row):
        row[i] = elem.replace(',', ' ').strip()

    queries = []
    for i, foo in enumerate(row):
        query = ''
        for j, elem in enumerate(row):
            if QUOTE_EACH_WORD and i == j:
                query += " \"" + elem + "\""
            else:
                query += " " + elem
        query += "email"
        queries.append(query)
        if not QUOTE_EACH_WORD:
            break

    return queries


def filterFoundTerms(foundTerms):
    foundTermsFiltered = []

    # Secondary checks
    if SECONDARY_EMAIL_CHECK:
        for mail in foundTerms:
            is_valid_address = validate_email(email_address=mail, check_format=True, check_blacklist=False, check_dns=False, dns_timeout=10, check_smtp=False, smtp_timeout=10, smtp_helo_host=None, smtp_from_address=None, smtp_debug=False)
            print(f"{is_valid_address} : {mail}")
            if is_valid_address:
                foundTermsFiltered.append(mail)
            if SLOW_EMAIL_CHECK:
                is_valid = validate_email(email_address=mail, check_format=True, check_blacklist=True, check_dns=False, dns_timeout=10, check_smtp=True, smtp_timeout=10, smtp_helo_host=None, smtp_from_address=None, smtp_debug=True)
                print(f"{is_valid} : {mail}")
            else:
                foundTermsFiltered.append(mail)

    # Remove duplicates
    foundTermsFiltered = list(set(foundTermsFiltered))

    return foundTermsFiltered


def runSearch():
    f = open(queryFilename, "a")
    queryNum = 0

    # csv output: do search and write to a csv
    with open(INPUT_CSV, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        # iterate through rows of CSV
        for rowIndex, row in enumerate(spamreader):
            if rowIndex < START_ROW:
                f.write(f"\n")
                continue
            if ' '.join(row).replace(',', ' ').strip() == '':  # empty row check
                continue
            time.sleep(DELAY_SECONDS)
            queryTerms = rowToQueries(row)
            print(f"{queryNum} " + "---" * 9 + f"\nquery list: {row}\nsearch query(s): {queryTerms}")
            validEmails = findemail(queryTerms)
            print(f"valid emails: {validEmails}" + "---" * 10 + "\n")
            f.write(f"{', '.join(validEmails)}\n")
            queryNum += 1
            if NUM_SEARCH != 0 and queryNum >= NUM_SEARCH:
                break

    csvfile.close()
    f.close()


def createCombinedCSV():
    # csv output: write a new combined csv
    with open(INPUT_CSV, 'r') as f1, open(queryFilename, 'r') as f2, open(combinedFilename, 'w') as w:
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


def main():
    print("Starting Search...")
    runSearch()
    createCombinedCSV()
    print(f"Done.\nOutput in ./{queryFilename} and ./{combinedFilename}")


if __name__ == "__main__":
    main()
