import os
def extraire_noms_presidents(chemin_dossier):
    noms_presidents = []
    # Parcourir tous les fichiers du dossier
    for nom_fichier in os.listdir(chemin_dossier):
        chemin_fichier = os.path.join(chemin_dossier, nom_fichier)
        # Vérifier si le chemin correspond à un fichier
        if os.path.isfile(chemin_fichier):
            # Extraire le nom du président du titre du fichier
            nom_president = nom_fichier.split('_')[1]  # Supposant que le nom du président est après la première occurrence de '_' dans le nom du fichier
            # Utiliser endswith() pour vérifier si le nom se termine par une lettre
            if nom_president.endswith('1.txt') or nom_president.endswith('2.txt'):
                nom_president = nom_president[:-5]  # Supprimer l'extension du fichier
            else :
                nom_president = nom_president[:-4 ]  # Supprimer l'extension du fichie
            noms_presidents.append(nom_president)
    return noms_presidents
# Spécifiez le chemin du dossier contenant les fichiers
chemin_dossier = "./speeches"
# Appel de la fonction pour extraire les noms des présidents
noms_presidents_extraits = extraire_noms_presidents(chemin_dossier)


def clean_and_save_files(input_folder="speeches", output_folder="cleaned"):
    # Vérifier si le dossier de sortie existe, sinon le créer
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # Parcourir les fichiers dans le dossier d'entrée
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):  # Assurez-vous que le fichier est un fichier texte (vous pouvez ajuster l'extension si nécessaire)
            input_filepath = os.path.join(input_folder, filename)
            output_filepath = os.path.join(output_folder, filename)
            # Lire le contenu du fichier d'entrée
            with open(input_filepath, "r", encoding="utf-8") as file:
                content = file.read()
            # Convertir le contenu en minuscules
            content_lower = content.lower()
            # Écrire le contenu transformé dans le fichier de sortie
            with open(output_filepath, "w", encoding="utf-8") as file:
                file.write(content_lower)
# Utilisation de la fonction avec les noms de dossiers par défaut
clean_and_save_files()

def enlever_ponctuation() -> None:
    PONCTUATION = '!"#$%&()*+,./:;<=>?@[\\]^_`{|}~'  # Liste des signes de ponctuation.
    PONCTUATION_ESPACE = "-'"  # Liste des signes de ponctuation qui doivent être remplacés par un espace.
    for nom_fichier in os.listdir('cleaned'): #On parcourt tout les fichiers du dossier cleaned.
        if os.path.isfile('./cleaned/' + nom_fichier) and nom_fichier.endswith('.txt'): #On vérifie que ce qu'on a n'est pas un dossier et si c'est bien un fichier texte.
            with open('./cleaned/'+ nom_fichier, "r", encoding="UTF-8") as fichier: #On ouvre chaque fichier en lecture (le r de read).
                lignes = fichier.readlines() #On extrait les lignes du fichier.
                with open('./cleaned/' + nom_fichier, "w", encoding="UTF-8") as fichier_ecriture: #On ouvre chaque fichier en écriture (le w de write).
                    for ligne in lignes: #Pour chaque ligne du fichier,
                        for ponc in PONCTUATION: #Pour chaque élément de ponctuation,
                            ligne=ligne.replace(ponc, "") #on efface les signes de ponctuation.
                        for ponc in PONCTUATION_ESPACE: #Pour chaque élément de ponctuation_espace,
                            ligne=ligne.replace(ponc, " ") #on le remplace des espaces.
                        fichier_ecriture.write(ligne)


enlever_ponctuation()


def TF(folder="cleaned"):
    # Dictionnaire pour stocker le nombre d'occurrences de chaque mot pour chaque fichier
    tf_matrices = {}
    # Parcourir les fichiers dans le dossier
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):  # Assurez-vous que le fichier est un fichier texte (ajustez l'extension si nécessaire)
            file_path = os.path.join(folder, filename)
            # Lire le contenu du fichier
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            # Initialiser le dictionnaire pour stocker le nombre d'occurrences de chaque mot
            word_count = {}
            # Diviser la chaîne en mots
            words = content.split()
            # Compter le nombre d'occurrences de chaque mot
            for word in words:
                # Ignorer la casse et la ponctuation
                # Mettre à jour le dictionnaire
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1
            # Stocker le dictionnaire dans la matrice TF
            tf_matrices[filename] = word_count
    return tf_matrices

import math

def IDF(corpus_folder="cleaned"):
    # Dictionnaire pour stocker le nombre de documents contenant chaque mot
    document_frequency = {}
    # Compteur total de documents dans le corpus
    total_documents = 0
    # Parcourir les fichiers dans le corpus
    for filename in os.listdir(corpus_folder):
        if filename.endswith(".txt"):  # Assurez-vous que le fichier est un fichier texte (ajustez l'extension si nécessaire)
            file_path = os.path.join(corpus_folder, filename)
            # Lire le contenu du fichier
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            # Mettre à jour le dictionnaire de fréquence documentaire pour chaque mot unique dans le document
            unique_words = set(content.split())
            for word in unique_words:
                if word in document_frequency:
                    document_frequency[word] += 1
                else:
                    document_frequency[word] = 1
            # Incrémenter le compteur total de documents
            total_documents += 1
    # Calculer le score IDF pour chaque mot
    idf_scores = {}
    for word, frequency in document_frequency.items():
        idf = math.log(total_documents / (1 + frequency))  # Formule IDF
        idf_scores[word] = idf

    return idf_scores


def calculer_tfidf(repertoire="cleaned"):
    # Dictionnaire pour stocker la matrice TF de chaque fichier
    matrices_tf = TF(folder=repertoire)
    # Dictionnaire pour stocker le score IDF de chaque mot
    matrice_idf = IDF(corpus_folder=repertoire)
    # Récupérer tous les mots uniques dans tous les fichiers
    mots_uniques = set()
    for tf in matrices_tf.values():
        mots_uniques.update(tf.keys())
    # Construire la matrice TF-IDF avec toutes les valeurs remplies à zéro
    matrice_complete = {mot: [matrices_tf[nom_fichier].get(mot, 0) * matrice_idf[mot] for nom_fichier in matrices_tf] for mot in mots_uniques}
    return matrice_complete  # Retourner un dictionnaire


def transposer_matrice(matrice):
    # Nombre de lignes et de colonnes dans la matrice
    nb_lignes = len(matrice)
    nb_colonnes = len(matrice[0])
    # Initialiser une nouvelle matrice transposée avec les dimensions inversées
    matrice_transposee = [[0] * nb_lignes for _ in range(nb_colonnes)]
    # Remplir la matrice transposée
    for i in range(nb_lignes):
        for j in range(nb_colonnes):
            matrice_transposee[j][i] = matrice[i][j]
    return matrice_transposee

# Appeler la fonction et afficher les résultats
#matrice_tfidf_transposee = calculer_tfidf(repertoire="cleaned")
#for ligne in matrice_tfidf_transposee:
#    print(ligne)

def mots_moins_importants(repertoire="cleaned"):
    # Calculer la matrice TF-IDF
    matrice_tfidf = calculer_tfidf(repertoire=repertoire)
    # Trouver les mots dont le TF-IDF est toujours égal à 0
    mots_moins_importants = [mot for mot, scores in matrice_tfidf.items() if all(score == 0 for score in scores)]
    return mots_moins_importants

# Appeler la fonction et afficher les résultats
mots_non_importants = mots_moins_importants(repertoire="cleaned")
print("Mots les moins importants :")
print(mots_non_importants)


def mots_plus_importants(repertoire="cleaned"):
    # Calculer la matrice TF-IDF
    matrice_tfidf = calculer_tfidf(repertoire=repertoire)
    # Trouver le(s) mot(s) ayant le score TF-IDF le plus élevé
    mots_plus_importants = max(matrice_tfidf, key=lambda mot: max(matrice_tfidf[mot]))
    return mots_plus_importants

# Appeler la fonction et afficher les résultats
mot_plus_important = mots_plus_importants(repertoire="cleaned")
print("Mot le plus important :")
print(mot_plus_important)

def mots_plus_repetes_chirac(repertoire="cleaned", president="Chirac"):
    # Calculer la matrice TF pour les discours du président spécifié
    matrices_tf_chirac = {filename: tf for filename, tf in TF(folder=repertoire).items() if president in filename}
    # Concaténer tous les discours de Chirac pour obtenir une seule matrice TF
    tf_chirac_concatene = {}
    for tf in matrices_tf_chirac.values():
        for mot, freq in tf.items():
            if mot in tf_chirac_concatene:
                tf_chirac_concatene[mot] += freq
            else:
                tf_chirac_concatene[mot] = freq
    # Trouver le(s) mot(s) le(s) plus répété(s) par le président
    mots_plus_repetes_chirac = max(tf_chirac_concatene, key=tf_chirac_concatene.get)
    return mots_plus_repetes_chirac

# Appeler la fonction et afficher les résultats
mot_plus_repete = mots_plus_repetes_chirac(repertoire="cleaned", president="Chirac")
print("Mot le plus répété par Jacques Chirac :")
print(mot_plus_repete)

def presidents_parlant_de_mot(repertoire="cleaned", mot_recherche="Nation"):
    # Dictionnaire pour stocker la fréquence du mot spécifié par président
    frequence_par_president = {}
    # Parcourir les fichiers dans le dossier
    for filename in os.listdir(repertoire):
        if filename.endswith(".txt"):  # Assurez-vous que le fichier est un fichier texte (ajustez l'extension si nécessaire)
            file_path = os.path.join(repertoire, filename)
            # Lire le contenu du fichier
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            # Compter le nombre d'occurrences du mot spécifié
            frequence_mot = content.lower().count(mot_recherche.lower())
            # Extraire le nom du président du titre du fichier
            nom_president = filename.split('_')[1]  # Supposant que le nom du président est après la première occurrence de '_' dans le nom du fichier
            # Ajouter la fréquence au dictionnaire par président
            if nom_president in frequence_par_president:
                frequence_par_president[nom_president] += frequence_mot
            else:
                frequence_par_president[nom_president] = frequence_mot
    return frequence_par_president

def president_avec_plus_frequences(repertoire="cleaned", mot_recherche="Nation"):
    # Calculer la fréquence du mot spécifié par président
    frequence_par_president = presidents_parlant_de_mot(repertoire=repertoire, mot_recherche=mot_recherche)
    # Trouver le(s) président(s) qui a (ont) parlé du mot le plus de fois
    president_plus_frequent = max(frequence_par_president, key=frequence_par_president.get)
    frequence_maximale = frequence_par_president[president_plus_frequent]
    return president_plus_frequent, frequence_maximale

# Appeler la fonction et afficher les résultats
president, frequence = president_avec_plus_frequences(repertoire="cleaned", mot_recherche="Nation")
print(f"Président(s) ayant parlé de la 'Nation' : {president}")
print(f"Nombre maximum de répétitions : {frequence}")


def premier_president_parlant_de_mot(repertoire="cleaned", mots_recherche=["climat", "écologie"]):
    # Dictionnaire pour stocker le discours où chaque président a mentionné le mot spécifié
    discours_par_president = {}
    # Liste pour stocker l'ordre des présidents
    ordre_presidents = []
    # Parcourir les fichiers dans le dossier
    for filename in sorted(os.listdir(repertoire)):
        if filename.endswith(".txt"):  # Assurez-vous que le fichier est un fichier texte (ajustez l'extension si nécessaire)
            file_path = os.path.join(repertoire, filename)
            # Lire le contenu du fichier
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read().lower()
            # Vérifier si le mot spécifié est mentionné dans le discours
            for mot_recherche in mots_recherche:
                if mot_recherche.lower() in content:
                    # Extraire le nom du président du titre du fichier
                    nom_president = filename.split('_')[1]  # Supposant que le nom du président est après la première occurrence de '_' dans le nom du fichier
                    # Enregistrer le discours et le nom du président
                    if nom_president not in discours_par_president:
                        discours_par_president[nom_president] = content
                        ordre_presidents.append(nom_president)
    if not ordre_presidents:
        return None  # Aucun président n'a mentionné les mots spécifiés
    # Trouver le premier président à parler du mot spécifié
    premier_president = ordre_presidents[0]
    return premier_president

# Appeler la fonction et afficher les résultats
premier_president = premier_president_parlant_de_mot(repertoire="cleaned", mots_recherche=["climat", "écologie"])
if premier_president is not None:
    print(f"Premier président à parler du 'climat' et/ou de 'l’écologie' : {premier_president}")
else:
    print("Aucun président n'a mentionné les mots spécifiés.")


def mots_communs_entre_presidents(repertoire="cleaned", mots_non_importants=None):
    if mots_non_importants is None:
        mots_non_importants = set()  # Si aucun ensemble de mots non importants n'est fourni, on le crée comme un ensemble vide
    # Dictionnaire pour stocker les ensembles de mots de chaque président
    ensembles_mots_par_president = {}
    # Parcourir les fichiers dans le dossier
    for filename in os.listdir(repertoire):
        if filename.endswith(".txt"):  # Assurez-vous que le fichier est un fichier texte (ajustez l'extension si nécessaire)
            file_path = os.path.join(repertoire, filename)
            # Lire le contenu du fichier
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read().lower()
            # Extraire le nom du président du titre du fichier
            nom_president = filename.split('_')[1]  # Supposant que le nom du président est après la première occurrence de '_' dans le nom du fichier
            # Diviser la chaîne en mots
            mots = content.split()
            # Ajouter l'ensemble de mots au dictionnaire
            if nom_president not in ensembles_mots_par_president:
                ensembles_mots_par_president[nom_president] = set(mots) - mots_non_importants
            else:
                ensembles_mots_par_president[nom_president] |= set(mots) - mots_non_importants
    # Trouver l'intersection des ensembles de mots de tous les présidents
    mots_communs = set.intersection(*ensembles_mots_par_president.values())
    return mots_communs

# Appeler la fonction et afficher les résultats
mots_communs = mots_communs_entre_presidents(repertoire="cleaned", mots_non_importants={"non", "importants"})
print("Mots communs entre tous les présidents (hormis les mots non importants) :")
print(mots_communs)


#print(TF(folder="cleaned"))
#print(IDF(corpus_folder="cleaned"))
#print(calculer_tfidf(repertoire="cleaned"))cleaned"))