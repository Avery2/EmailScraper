# Email Scraper

Takes a csv as input for search terms, checks google page for emails, outputs as txt file with found emails.

## Running

Edit parameters at top of `main.py` then run in terminal: `python main.py` (or `python3 main.py`).

Command line options:

`main.py -i <inputfilepath> -s <startrow> -n <numsearch>`

- `-i <inputfilepath>`: specify input file
- `-s <startrow>`: specify row to start
- `-n <numsearch>`: specify number of searches to do

Example starting from row `10` and doing `5` searches:

`python main.py -s 10 -n 5`

Make sure you use python version 3.6 or above. Python 3.9 works best.

## Link Dump

<!-- []() -->

- [Writing to file in python](https://www.w3schools.com/python/python_file_write.asp)

- [regex cheat sheet](https://cheatography.com/davechild/cheat-sheets/regular-expressions/)

- [regex tester](https://regex101.com/r/BpnZWY/1/)

- [python regex library](https://docs.python.org/3/library/re.html)

- [beautiful soup - the library used to do google searches](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

- [Scrape Google Search Results using Python BeautifulSoup geeksforgeeks article](https://www.geeksforgeeks.org/scrape-google-search-results-using-python-beautifulsoup/)

- [test email](https://gist.github.com/cjaoude/fd9910626629b53c4d25)

- [email regex](https://emailregex.com/)

- [email validation](https://github.com/karolyi/py3-validate-email)

- [workarounds need to randomize headers sometime](https://pknerd.medium.com/5-strategies-to-write-unblock-able-web-scrapers-in-python-5e40c147bdaf)

## Possible Expansions

[Linkedin API](https://docs.microsoft.com/en-us/linkedin/)

## Installing and stuff (not comprehensive)

`python -m pip install py3-validate-email`
