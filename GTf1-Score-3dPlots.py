import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.colors import Normalize
from sklearn.metrics import f1_score, confusion_matrix

df_befragung = pd.read_csv('KommentareBefragungStatistik.csv')
befragungScores = np.array(df_befragung['Mittelwert'].tolist()) / 10

tool_names = [
    'German Sentiment Classification with BERT','German Sentiment Analysis',
    'XMLRoBERTaGerman','textblob_de','NLTK Vader','spaCy',
    'DistilBERT base uncased finetuned SST-2','bertweet','Twitter-roBERTa-base'
]

radius_values = np.arange(0.15, 0.5, 0.01)

def classification_scores(scores, radius):
    bins = [-1, -radius, radius, 1]
    return np.digitize(scores, bins, right=True)

f1_scores_list = []

output_folder = '3d Plots GT'
os.makedirs(output_folder, exist_ok=True)

for tool_name in tool_names:

    df_tool = pd.read_csv('GTKommentareToolScores.csv')

    tool_scores = df_tool[tool_name].tolist()

    macro_f1_scores = np.zeros((len(radius_values), len(radius_values)))

    for i, radius_manual in enumerate(radius_values):
        for j, radius_model in enumerate(radius_values):
            manual_classes = classification_scores(befragungScores, radius_manual)
            model_classes = classification_scores(tool_scores, radius_model)
            
            f1_score_value = f1_score(
                manual_classes, 
                model_classes, 
                average='macro', 
                labels=[1, 2, 3]
            )
            
            macro_f1_scores[i, j] = f1_score_value
            f1_scores_list.append({
                'Tool': tool_name,
                'Radius_Manual': radius_manual,
                'Radius_Model': radius_model,
                'F1_Score': f1_score_value
            })
            
    max_f1_score = np.max(macro_f1_scores)
    max_index = np.unravel_index(np.argmax(macro_f1_scores), macro_f1_scores.shape)
    radius_manual_max, radius_model_max = radius_values[max_index[0]], radius_values[max_index[1]]

    print(f"Tool: {tool_name}")
    print(f"Höchster Makro-F1-Score: {max_f1_score:.4f}")
    print(f"Radien für höchsten Makro-F1-Score: Radius Manual = {radius_manual_max:.2f}, Radius Model = {radius_model_max:.2f}")

    best_manual_classes = classification_scores(befragungScores, radius_manual_max)
    best_model_classes = classification_scores(tool_scores, radius_model_max)
    cm = confusion_matrix(best_manual_classes, best_model_classes, labels=[1, 2, 3])

    print(f"Konfusionsmatrix für {tool_name} bei höchsten Makro-F1-Score:")
    print(cm)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    X, Y = np.meshgrid(radius_values, radius_values)
    Z = macro_f1_scores

    norm = Normalize(vmin=0, vmax=1)

    surface = ax.plot_surface(X, Y, Z, cmap='viridis', norm=norm, edgecolor='none')

    cbar = fig.colorbar(surface, ax=ax, shrink=0.5, aspect=5)
    cbar.set_label('Macro F1 Score')

    ax.set_xlabel('Radius Manual')
    ax.set_ylabel('Radius Model')
    ax.set_zlabel('Macro F1 Score')
    ax.set_title(f'3D Surface Plot für {tool_name}')

    plt.savefig(os.path.join(output_folder, f'GT_3D_Surface_Plot_{tool_name}.png'))
    plt.close()

f1_scores_df = pd.DataFrame(f1_scores_list)

f1_scores_df.to_csv('GTf1_scores_all_tools.csv', index=False)
