import warnings

import pandas as pd
import win32com.client
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob

warnings.simplefilter(action = 'ignore', category = FutureWarning)

similarity_threshold = 0.1 #set to 10%
data = pd.read_csv('D:/OneDrive/Desktop/articles_clean.csv')
sources = data['Source'].drop_duplicates() #also check manually for testing
data1 = data.loc[data['Source'] == sources[0]]
data2 = data.loc[data['Source'] == sources[20]] #currently hard coded
final_data = pd.DataFrame(columns = ['Source1', 'Article1', 'Subjectivity1', 'Polarity1', 'Source2', 'Article2', 'Subjectivity2', 'Polarity2', 'Similarity'])

source1_list = []
article1_list = []
subjectivity1_list = []
polarity1_list = []

source2_list = []
article2_list = []
subjectivity2_list = []
polarity2_list = []

similarity_list = []

def get_similarity(text1, text2):
    #tokenize and remove stop words
    stop_words = set(stopwords.words('english'))
    tokens1 = [word.lower() for word in word_tokenize(text1) if word.isalpha() and word.lower() not in stop_words]
    tokens2 = [word.lower() for word in word_tokenize(text2) if word.isalpha() and word.lower() not in stop_words]
    
    #calculate Jaccard similarity
    score = len(set(tokens1) & set(tokens2)) / len(set(tokens1) | set(tokens2))
    
    return score

def get_analysis(text):
    blob = TextBlob(text)
    subjectivity = blob.sentiment.subjectivity
    polarity = blob.sentiment.polarity

    return subjectivity, polarity

try: 
    for i, row1 in data1.iterrows():
        for j, row2 in data2.iterrows():
            if i == j:
                continue
            else:
                score = get_similarity(row1['Text'], row2['Text'])
                if score > similarity_threshold:
                    subjectivity1, polarity1, = get_analysis(row1['Text'])
                    subjectivity2, polarity2 = get_analysis(row2['Text'])
                    
                    source1_list.append(row1['Source'])
                    article1_list.append(row1['Article'])
                    subjectivity1_list.append(subjectivity1)
                    polarity1_list.append(polarity1)

                    source2_list.append(row2['Source'])
                    article2_list.append(row2['Article'])
                    similarity_list.append(score)
                    subjectivity2_list.append(subjectivity2)
                    polarity2_list.append(polarity2)
                else:
                    continue
                    
    final_data['Source1'] = source1_list
    final_data['Article1'] = article1_list
    final_data['Subjectivity1'] = subjectivity1_list
    final_data['Polarity1'] = polarity1_list

    final_data['Source2'] = source2_list
    final_data['Article2'] = article2_list
    final_data['Subjectivity2'] = subjectivity2_list
    final_data['Polarity2'] = polarity2_list

    final_data['Similarity'] = similarity_list

    final_data.to_csv('D:/OneDrive/Desktop/final_data.csv', index = False)
    print('Analysis complete!')
except:
    print('Analysis failed!')
    exit()

#excel = win32com.client.Dispatch('Excel.Application')
#excel.Visible = True
#excel.WindowState = -4137
#workbook = excel.Workbooks.Open(r'D:/OneDrive/Desktop/final_data.csv')
#worksheet = workbook.ActiveSheet
#worksheet.Columns.AutoFit()
#win32com.client.Dispatch("WScript.Shell").AppActivate(excel.Caption)