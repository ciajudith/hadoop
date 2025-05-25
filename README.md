# Hadoop Docker Demo Repository

> Aperçu du dépôt et du projet Hadoop sous Docker

>**Date :** `2025-05-24`

---

## Présentation

Ce dépôt propose une démonstration simple et pédagogique de l’utilisation de Hadoop dans un environnement conteneurisé Docker. Il contient :

* Une configuration Docker pour exécuter Hadoop.
* Deux démonstrations MapReduce :

   1. WordCount classique sur un fichier texte simple.
   2. Analyse de données CSV (`addiction.csv`) pour calculer une statistique par pays via Hadoop Streaming.
* Un script d’analyse externe qui exploite la sortie du cluster pour générer des visualisations.

---

## Arborescence du dépôt

```
hadoop/
├─ hadoop-demo/
│  ├─ data/            # Dataset CSV (`addiction.csv`)
   │  └─ addiction/
   │     └─ addiction.csv
│  └─ scripts/         # Scripts Hadoop Streaming et analyse
│     ├─ mapper.py     # Mapper pour streaming
│     ├─ reducer.py    # Reducer pour streaming
│     └─ analysis.py   # Analyse & visualisation Python
├─ getting-started.md  # Guide rapide de démarrage Docker + Hadoop
├─ scripts.txt         # Instructions pour générer les scripts
└─ README.md           # Documentation principale (aperçu du projet)
```

---

## Prérequis

* **Docker** (version 20+).
* Ports **9870** (HDFS UI) et **8088** (YARN UI) libres.

---

## Installation

1. Télécharger l’image Docker Hadoop.
2. Lancer un conteneur avec montage du répertoire `data/`.
3. Formater le NameNode et démarrer les services HDFS et YARN.
4. Vérifier le bon démarrage des processus Hadoop.

*Voir* `getting-started.md` pour les commandes détaillées.

---

## Démonstrations MapReduce

### Demo 1 : WordCount classique

* **Objectif :** compter le nombre d’occurrences de chaque mot dans un fichier texte.
* **Flux :**

   1. Charger un fichier d’exemple (titre, lignes de texte) dans HDFS.
   2. Lancer le job WordCount fourni par Hadoop.
   3. Consulter les résultats (tri, top N).
   4. Supprimer les fichiers de sortie pour nettoyer l’environnement.

### Demo 2 : Hadoop Streaming sur `addiction.csv`

* **Objectif :** calculer la moyenne du temps d’utilisation quotidienne des réseaux sociaux par pays.
* **Dataset** :

   * Chaque ligne contient : Identifiant étudiant, âge, genre, niveau académique, pays, heures moyennes par jour, plateforme préférée, impact académique, heures de sommeil, score mental, statut relationnel, conflits, indice d’addiction.
* **Flux :**

   1. Charger `addiction.csv` dans HDFS.
   2. Exécuter un job Hadoop Streaming avec un mapper (extraction pays + heures) et un reducer (calcul de la moyenne).
   3. Récupérer la sortie pour l’analyse.

---

## Données (`addiction.csv`)

| Champ                          | Description                                |
|--------------------------------|--------------------------------------------|
| Student\_ID                    | Identifiant unique de l’étudiant           |
| Age                            | Âge en années                              |
| Gender                         | Genre (Male/Female)                        |
| Academic\_Level                | Niveau d’études (Undergraduate, Master…)   |
| Country                        | Pays de résidence                          |
| Avg\_Daily\_Usage\_Hours       | Heures moyennes d’utilisation par jour     |
| Most\_Used\_Platform           | Plateforme la plus utilisée                |
| Affects\_Academic\_Performance | Impact sur la réussite académique (Yes/No) |
| Sleep\_Hours\_Per\_Night       | Moyenne d’heures de sommeil par nuit       |
| Mental\_Health\_Score          | Score d’état mental (échelle interne)      |
| Relationship\_Status           | Statut relationnel                         |
| Conflicts\_Over\_Social\_Media | Nombre de conflits causés                  |
| Addicted\_Score                | Indice global d’addiction (0–10)           |

---

## Analyse et visualisation hors-cluster

Le script `analysis.py` (Python) :

1. Importe la sortie du reducer en tant que tableau.
2. Calcule et affiche la statistique par pays.
3. Génère un graphique (Matplotlib) pour visualiser les moyennes.

---

## Nettoyage

* Arrêt et suppression du conteneur Docker Hadoop.
* Suppression de l’image Docker.

---

## Ressources

* Documentation officielle Hadoop : [https://hadoop.apache.org/](https://hadoop.apache.org/)
* Documentation Docker : [https://docs.docker.com/](https://docs.docker.com/)
* Guides internes : `getting-started.md`, `scripts.txt`

---

*© ciajudith*
