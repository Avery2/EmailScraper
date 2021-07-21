initialized = False
terminate_early = False

optionNames = None
options = None
output = None

def initialize():
    global initialized
    if initialized:
        return
    initialized = True
    global optionNames
    optionNames = ['startRow',
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
                   'makeLowercase',
                   'showURL',
                   'searchURLs']

    global options
    options = {optionNames[0]: 1,  # startRow
               optionNames[1]: 5,  # numSearch
               optionNames[2]: 'input/TestCaseEmailScript.csv',  # inputFile
               optionNames[3]: True,  # doBingSearch
               optionNames[4]: False,  # doGoogleSearch
               optionNames[5]: 0,  # delaySeconds
               optionNames[6]: True,  # quoteEachWord
               optionNames[7]: True,  # createCombined
               optionNames[8]: False,  # disableColors
               optionNames[9]: True,  # doPrimaryEmailCheck
               optionNames[10]: True,  # applySecondaryFilters
               optionNames[11]: True,  # sortOutput
               optionNames[12]: False,  # showText
               optionNames[13]: True,  # makeLowercase
               optionNames[14]: True,  # showURL
               optionNames[15]: True,  # searchURLs
               }

    global output
    output = {"outputPath": None}
