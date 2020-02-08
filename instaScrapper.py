from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import re
from urllib.request import urlopen
import json
from pandas.io.json import json_normalize
import pandas as pd, numpy as np
import glob

# dirrectory where to save files with info
directory_path = '_results_files'
# path to chrome driver
browser = webdriver.Chrome('C:/chromedriver.exe')
links = []

# how many pages scrap
n_pages = 100
# hashtag / user
mode = 'hashtag'
# list of hashtags / usernames
name_list = ['2019ncov', 'coronavirusoutbreak','coronavirusnews', 'chinavirus', 'ncov', 'ncov2019' ]
#name_list = ['liwenliang']
# , 'selfiestick', 'selfiequeen'
# save info each ... (in case of bad connection orsome error during scrapping better do not wait till last / 
# also easier to stop script if you want without loosing all data)
save_after = 50


def scrollPage(n_pages = 1):

    print("PAGE     : 0")

    Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    source = browser.page_source
    data=bs(source, 'html.parser')
    body = data.find('body')
    script = body.find('span')
    for link in body.findAll('a'):
        #print(link)
        if re.match("/p", link.get('href')):
            links.append('https://www.instagram.com'+link.get('href'))

    time.sleep(5) 

    if n_pages > 1:
        for i in range(n_pages-1):
            print("PAGE     : {}".format(i+1))
            Pagelength = browser.execute_script("window.scrollTo(document.body.scrollHeight/2, document.body.scrollHeight);")
            source = browser.page_source
            data=bs(source, 'html.parser')
            body = data.find('body')
            script = body.find('span')
            for link in body.findAll('a'):
                if re.match("/p", link.get('href')):
                    links.append('https://www.instagram.com'+link.get('href'))
            
            time.sleep(5) 

def getInfo(links, name, save_after):
    
    # read the file with images we already parsed (use list_dir.py to create ths file first)
    shortcodes = pd.read_csv('shortcodes.csv')

    #do not replace already existing files
    cur_file = 0
    files = glob.glob("{}/{}_*".format(directory_path,name), recursive=True)
    print("FILES with {} - {}".format(name,len(files)))
    cur_file = len(files)
    
    links = list(set(links))

    if len(links) > 0:
        result=pd.DataFrame()
        
        q = 0

        for i in range(len(links)):
            
            # check if we alreay parsed this image
            short = [links[i].split('/')[4]]
            m = shortcodes.isin(short).any()
            cols = m.index[m].tolist()
            
            # if not
            if len(cols) == 0:
                
                try:
                    print("{}   {}".format(i, links[i]))
                    page = urlopen(links[i]).read()
                    data=bs(page, 'html.parser')
                    body = data.find('body')
                    script = body.find('script')
                    raw = script.text.strip().replace('window._sharedData =', '').replace(';', '')
                    json_data=json.loads(raw)
                    posts =json_data['entry_data']['PostPage'][0]['graphql']
                    posts= json.dumps(posts)
                    posts = json.loads(posts)
                    x = pd.DataFrame.from_dict(json_normalize(posts), orient='columns') 
                    x.columns =  x.columns.str.replace("shortcode_media.", "")
                    result=result.append(x)
                    q += 1
                
                except:
                    print('     CANT PARSE IMAGE')
                    np.nan

                if q > save_after:
                    
                    result = result.drop_duplicates(subset = 'shortcode')
                    result.to_csv('{}/{}_{}.csv'.format(directory_path, name, cur_file))
                    print('-' * 30)
                    print("FILE SAVED     : {}_{}.csv".format(name, cur_file))
                    cur_file += 1
                    result=pd.DataFrame()
                    q = 0
            else:
                print('{}   {}  Already parsed'.format(i, links[i]))
        
        result = result.drop_duplicates(subset = 'shortcode')
        result.to_csv('{}/{}_{}.csv'.format(directory_path, name, cur_file))
        print('-' * 10)
        print("FILE SAVED     : {}_{}.csv".format(name, cur_file))

        del links[:]

def instaScrapper( name_list, n_pages, mode = 'hashtag', save_after=100):
    
    if mode == 'user':
        for name in name_list:
            print(' ')
            print('-' * 30)
            print("PARSING NAME     : {}".format(name))
            username = name
            browser.get('https://www.instagram.com/'+username+'/?hl=en')

            scrollPage(n_pages)
            getInfo(links, name, save_after)


    else:

        for name in name_list:
            print(' ')
            print('-' * 30)
            print("PARSING NAME     : {}".format(name))
            hashtag = name
            browser.get('https://www.instagram.com/explore/tags/'+hashtag)

            scrollPage(n_pages)
            getInfo(links, name, save_after)
            
instaScrapper( name_list, n_pages, mode, save_after)