from projet import *


chemin_dossier = "./speeches"
nom_président_extraits = extraire_noms_presidents(chemin_dossier)
Dico = { }
# Afficher les noms des présidents extraits
for nom in noms_presidents_extraits:
    if nom == "Chirac" and not nom in Dico:
        Dico["Chirac"] = "Jacque"
        print("Jacque "+nom)
    elif nom == "Mitterrand" and not nom in Dico:
        Dico["Mitterrand"] = "François"
        print("François "+nom)
    elif nom == "Sarkozy" and not nom in Dico:
        Dico["Sarkozy"] = "Nicolas"
        print("Nicolas "+nom)
    elif nom == "Hollande" and not nom in Dico:
        Dico["Hollande"] = "François"
        print("François "+nom)
    elif nom == "Giscard dEstaing" and not nom in Dico:
        Dico["Giscard dEstaing"] = "Valéry"
        print("Valéry "+nom)
    elif nom == "Macron" and not nom in Dico:
        Dico["Macron"] = "Emmanuel"
        print("Emmanuel "+nom)

