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

UPDATE: How the program is run has changed. It is now purely through the command line.

```
main.py --startRow=<value> --numSearch=<value> --inputFile=<value> --doBingSearch=<value> --doGoogleSearch=<value> --delaySeconds=<value> --quoteEachWord=<value> --createCombined=<value> --disableColors=<value> --doPrimaryEmailCheck=<value> --applySecondaryFilters=<value> --sortOutput=<value> --showText=<value> --makeLowercase
```

#### Command line options

<img width="1552" alt="Screen Shot 2021-06-25 at 4 19 44 PM" src="https://user-images.githubusercontent.com/53503018/123910568-41ccb080-d940-11eb-9c36-eca814f48026.png">


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

## GUI (in progress)

`python3 -m pip install PySimpleGUI`

`python gui.py`

![image](https://user-images.githubusercontent.com/53503018/123910424-09c56d80-d940-11eb-92fa-617673a2914b.png)


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
