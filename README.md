# Email Scraper

Takes input csv of search terms, does Bing search, outputs found emails.

## Installing (not comprehensive)

Run these commands (not comprehensive because I forgot if there were more).

`python -m pip install py3-validate-email`

`python -m pip install bs4`

## Running

### How To Run

Run in terminal with: `python main.py` (or `python3 main.py`). 
You must use python version 3.6 or above. 
I've only run it on Python 3.9.

### Options

To configure your search, you can edit parameters at top of `main.py` and/or use the command line options below.

#### Command line options

`main.py -i <inputfilepath> -s <startrow> -n <numsearch>`

- `-i <inputfilepath>`: specify input file
- `-s <startrow>`: specify row to start
- `-n <numsearch>`: specify number of searches to do (`0` to process entire input file)

Example starting from row `10` and doing `5` searches:

`python main.py -s 10 -n 5`

Example starting from row `1` (the header counts as row 0) and doing searches for the entire input file:

`python main.py -s 1 -n 0`

#### Inline options


These are default values overridden by command line arguments
```
startRow = 1   # What row to start from. Default 1 because row 0 is the header
numSearch = 5  # The number of google searches it will do, if 0, will go forever
inputFile = 'input/TestCaseEmailScript.csv' # path to the input csv file
```

Select what searches to do (Google will mark as bot so set to False by default)
```
DO_BING_SEARCH = True
DO_GOOGLE_SEARCH = False
```

Delay (Default 0 since bing has no bot detection)
```
DELAY_SECONDS = 0
```

Other options
```
QUOTE_EACH_WORD = True    # Option to do multiple searches with a different word in quotes each time. If set to False quotes none.
CREATE_COMBINED = True    # Creates a seperate "combined" csv that appends the found emails to the original csv
```

Primary filters. Primary filters are applied to every email.
```
DO_PRIMARY_EMAIL_CHECK = True # Filters emails using the validate_email package
```

Secondary filters. Seconary filters are only applied to create a seperate "filtered" csv. This is because these filters might be too strong and remove all/most emails.
```
APPLY_NAME_FILTER = False # Filters emails so they must contain some part of the person's name
```

Debugging
```
SORT_OUTPUT = True  # Sorts the output in terminal of found emails which can be helpful to see patterns
SHOW_TXT = False    # Shows the raw text the search found
```

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
