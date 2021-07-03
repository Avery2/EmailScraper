# Email Scraper

Takes input csv of search terms, does Bing search, outputs found emails.

## Installing (not comprehensive)

Run these commands (not comprehensive because I forgot if there were more).

`python -m pip install py3-validate-email`

`python -m pip install bs4`

If you want to use GUI:

`python3 -m pip install PySimpleGUI`

## Running

### How To Run

Run in terminal with: `python main.py` (or `python3 main.py`).
You must use python version 3.6 or above.
I've only run it on Python 3.9.

### Command line options

UPDATE: How the program is run has changed. It is now purely through the command line.

```
main.py --startRow=<value> --numSearch=<value> --inputFile=<value> --doBingSearch=<value> --doGoogleSearch=<value> --delaySeconds=<value> --quoteEachWord=<value> --createCombined=<value> --disableColors=<value> --doPrimaryEmailCheck=<value> --applySecondaryFilters=<value> --sortOutput=<value> --showText=<value> --makeLowercase
```

| Option                | Description                                                                                | Default Value                 |
| --------------------- | ------------------------------------------------------------------------------------------ | ----------------------------- |
| startRow              | (int) Row to start on                                                                      | 1                             |
| numSearch             | (int) Number of searches to do (0 to process entire input file)                            | 5                             |
| inputFile             | (str) Path to input file                                                                   | input/TestCaseEmailScript.csv |
| doBingSearch          | (bool) Do Bing search                                                                      | True                          |
| doGoogleSearch        | (bool) Do Google search                                                                    | False                         |
| delaySeconds          | (int) Delay beteween searches (to avoid bots)                                              | 0                             |
| quoteEachWord         | (bool) Do multiple searches with a different word in quotes each time. If False quote none | True                          |
| createCombined        | (bool) Creates a seperate "combined" csv that appends the found emails to the original csv | True                          |
| disableColors         | (bool) Disables termial output coloring                                                    | False                         |
| doPrimaryEmailCheck   | (bool) Filters emails using the validate_email package                                     | True                          |
| applySecondaryFilters | (bool) Does secondary filtering based on custom functions                                  | True                          |
| sortOutput            | (bool) Sorts the output in terminal of found emails which can be helpful to see patterns   | True                          |
| showText              | (bool) Shows the raw text the search found                                                 | False                         |
| makeLowercase         | (bool) Makes the emails lowercase (and therefore not case sensitive)                       | True                          |
| showURL               | (bool) Shows search query URL                                                              | True                          |

Example: `python main.py --numSearch 0 --inputFile input/UpdatedTestCaseHubSpot.csv`

<img width="1552" alt="Screen Shot 2021-07-03 at 10 34 48 AM" src="https://user-images.githubusercontent.com/53503018/124359417-6cda2d00-dbea-11eb-888e-c8412128c765.png">

## Other

Code assumes the input file has this structure:

```
1st column = first name
2nd column = last name
3rd column = company/university
4th column = key term 1
5th column = key term 2
...
```

Example filter function that just removes the first email if it exists. This function would go in the `FILTER LOGIC` section of the `applySecondaryFilters` function in case you want to apply your own filter. To do this just make your own function in a similar form that takes in the `foundEmails` list, mutates it by removing whatever you wany, and returns it. Then call your function and set the `foundEmails`

```
def filterExample(emails):
    # Set first email to None if it exists
    if emails[0]:
        emails[0] = None
    # Filter None out of list
    emails = list(filter(None, emails))
    return emails
# Call Function
foundEmails = filterExample(foundEmails)
```

Template that does nothing.

```
def filterTemplate(emails):
    return emails

foundEmails = filterTemplate(emails)
```

## GUI (now working!)

To run:

`python gui.py`

<img width="1322" alt="Screen Shot 2021-07-03 at 10 35 08 AM" src="https://user-images.githubusercontent.com/53503018/124359420-7368a480-dbea-11eb-9679-40bc46282881.png">


## Link Dump

[[Writing to file in python]](https://www.w3schools.com/python/python_file_write.asp)
[[regex cheat sheet]](https://cheatography.com/davechild/cheat-sheets/regular-expressions/)
[[regex tester]](https://regex101.com/r/BpnZWY/1/)
[[python regex library]](https://docs.python.org/3/library/re.html)
[[beautiful soup - the library used to do google searches]](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
[[Scrape Google Search Results using Python BeautifulSoup geeksforgeeks article]](https://www.geeksforgeeks.org/scrape-google-search-results-using-python-beautifulsoup/)
[[test email]](https://gist.github.com/cjaoude/fd9910626629b53c4d25)
[[email regex]](https://emailregex.com/)
[[email validation]](https://github.com/karolyi/py3-validate-email)
[[workarounds need to randomize headers sometime]](https://pknerd.medium.com/5-strategies-to-write-unblock-able-web-scrapers-in-python-5e40c147bdaf)
[[Linkedin API]](https://docs.microsoft.com/en-us/linkedin/)
[[python to executable on mac]](https://superuser.com/questions/1164706/how-do-i-make-a-python-file-executable-on-macos-sierra/1420649)
