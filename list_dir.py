import glob
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
 
directory_path = '_results_files'
files = glob.glob(directory_path + '/**/*', recursive=True)
save_to = 'shortcodes.csv'

data = DataFrame()

for curfile in files:
    temp = pd.read_csv(curfile)
    try:
        tmp = temp[['shortcode','edge_media_preview_comment.count','edge_media_preview_like.count', 'edge_media_to_caption.edges']]
        data = pd.concat([data, tmp])
    except:
        print('empty')
    print(curfile)

data.drop_duplicates(subset=['shortcode'], inplace = True)
 
data.to_csv(save_to)
    