#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import argparse

def main():
    # 1) Analyse des arguments
    parser = argparse.ArgumentParser(
        description="Visualiser la moyenne d'heures d'addiction par étudiant et par pays"
    )
    parser.add_argument(
        "input_file",
        help="Chemin vers le fichier TSV issu du reducer (country<TAB>avg_hours)"
    )
    args = parser.parse_args()

    # 2) Lecture des données
    df = pd.read_csv(
        args.input_file,
        sep='\t',
        header=None,
        names=['country', 'avg_hours']
    )

    # 3) Tri décroissant des moyennes
    df_sorted = df.sort_values(by='avg_hours', ascending=False)

    # 4) Création du graphique
    plt.figure(figsize=(12, 6))
    plt.bar(df_sorted['country'], df_sorted['avg_hours'])
    plt.xticks(rotation=90)
    plt.xlabel('Pays')
    plt.ylabel("Moyenne d'heures d'addiction")
    plt.title("Moyenne d'heures par étudiant et par pays")
    plt.tight_layout()

    # 5) Affichage
    plt.savefig('addiction_analysis.png')
    plt.show()
    print("Image successfully created")

if __name__ == "__main__":
    main()
