#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os

def main():
    parser = argparse.ArgumentParser(
        description="Visualiser la moyenne d'heures d'addiction par pays (top 20)"
    )
    parser.add_argument(
        "input_file",
        help="Chemin vers le fichier TSV issu du reducer (country<TAB>avg_hours)"
    )
    args = parser.parse_args()

    # Lecture des données
    df = pd.read_csv(
        args.input_file,
        sep='\t',
        header=None,
        names=['country', 'avg_hours']
    )

    # Tri décroissant et sélection des 20 premiers
    df_top20 = df.sort_values(by='avg_hours', ascending=False).head(20)

    # Création du graphique
    plt.figure(figsize=(12, 6))
    plt.bar(df_top20['country'], df_top20['avg_hours'])
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Pays')
    plt.ylabel("Moyenne d'heures d'addiction")
    plt.title("Top 20 des pays par moyenne d'heures d'utilisation")
    plt.tight_layout()

    # Définition du nom de fichier de sortie et son chemin absolu
    output_filename = 'addiction_top20.png'
    output_path = os.path.abspath(output_filename)

    # Sauvegarde et affichage
    plt.savefig(output_path)
    plt.show()
    print(f"Graphique enregistré sous : {output_path}")

if __name__ == "__main__":
    main()
