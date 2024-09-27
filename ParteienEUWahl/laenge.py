import pandas as pd


cdu = pd.read_csv('Thesen/ParteienEUWahl/KommentareCDU.csv')
spd = pd.read_csv('Thesen/ParteienEUWahl/KommentareSPD.csv')
gruene = pd.read_csv('Thesen/ParteienEUWahl/KommentareDIEGRUENEN.csv')
afd = pd.read_csv('Thesen/ParteienEUWahl/KommentareAFD.csv')

qcdu = pd.read_csv('Thesen/ParteienEUWahl/QuellenCDU.csv')
qspd = pd.read_csv('Thesen/ParteienEUWahl/QuellenSPD.csv')
qgruene = pd.read_csv('Thesen/ParteienEUWahl/QuellenDIEGRUENEN.csv')
qafd = pd.read_csv('Thesen/ParteienEUWahl/QuellenAFD.csv')
print("Anzahl Kommentare")
print("CDU: "+str(len(cdu)))
print("SPD: "+str(len(spd)))
print("DieGruene: "+str(len(gruene)))
print("AfD: "+str(len(afd)))
print("Anzahl Kommentare pro Beitrag")
print("CDU: "+str(len(cdu)/len(qcdu)))
print("SPD: "+str(len(spd)/len(qspd)))
print("DieGruene: "+str(len(gruene)/len(qgruene)))
print("AfD: "+str(len(afd)/len(qafd)))