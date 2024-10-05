import pandas as pd

file_path = 'Thesen/IsraelGazaVerlauf/Kommentare.csv'
data = pd.read_csv(file_path)

def count_positive_values(data, column_name):
    positive_count = data[column_name][data[column_name] > 0].count()
    return positive_count

print(count_positive_values(data, 'sentimentDEU'))