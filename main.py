import os
import csv
import requests
import bs4
import re
import time
from validate_email import validate_email
import random

# ==== GENERAL ====
START_ROW = 1
NUM_SEARCH = 5  # the number of google searches it will do, if 0, will go forever
DO_BING_SEARCH = True
DO_GOOGLE_SEARCH = False
INPUT_CSV = 'input/TestCaseEmailScript.csv'
DELAY_SECONDS = 0.01

# ==== OPTIONS ====
QUOTE_EACH_WORD = True  # if False quotes none
EMAIL_NEEDS_NAME = True  # filters emails so they must contain some part of the person's name

# ==== PROBABLY LEAVE ALONE ====
SECONDARY_EMAIL_CHECK = True
SLOW_EMAIL_CHECK = False  # this doesn't actually work rn

# ==== INITIALIZE VALUES ====
GOOGLE_QUERY_URL = 'https://google.com/search?q='
BING_QUERY_URL = 'https://bing.com/search?q='
GOOGLE_BOT_MESSAGE = "This page checks to see if it's really you sending the requests, and not a robot."
START_TIME = time.strftime("%A-%H-%M-%S", time.localtime())
OUTPUT_PATH = f"output/{START_TIME}/"
QUERY_FILENAME = f"emails-{START_TIME}.csv"
COMBINED_FILENAME = f"combined-emails-{START_TIME}.csv"
AGENT_LIST = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/43.4',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
]


class PrintColors:

    BLACK = "\u001b[30m"
    RED = "\u001b[31m"
    GREEN = "\u001b[32m"
    YELLOW = "\u001b[33m"
    BLUE = "\u001b[34m"
    MAGENTA = "\u001b[35m"
    CYAN = "\u001b[36m"
    WHITE = "\u001b[37m"
    RESET = "\u001b[0m"
    BOLD = "\u001b[1m"
    UNDERLINE = "\u001b[4m"
    REVERSED = "\u001b[7m"

    def reset(self):
        print(self.RESET, end='')

    def toggleRed(self):
        print(self.GREEN, end='')

    def toggleGreen(self):
        print(self.GREEN, end='')


def getQueryText(text="default text", queryurl=BING_QUERY_URL):
    headers = {
        'user-agent': AGENT_LIST[random.randint(0, len(AGENT_LIST)-1)],
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
        print(f"\n{PrintColors.RED}WARNING: You may have been flagged as a bot (by Google). Uncomment `print(txt)` in the findemail() function to check.{PrintColors.RESET}\n")

    myRegularExpression = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
    foundTerms = re.findall(myRegularExpression, txt)
    return filterFoundTerms(foundTerms)


def rowToQueries(row):
    for i, elem in enumerate(row):
        row[i] = elem.replace(',', ' ').strip()
    row.append("email")
    row = [e for e in row if e]
    queries = []

    # no quotes
    query = ''
    for j, elem in enumerate(row):
        query += f" {elem}"
    queries.append(query.strip())

    # quotes each word
    if QUOTE_EACH_WORD:
        for i, foo in enumerate(row):
            query = ''
            for j, elem in enumerate(row):
                if QUOTE_EACH_WORD and i == j:
                    # query += " \"" + elem + "\""
                    query += f" \"{elem}\""
                else:
                    query += f" {elem}"
            queries.append(query.strip())

    return queries


def filterFoundTerms(foundTerms):
    foundTermsFiltered = []
    foundTerms = list(set(foundTerms))
    # Secondary checks
    for mail in foundTerms:
        checks = []
        # if False:
        #     checks.append(False)
        if SECONDARY_EMAIL_CHECK:
            checks.append(validate_email(email_address=mail, check_format=True, check_blacklist=False, check_dns=False, dns_timeout=10, check_smtp=False, smtp_timeout=10, smtp_helo_host=None, smtp_from_address=None, smtp_debug=False))

        passAllChecks = all(checks)
        if passAllChecks:
            foundTermsFiltered.append(mail)
        print(f"{PrintColors.GREEN}{passAllChecks}{PrintColors.RESET}  : {mail}") if passAllChecks else print(f"{PrintColors.RED}{passAllChecks}{PrintColors.RESET} : {mail}")

    if foundTermsFiltered == []:
        print(f"{PrintColors.RED}Warning: No valid emails found.{PrintColors.RESET}")

    return foundTermsFiltered


def runSearch():
    f = open(OUTPUT_PATH+QUERY_FILENAME, "a")
    queryNum = 0
    foundEmails = 0

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
            print(f"{PrintColors.BOLD}{queryNum}{PrintColors.RESET} " + f"\n{PrintColors.BOLD}query list:{PrintColors.RESET} {row}\n{PrintColors.BOLD}search query(s):{PrintColors.RESET} {queryTerms}")
            validEmails = findemail(queryTerms)
            print(f"{PrintColors.BOLD}valid emails:{PrintColors.RESET} {len(validEmails)}\n" + "\n")
            foundEmails += len(validEmails)
            f.write(f"{', '.join(validEmails)}\n")
            queryNum += 1
            if NUM_SEARCH != 0 and queryNum >= NUM_SEARCH:
                break

    csvfile.close()
    f.close()
    return foundEmails


def createCombinedCSV(prefix=''):
    # csv output: write a new combined csv
    with open(INPUT_CSV, 'r') as f1, open(OUTPUT_PATH+QUERY_FILENAME, 'r') as f2, open(OUTPUT_PATH+prefix+COMBINED_FILENAME, 'w') as w:
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
    os.mkdir(OUTPUT_PATH)
    foundEmails = runSearch()
    print(f"Found {PrintColors.BOLD}{foundEmails}{PrintColors.RESET} emails.")
    createCombinedCSV(f"{foundEmails}_")
    print(f"Output in {PrintColors.BOLD}./{OUTPUT_PATH+QUERY_FILENAME}{PrintColors.RESET} and {PrintColors.BOLD}./{OUTPUT_PATH+COMBINED_FILENAME}{PrintColors.RESET}")


if __name__ == "__main__":
    main()
