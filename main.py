import os
import csv
import requests
from bs4 import BeautifulSoup, SoupStrainer
import re
import time
from validate_email import validate_email
import random
import sys
import getopt
import my_globals
import signal

GOOGLE_QUERY_URL = 'https://google.com/search?q='
BING_QUERY_URL = 'https://bing.com/search?q='
GOOGLE_BOT_MESSAGE = "This page checks to see if it's really you sending the requests, and not a robot."
AGENT_LIST = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/43.4',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
]
BLACKLIST = ["tripadvisor.com", "go.microsoft.com", "maps.apple.com", "pdf$"]


class PrintColors:
    my_globals.initialize()
    black = "\u001b[30m" if not my_globals.options['disableColors'] else ''
    red = "\u001b[31m" if not my_globals.options['disableColors'] else ''
    green = "\u001b[32m" if not my_globals.options['disableColors'] else ''
    yellow = "\u001b[33m" if not my_globals.options['disableColors'] else ''
    blue = "\u001b[34m" if not my_globals.options['disableColors'] else ''
    magenta = "\u001b[35m" if not my_globals.options['disableColors'] else ''
    cyan = "\u001b[36m" if not my_globals.options['disableColors'] else ''
    white = "\u001b[37m" if not my_globals.options['disableColors'] else ''
    reset = "\u001b[0m" if not my_globals.options['disableColors'] else ''
    bold = "\u001b[1m" if not my_globals.options['disableColors'] else ''
    underline = "\u001b[4m" if not my_globals.options['disableColors'] else ''
    reverse = "\u001b[7m" if not my_globals.options['disableColors'] else ''

    def update():
        PrintColors.black = "\u001b[30m" if not my_globals.options['disableColors'] else ''
        PrintColors.red = "\u001b[31m" if not my_globals.options['disableColors'] else ''
        PrintColors.green = "\u001b[32m" if not my_globals.options['disableColors'] else ''
        PrintColors.yellow = "\u001b[33m" if not my_globals.options['disableColors'] else ''
        PrintColors.blue = "\u001b[34m" if not my_globals.options['disableColors'] else ''
        PrintColors.magenta = "\u001b[35m" if not my_globals.options['disableColors'] else ''
        PrintColors.cyan = "\u001b[36m" if not my_globals.options['disableColors'] else ''
        PrintColors.white = "\u001b[37m" if not my_globals.options['disableColors'] else ''
        PrintColors.reset = "\u001b[0m" if not my_globals.options['disableColors'] else ''
        PrintColors.bold = "\u001b[1m" if not my_globals.options['disableColors'] else ''
        PrintColors.underline = "\u001b[4m" if not my_globals.options['disableColors'] else ''
        PrintColors.reverse = "\u001b[7m" if not my_globals.options['disableColors'] else ''

    def setBlack():
        print(PrintColors.black, end='')

    def setRed():
        print(PrintColors.red, end='')

    def setGreen():
        print(PrintColors.green, end='')

    def setYellow():
        print(PrintColors.yellow, end='')

    def setBlue():
        print(PrintColors.blue, end='')

    def setMagenta():
        print(PrintColors.magenta, end='')

    def setCyan():
        print(PrintColors.cyan, end='')

    def setWhite():
        print(PrintColors.white, end='')

    def setReset():
        print(PrintColors.reset, end='')

    def setBold():
        print(PrintColors.bold, end='')

    def setUnderline():
        print(PrintColors.underline, end='')

    def setReverse():
        print(PrintColors.reverse, end='')


class EmailBot:
    startTime = time.strftime("%A-%H-%M-%S", time.localtime())
    outputPath = f"output/{startTime}/"
    queryFilename = f"emails-{startTime}.csv"
    combinedFilename = f"combined-emails-{startTime}.csv"

    def update():
        EmailBot.startTime = time.strftime("%A-%H-%M-%S", time.localtime())
        EmailBot.outputPath = f"output/{EmailBot.startTime}/"
        EmailBot.queryFilename = f"emails-{EmailBot.startTime}.csv"
        EmailBot.combinedFilename = f"combined-emails-{EmailBot.startTime}.csv"

    def run():
        print('\n' + "="*10)
        print("Starting Search...")
        os.mkdir(EmailBot.outputPath)
        numFoundEmails = EmailBot.runSearch()
        print(f"Found {PrintColors.bold}{numFoundEmails}{PrintColors.reset} emails.\n")
        print("Applying secondary filters...")
        if my_globals.options['applySecondaryFilters']:
            EmailBot.createFilteredCSV(f"{numFoundEmails}-filtered_")
        if my_globals.options['createCombined']:
            EmailBot.createCombinedCSV(f"{numFoundEmails}_")
        outputMsg = f"Output in {PrintColors.bold}./{EmailBot.outputPath}{PrintColors.reset}"
        my_globals.output["outputPath"] = EmailBot.outputPath
        print(outputMsg)
        print("="*10 + '\n')
        return outputMsg

    def runSearch():
        def doSearch(terms=["default text"]):
            def getQueryText(text="default text", queryurl=BING_QUERY_URL):

                def getQueryTextHelper(text="default text", url=''):
                    if my_globals.terminate_early:
                        return '', []
                    try:
                        headers = {'user-agent': AGENT_LIST[random.randint(0, len(AGENT_LIST) - 1)]}
                        request_result = requests.get(url, headers=headers)
                        soup = BeautifulSoup(request_result.text,
                                             "html.parser")
                        if my_globals.options['searchURLs']:
                            links = []
                            for link in soup.find_all('a'):
                                href = link.get('href')
                                if href:
                                    for thing in BLACKLIST:
                                        if len(re.findall(thing, href)) > 0:
                                            href = None
                                            break
                                if not href or href[0:4] != 'http':
                                    continue
                                links.append(href)
                            links = list(set(links))
                        txt = soup.get_text()
                        if my_globals.options['showText']:
                            print(txt)
                            print(soup.find_all('p'))
                        return txt, links
                    except requests.exceptions.ConnectionError:
                        print(f"\n{PrintColors.red}WARNING: There was a connection error.{PrintColors.reset}\n")
                        return '', []

                searchUrl = queryurl + text.strip().replace(' ', '%20').replace('"', '%22')
                if my_globals.options['showURL']:
                    print(f"Search: {PrintColors.blue}{searchUrl}{PrintColors.reset}")
                txt, links = getQueryTextHelper(text, searchUrl)
                if my_globals.options['searchURLs']:
                    print("Searching Found Links:")
                    for link in links:
                        if my_globals.terminate_early:
                            return txt
                        current_time = time.strftime("%H:%M:%S", time.localtime())
                        print(f"\t{current_time}: {PrintColors.blue}{link}{PrintColors.reset}")
                        link_txt, link_links = getQueryTextHelper(url=link)
                        txt += link_txt

                return txt

            def filterFoundTerms(foundTerms):
                foundTermsFiltered = []
                if my_globals.options['makeLowercase']:
                    foundTerms = [e.lower() for e in foundTerms]  # to lowercase
                foundTerms = list(set(foundTerms))
                if my_globals.options['sortOutput']:
                    foundTerms.sort()
                for mail in foundTerms:
                    checks = []
                    # PRIMARY FILTERS HERE
                    # if False:
                    #     checks.append(False)
                    if my_globals.options['doPrimaryEmailCheck']:
                        checks.append(validate_email(email_address=mail, check_format=True, check_blacklist=False, check_dns=False, dns_timeout=10, check_smtp=False, smtp_timeout=10, smtp_helo_host=None, smtp_from_address=None, smtp_debug=False))

                    passAllChecks = all(checks)
                    if passAllChecks:
                        foundTermsFiltered.append(mail)
                        print(f"{PrintColors.green}{passAllChecks}{PrintColors.reset}  : {mail}")
                    else:
                        print(f"{PrintColors.red}{passAllChecks}{PrintColors.reset} : {mail}")

                if foundTermsFiltered == []:
                    print(f"{PrintColors.red}Warning: No valid emails found.{PrintColors.reset}")

                return foundTermsFiltered

            txt = ''
            for term in terms:
                if my_globals.terminate_early:
                    return []
                if my_globals.options['doBingSearch']:
                    txt += getQueryText(term, BING_QUERY_URL)
                if my_globals.options['doGoogleSearch']:
                    txt += getQueryText(term, GOOGLE_QUERY_URL)
            if len(re.findall(GOOGLE_BOT_MESSAGE, txt)) > 0:
                print(f"\n{PrintColors.red}WARNING: You may have been flagged as a bot (by Google). Uncomment `print(txt)` in the findemail() function to check.{PrintColors.reset}\n")

            myRegularExpression = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
            foundTerms = re.findall(myRegularExpression, txt)
            foundTerms = [e.strip(".") for e in foundTerms]
            return filterFoundTerms(foundTerms)

        def rowToQueries(row):
            queries = []

            # no quotes
            query = ''
            for j, elem in enumerate(row):
                query += f" {elem}"
            queries.append(query.strip())

            # quotes each word
            if my_globals.options['quoteEachWord']:
                for i, foo in enumerate(row):
                    query = ''
                    for j, elem in enumerate(row):
                        if my_globals.options['quoteEachWord'] and i == j:
                            # query += " \"" + elem + "\""
                            query += f" \"{elem}\""
                        else:
                            query += f" {elem}"
                    queries.append(query.strip())

            return queries

        f = open(EmailBot.outputPath+EmailBot.queryFilename, "a")
        queryNum = 0
        numFoundEmails = 0

        # csv output: do search and write to a csv
        with open(my_globals.options['inputFile'], newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            # iterate through rows of CSV
            for rowIndex, row in enumerate(spamreader):
                if my_globals.terminate_early:
                    csvfile.close()
                    f.close()
                    my_globals.terminate_early = False
                    print(f"\n{'!'*15}\nSearch Ended. You can safely start a new one now.\n{'!'*15}\n")
                    exit()
                if rowIndex < my_globals.options['startRow']:
                    f.write(f"\n")
                    continue
                if ' '.join(row).replace(',', ' ').strip() == '':  # empty row check
                    continue
                time.sleep(my_globals.options['delaySeconds'])

                for i, elem in enumerate(row):
                    row[i] = elem.replace(',', ' ').strip()
                row.append("email")
                row = [e for e in row if e]

                queryTerms = rowToQueries(row)
                print(f"{PrintColors.bold}{queryNum}{PrintColors.reset} " + f"\n{PrintColors.bold}query list:{PrintColors.reset} {row}\n{PrintColors.bold}search query(s):{PrintColors.reset} {queryTerms}")
                validEmails = doSearch(queryTerms)
                print(f"{PrintColors.bold}valid emails:{PrintColors.reset} {len(validEmails)}\n" + "\n")
                numFoundEmails += len(validEmails)
                f.write(f"{', '.join(validEmails)}\n")
                queryNum += 1
                if my_globals.options['numSearch'] != 0 and queryNum >= my_globals.options['numSearch']:
                    break

        csvfile.close()
        f.close()
        return numFoundEmails

    def createCombinedCSV(prefix=''):
        # csv output: write a new combined csv
        with open(my_globals.options['inputFile'], 'r') as f1, open(EmailBot.outputPath+EmailBot.queryFilename, 'r') as f2, open(EmailBot.outputPath+prefix+EmailBot.combinedFilename, 'w') as w:
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

            print(f"{PrintColors.bold}input:{PrintColors.reset}  {inputRows}")
            print(f"{PrintColors.bold}emails: {len(foundEmails)}:{PrintColors.reset} {foundEmails}")

            numBefore = len(foundEmails)

            # === START FILTER LOGIC ===

            def filterNoSharedChar(emails):
                # print(f"{PrintColors.bold}Use as filter:{PrintColors.reset} {inputRows[0:2]}")
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

            if len(foundEmails) > 0:
                print(f"{PrintColors.bold}Filtered Emails: {len(foundEmails)}:{PrintColors.reset} {foundEmails}")
            else:
                print(f"{PrintColors.bold}Filtered Emails: {PrintColors.red}{len(foundEmails)}:{PrintColors.reset} {foundEmails}")
            if numBefore - numAfter == 0: 
                print(f"Found {PrintColors.red}0{PrintColors.reset} emails after filters.")
            else:
                print(f"Found {PrintColors.bold}{numBefore - numAfter}{PrintColors.reset} emails after filters.\n")
            return inputRows, foundEmails

        with open(my_globals.options['inputFile'], 'r') as f1, open(EmailBot.outputPath+EmailBot.queryFilename, 'r') as f2, open(EmailBot.outputPath+prefix+EmailBot.combinedFilename, 'w') as w:
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
    EmailBot.update()
    # Command line parsing
    longOpts = [f'{e}=' for e in my_globals.optionNames].copy()
    longOpts.append('help')
    try:
        opts, args = getopt.getopt(argv, shortopts='h', longopts=longOpts)
    except getopt.GetoptError:
        print(f"{PrintColors.red}Invalid options.{PrintColors.reset} Usage:")
        print('main.py ' + '=<value> '.join([f'--{e}' for e in my_globals.optionNames]))
        sys.exit(2)
    for opt, arg in opts:
        # print(f"{opt} {arg}")
        if opt in ('-h', '--help'):
            print('main.py ' + '=<value> '.join([f'--{e}' for e in my_globals.optionNames]), end='=<value>\n')
            sys.exit()
        elif opt in [f'--{e}' for e in my_globals.optionNames]:
            if arg.lower() in ['t', 'true']:
                my_globals.options[opt[2:]] = True
            elif arg.lower() in ['f', 'false']:
                my_globals.options[opt[2:]] = False
            else:
                try:
                    my_globals.options[opt[2:]] = int(arg)
                except ValueError:
                    my_globals.options[opt[2:]] = arg

    PrintColors.update()
    EmailBot.run()


if __name__ == "__main__":
    my_globals.initialize()
    main(sys.argv[1:])
