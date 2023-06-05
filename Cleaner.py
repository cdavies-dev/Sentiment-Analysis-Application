import warnings

import dataframe_image as dfi
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd

warnings.simplefilter(action = 'ignore', category = FutureWarning)

data = pd.read_csv('D:/OneDrive/Desktop/articles_dirty.csv')
scraped_counts = data['Source'].value_counts()

try:
    data.drop_duplicates(subset = ['Article'], inplace = True) #drop duplicates
    data = data.drop(data[(data['Article'] == '') | (data['Article'] == 'Sorry...') | (data['Article'] == 'Unauthorized')].index) #drop failed access
    data = data[~data.apply(lambda row: row.astype(str).str.contains('404').any(), axis = 1)] #drop 404s

    data['Text'] = data['Text'].str.replace('This video can not be played', '') #drop video playback message in text

    retained_counts = data['Source'].value_counts()
    data.to_csv('D:/OneDrive/Desktop/articles_clean.csv', index = False)
    results = pd.DataFrame(columns = ['Source', 'Scraped', 'Retained'])
    results['Source'] = scraped_counts.index
    results['Scraped'] = scraped_counts.tolist()
    results['Retained'] = retained_counts.tolist()

    path = 'D:/OneDrive/Desktop/results.png' 
    dfi.export(results, path)
    image = mpimg.imread(path)
    plt.imshow(image)
    plt.tick_params(
        axis = 'both',
        which = 'both',
        top = False,
        bottom = False,
        left = False,
        right = False,
        labelbottom = False,
        labelleft = False)
    plt.show()

    print('Cleaning complete!')
except:
    print('Cleaning failed!')
    exit()