if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && start "" /min "%~dpnx0" %* && exit
@pyw C:\Users\jerem\OneDrive\Summer\WebScraper\scrape.py %*
exit