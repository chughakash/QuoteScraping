import urllib2
import json
from bs4 import BeautifulSoup

#Parse brainyquote website for motivational quotes
def scrape():
    result = {}
    web_page = 'https://www.brainyquote.com/topics/motivational'
    header =  {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    request = urllib2.Request(web_page,headers = header)
    try:
        html_page_open = urllib2.urlopen(request)
    except urllib2.HTTPError, e:
            print e.fp.read()
    html_skeleton = BeautifulSoup(html_page_open,'html.parser')
    quotesList =  html_skeleton.find("div", {"id": "quotesList"})
    quotes = quotesList.find_all("a", {"title": "view quote"})
    extractedQuoteList = []
    extractedAuthorsList = []

    #Create quptes list
    for quote in quotes:
        extractedQuoteList.append(quote.text)
    authors = quotesList.find_all("a", {"title": "view author"})

    #Create author list
    for author in authors:
        extractedAuthorsList.append(author.text)

    #Create JSON object
    for i in range(0,len(extractedQuoteList)):
        create_json(i,result,extractedQuoteList[i],extractedAuthorsList[i],"motivation")

    result_json_object = json.dumps(result)
    print result_json_object
    file_write(result_json_object)

# Write json object to file
def file_write(json_text):
    f = open("quotes.txt", "w+")
    f.write(json_text)
    f.close()

# JSON Object format : {"0": {"category": "motivation", "quote": "Only I can change my life. No one can do it for me.",
# "author": "Carol Burnett"}...}
def create_json(index, result, quote, author, category):
    buffer_dict = {}
    buffer_dict['quote'] = quote
    buffer_dict['author'] = author
    buffer_dict['category'] = category
    result[index] = buffer_dict

if __name__ == "__main__":
    scrape()







