import os
import csv
import requests
import bs4
import re
import time
from validate_email import validate_email
import random
import sys
import getopt


# ==== GENERAL ====
startRow = 1
numSearch = 5
inputFile = 'input/TestCaseEmailScript.csv'
doBingSearch = True
doGoogleSearch = False
delaySeconds = 0

# ==== OPTIONS ====
quoteEachWord = True
createCombined = True
disableColors = False

# ==== PRIMARY FILTERS ====
doPrimaryEmailCheck = True
# SLOW_EMAIL_CHECK = False  # this doesn't actually work rn

# ==== SECONDARY FILTERS ====
applySecondaryFilters = True

# ==== DEBUGGING ====
sortOutput = True
showText = False
makeLowercase = True

globalOptionNames = ['startRow',
                     'numSearch',
                     'inputFile',
                     'doBingSearch',
                     'doGoogleSearch',
                     'delaySeconds',
                     'quoteEachWord',
                     'createCombined',
                     'disableColors',
                     'doPrimaryEmailCheck',
                     'applySecondaryFilters',
                     'sortOutput',
                     'showText',
                     'makeLowercase']

globalOptions = {globalOptionNames[0]: startRow,
                 globalOptionNames[1]: numSearch,
                 globalOptionNames[2]: inputFile,
                 globalOptionNames[3]: doBingSearch,
                 globalOptionNames[4]: doGoogleSearch,
                 globalOptionNames[5]: delaySeconds,
                 globalOptionNames[6]: quoteEachWord,
                 globalOptionNames[7]: createCombined,
                 globalOptionNames[8]: disableColors,
                 globalOptionNames[9]: doPrimaryEmailCheck,
                 globalOptionNames[10]: applySecondaryFilters,
                 globalOptionNames[11]: sortOutput,
                 globalOptionNames[12]: showText,
                 globalOptionNames[13]: makeLowercase}

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
    global globalOptions
    BLACK = "\u001b[30m" if not globalOptions['disableColors'] else ''
    RED = "\u001b[31m" if not globalOptions['disableColors'] else ''
    GREEN = "\u001b[32m" if not globalOptions['disableColors'] else ''
    YELLOW = "\u001b[33m" if not globalOptions['disableColors'] else ''
    BLUE = "\u001b[34m" if not globalOptions['disableColors'] else ''
    MAGENTA = "\u001b[35m" if not globalOptions['disableColors'] else ''
    CYAN = "\u001b[36m" if not globalOptions['disableColors'] else ''
    WHITE = "\u001b[37m" if not globalOptions['disableColors'] else ''
    RESET = "\u001b[0m" if not globalOptions['disableColors'] else ''
    BOLD = "\u001b[1m" if not globalOptions['disableColors'] else ''
    UNDERLINE = "\u001b[4m" if not globalOptions['disableColors'] else ''
    REVERSED = "\u001b[7m" if not globalOptions['disableColors'] else ''

    def reset(self):
        print(self.RESET, end='')

    def toggleRed(self):
        print(self.GREEN, end='')

    def toggleGreen(self):
        print(self.GREEN, end='')


def runSearch():
    global globalOptions

    def doSearch(terms=["default text"]):
        def getQueryText(text="default text", queryurl=BING_QUERY_URL):
            headers = {
                'user-agent': AGENT_LIST[random.randint(0, len(AGENT_LIST)-1)],
            }
            url = queryurl + text.strip().replace(' ', '%20').replace('"', '%22')
            request_result = requests.get(url, headers=headers)
            soup = bs4.BeautifulSoup(request_result.text,
                                     "html.parser")
            txt = soup.get_text()
            if globalOptions['showText']:
                print(txt)
            return txt

        def filterFoundTerms(foundTerms):
            foundTermsFiltered = []
            if globalOptions['makeLowercase']:
                foundTerms = [e.lower() for e in foundTerms]  # to lowercase
            foundTerms = list(set(foundTerms))
            if globalOptions['sortOutput']:
                foundTerms.sort()
            for mail in foundTerms:
                checks = []
                # PRIMARY FILTERS HERE
                # if False:
                #     checks.append(False)
                if globalOptions['doPrimaryEmailCheck']:
                    checks.append(validate_email(email_address=mail, check_format=True, check_blacklist=False, check_dns=False, dns_timeout=10, check_smtp=False, smtp_timeout=10, smtp_helo_host=None, smtp_from_address=None, smtp_debug=False))

                passAllChecks = all(checks)
                if passAllChecks:
                    foundTermsFiltered.append(mail)
                print(f"{PrintColors.GREEN}{passAllChecks}{PrintColors.RESET}  : {mail}") if passAllChecks else print(f"{PrintColors.RED}{passAllChecks}{PrintColors.RESET} : {mail}")

            if foundTermsFiltered == []:
                print(f"{PrintColors.RED}Warning: No valid emails found.{PrintColors.RESET}")

            return foundTermsFiltered

        txt = ''
        for term in terms:
            if globalOptions['doBingSearch']:
                txt += getQueryText(term, BING_QUERY_URL)
            if globalOptions['doGoogleSearch']:
                txt += getQueryText(term, GOOGLE_QUERY_URL)
        if len(re.findall(GOOGLE_BOT_MESSAGE, txt)) > 0:
            print(f"\n{PrintColors.RED}WARNING: You may have been flagged as a bot (by Google). Uncomment `print(txt)` in the findemail() function to check.{PrintColors.RESET}\n")

        myRegularExpression = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
        foundTerms = re.findall(myRegularExpression, txt)
        return filterFoundTerms(foundTerms)

    def rowToQueries(row):
        queries = []

        # no quotes
        query = ''
        for j, elem in enumerate(row):
            query += f" {elem}"
        queries.append(query.strip())

        # quotes each word
        if globalOptions['quoteEachWord']:
            for i, foo in enumerate(row):
                query = ''
                for j, elem in enumerate(row):
                    if globalOptions['quoteEachWord'] and i == j:
                        # query += " \"" + elem + "\""
                        query += f" \"{elem}\""
                    else:
                        query += f" {elem}"
                queries.append(query.strip())

        return queries

    f = open(OUTPUT_PATH+QUERY_FILENAME, "a")
    queryNum = 0
    numFoundEmails = 0

    # csv output: do search and write to a csv
    with open(globalOptions['inputFile'], newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        # iterate through rows of CSV
        for rowIndex, row in enumerate(spamreader):
            if rowIndex < startRow:
                f.write(f"\n")
                continue
            if ' '.join(row).replace(',', ' ').strip() == '':  # empty row check
                continue
            time.sleep(globalOptions['delaySeconds'])

            for i, elem in enumerate(row):
                row[i] = elem.replace(',', ' ').strip()
            row.append("email")
            row = [e for e in row if e]

            queryTerms = rowToQueries(row)
            print(f"{PrintColors.BOLD}{queryNum}{PrintColors.RESET} " + f"\n{PrintColors.BOLD}query list:{PrintColors.RESET} {row}\n{PrintColors.BOLD}search query(s):{PrintColors.RESET} {queryTerms}")
            validEmails = doSearch(queryTerms)
            print(f"{PrintColors.BOLD}valid emails:{PrintColors.RESET} {len(validEmails)}\n" + "\n")
            numFoundEmails += len(validEmails)
            f.write(f"{', '.join(validEmails)}\n")
            queryNum += 1
            if numSearch != 0 and queryNum >= numSearch:
                break

    csvfile.close()
    f.close()
    return numFoundEmails


def createCombinedCSV(prefix=''):
    # csv output: write a new combined csv
    with open(globalOptions['inputFile'], 'r') as f1, open(OUTPUT_PATH+QUERY_FILENAME, 'r') as f2, open(OUTPUT_PATH+prefix+COMBINED_FILENAME, 'w') as w:
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


def createFilteredCSV(prefix=''):
    # SECONDARY FILTERS that apply to a new csv

    def applySecondaryFilters(inputRows, foundEmails):
        # NOTES
        # This function takes in two lists of strings: "inputRows" and "foundEmails"
        # You can filter the "foundEmails" list here

        print(f"{PrintColors.BOLD}input:{PrintColors.RESET}  {inputRows}")
        print(f"{PrintColors.BOLD}emails: {len(foundEmails)}:{PrintColors.RESET} {foundEmails}")

        numBefore = len(foundEmails)

        # === START FILTER LOGIC ===

        def filterNoSharedChar(emails):
            # print(f"{PrintColors.BOLD}Use as filter:{PrintColors.RESET} {inputRows[0:2]}")
            setInput = set(''.join(inputRows[0:2]))
            for index, email in enumerate(emails):
                setEmail = set(email)
                hasCommonChar = setInput & setEmail
                if not hasCommonChar:
                    emails[index] = None
            emails = list(filter(None, emails))
            return emails

        def filterName(emails):
            copy = []
            firstName, lastName = [e.lower() for e in inputRows[0:2]]
            for email in emails:
                if firstName in email:
                    copy.append(email)
                elif lastName in email:
                    copy.append(email)
                elif firstName[0] in email and lastName[0] in email:
                    copy.append(email)
            return copy

        # Call filtering function
        foundEmails = filterNoSharedChar(foundEmails)
        foundEmails = filterName(foundEmails)

        # === END FILTER LOGIC ===

        numAfter = len(foundEmails)

        # Remove any elements in list with the value: None
        foundEmails = list(filter(None, foundEmails))

        print(f"{PrintColors.BOLD}Filtered Emails: {len(foundEmails)}:{PrintColors.RESET} {foundEmails}")
        print(f"Filtered out {PrintColors.RED}0{PrintColors.RESET} emails.") if numBefore - numAfter == 0 else print(f"Filtered out {PrintColors.BOLD}{numBefore - numAfter}{PrintColors.RESET} emails.\n")
        return inputRows, foundEmails

    with open(globalOptions['inputFile'], 'r') as f1, open(OUTPUT_PATH+QUERY_FILENAME, 'r') as f2, open(OUTPUT_PATH+prefix+COMBINED_FILENAME, 'w') as w:
        writer = csv.writer(w)
        r1, r2 = csv.reader(f1), csv.reader(f2)
        while True:
            try:
                nr1, nr2 = applySecondaryFilters(next(r1), next(r2))
                writer.writerow(nr1+nr2)
            except StopIteration:
                break
    f1.close()
    f2.close()
    w.close()


def main(argv):
    global globalOptions
    longOpts = [f'{e}=' for e in globalOptionNames].copy()
    longOpts.append('help')

    try:
        opts, args = getopt.getopt(argv, shortopts='h', longopts=longOpts)
    except getopt.GetoptError:
        print(f"{PrintColors.RED}Invalid options.{PrintColors.RESET} Usage:")
        print('main.py ' + '=<value> '.join([f'--{e}' for e in globalOptionNames]))
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('main.py ' + '=<value> '.join([f'--{e}' for e in globalOptionNames]))
            sys.exit()
        elif opt in [f'--{e}' for e in globalOptionNames]:
            try:
                globalOptions[opt[2:]] = int(arg)
            except ValueError:
                globalOptions[opt[2:]] = arg

    print(globalOptions)

    print("Starting Search...")
    os.mkdir(OUTPUT_PATH)
    numFoundEmails = runSearch()
    print(f"Found {PrintColors.BOLD}{numFoundEmails}{PrintColors.RESET} emails.\n")
    print("Applying secondary filters...")
    if globalOptions['applySecondaryFilters']:
        createFilteredCSV(f"{numFoundEmails}-filtered_")
    if globalOptions['createCombined']:
        createCombinedCSV(f"{numFoundEmails}_")
    outputMsg = f"Output in {PrintColors.BOLD}./{OUTPUT_PATH}{PrintColors.RESET}"
    print(outputMsg)
    return outputMsg


if __name__ == "__main__":
    main(sys.argv[1:])
