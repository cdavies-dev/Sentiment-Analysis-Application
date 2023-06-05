import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = pd.read_csv('D:/OneDrive/Desktop/final_data.csv')
source1 = data['Source1'].drop_duplicates()
source2 = data['Source2'].drop_duplicates()
try:
    plt.plot(data['Subjectivity1'], label = source1[0])
    plt.plot(data['Subjectivity2'], label = source2[0])
    #plt.plot(data['Similarity'], label = 'Similarity (%)')
    plt.xlabel('Articles')
    plt.ylabel('Subjectivity (%)')
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.legend()
    plt.savefig('D:/OneDrive/Desktop/Objectivity.png')
    plt.show()

    plt.plot(data['Polarity1'], label = source1[0])
    plt.plot(data['Polarity2'], label = source2[0])
    #plt.plot(data['Similarity'], label = 'Similarity (%)')
    plt.xlabel('Articles')
    plt.ylabel('Polarity (%)')
    plt.yticks(np.arange(-1, 1.1, 0.2))
    plt.legend()
    plt.savefig('D:/OneDrive/Desktop/Polarity.png')
    plt.show()
    
    print('Plotting complete!')
except:
    print('Plotting failed!')
    exit()
