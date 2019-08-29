import os
import requests
import urllib.request
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import glob

directory_path = '../_results_files'
files = glob.glob(directory_path + '/**/*.csv', recursive=True)

directory="../_scrapped"
for curfile in files:
        print('READING          {}'.format(curfile))
        temp = pd.read_csv(curfile)
        q = 0
        for i in range(len(temp)):
                if(temp['is_video'][i] == False):
                        try:
                                filename = "{}\{}.jpg".format(directory, temp['shortcode'][i])
                                print(filename)
                                if not os.path.isfile(filename):
                                        urllib.request.urlretrieve(temp['display_url'][i],  filename)
                                        q += 1
                                else:
                                        print('{}       FILE ALREADY EXIST'.format(filename))
                        except:
                                print('IMAGE HAVE LOST SOME DATA')
        

        print('{}       DOWNLOADED FROM FILE    {}'.format(q,curfile))
        os.rename(curfile, "{}.done".format(curfile))