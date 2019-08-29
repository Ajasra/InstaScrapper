import glob
import os
 
directory_path = '../_results_files'
files = glob.glob(directory_path + '/**/*', recursive=True)


for curfile in files:
    os.rename(curfile, curfile.replace('.done',''))