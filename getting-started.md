# Documentation : Hadoop sur Docker

> Guide complet pour installer, configurer et utiliser Hadoop dans un conteneur Docker  
> Date : `2025-05-24`

---

## Table des matières

- [1. Introduction](#1-introduction)
- [2. Prérequis](#2-prérequis)
- [3. Installation du conteneur Hadoop Docker](#3-installation-du-conteneur-hadoop-docker)
  - [3.1 Récupérer l’image Docker](#31-récupérer-limage-docker)
  - [3.2 Créer et lancer le conteneur](#32-créer-et-lancer-le-conteneur)
  - [3.3 Configurer le conteneur](#33-configurer-le-conteneur)
  - [3.4 Reprendre un conteneur existant](#34-reprendre-un-conteneur-existant)
  - [3.5 Montage de volume depuis l’hôte](#35-montage-de-volume-depuis-lhôte)
- [4. Gestion de fichiers dans HDFS](#4-gestion-de-fichiers-dans-hdfs)
- [5. Exécution de démonstrations MapReduce](#5-exécution-de-démonstrations-mapreduce)
    - [5.1 Démo 1 : WordCount simple](#51-démo-1-wordcount-simple)
    - [5.2 Démo 2 : Job MapReduce personnalisé (streaming)](#52-démo-2-job-mapreduce-personnalisé-streaming)
- [6. Analyse des résultats externes](#6-analyse-des-résultats-externes)
- [7. Accès aux interfaces web Hadoop](#7-accès-aux-interfaces-web-hadoop)
- [8. Nettoyage et suppression](#8-nettoyage-et-suppression)
- [9. Conclusion](#9-conclusion)

## 1. Introduction

Ce document décrit pas à pas :

- La mise en place d’un environnement Hadoop complet dans un conteneur Docker.
- La gestion des fichiers via HDFS.
- L’exécution de jobs MapReduce (exemples et streaming).
- L’analyse des résultats hors du cluster.
- L’accès aux interfaces web de Hadoop.

---

## 2. Prérequis

- **Docker** installé ([guide officiel](https://docs.docker.com/get-docker/)).
- **Ports** libres :
    - 9870 pour l’interface HDFS 
    - 8088 pour l’interface YARN

---

## 3. Installation du conteneur Hadoop Docker

### 3.1 Récupérer l’image Docker

```bash
docker pull silicoflare/hadoop:amd
```

### 3.2 Créer et lancer le conteneur

```bash
docker run --name hadoop-debug   -it -p 9870:9870 -p 8088:8088   silicoflare/hadoop:amd bash
```

- **`--name hadoop-debug`** : nom du conteneur
- **`-p 9870:9870`**, **`-p 8088:8088`** : exposition des ports pour les UI Hadoop

### 3.3 Configurer le conteneur

1. Vérifier les variables et exécutables Hadoop :

   ```bash
   echo "HADOOP_HOME = $HADOOP_HOME"
   which hdfs
   which yarn
   ```

2. Formater le NameNode et démarrer HDFS :

   ```bash
   hdfs namenode -format
   hdfs --daemon start namenode
   hdfs --daemon start datanode
   ```

3. Démarrer YARN :

   ```bash
   yarn --daemon start resourcemanager
   yarn --daemon start nodemanager
   ```

4. Vérifier le démarrage avec `jps` :

   ```bash
   jps
   ```

### 3.4 Reprendre un conteneur existant

Si le conteneur est arrêté :

```bash
docker start hadoop-debug
docker exec -it hadoop-debug bash
```

### 3.5 Montage de volume depuis l’hôte

Pour travailler avec des données locales :

```bash
docker run --name hadoop -v "/chemin/local/data:/data/data" -it -p 9870:9870 -p 8088:8088 silicoflare/hadoop:amd bash
```
Chez moi, cela donne :

```bash
docker run --name hadoop -v "D:\python\bigdata\hadoop\hadoop-demo\data:/data/data" -v "D:\python\bigdata\hadoop\hadoop-demo\scripts:/data/scripts" -it -p 9870:9870 -p 8088:8088 silicoflare/hadoop:amd bash
```

- **`/chemin/local/data`** : dossier source sur la machine hôte
- **`/data/data`** : point de montage dans le conteneur
Puis, refaire le étapes de configuration du conteneur.
---

## 4. Gestion de fichiers dans HDFS

### 4.1 Création et déplacement

Créer un répertoire et y placer un fichier (ici `addiction.csv` qui sera utilisé pour les démonstrations) :

```bash
hdfs dfs -mkdir -p /user/demo/input
hdfs dfs -put -f /data/data/addiction/addiction.csv /user/demo/input
```

Spécifier un size block spécifique :
Ici, nous avons spécifié la taille du bloc à 1 Mo (1048576 octets) lors du déplacement du fichier. Cela peut être utile pour optimiser le stockage et le traitement des données dans HDFS.


```bash
hdfs dfs -mkdir -p /user/demo/testinput
hdfs dfs -D dfs.blocksize=1048576 -put -f /data/data/addiction/addiction.csv /user/demo/testinput
```

### 4.2 Vérification d’intégrité

```bash
hdfs fsck /user/demo/input/addiction.csv   -files -blocks -locations -racks

hdfs fsck /user/demo/testinput/addiction.csv   -files -blocks -locations -racks
```
Cette commande permet de vérifier l'intégrité du fichier dans HDFS, en affichant les informations sur les fichiers, les blocs et les racks. Elle est utile pour s'assurer que le fichier a été correctement chargé dans HDFS et qu'il n'y a pas de problèmes d'intégrité.


### 4.3 Liste et consultation

- **Lister** :

  ```bash
  hdfs dfs -ls /user/demo/input
  ```

- **Afficher** :

  ```bash
  hdfs dfs -cat /user/demo/input/addiction.csv | head -n 10
  ```

---

## 5. Exécution de démonstrations MapReduce

### 5.1 Démo 1 : WordCount simple

1. **Préparer un fichier d’exemple** :

    ```bash
    cat > sample.txt <<EOF
    bonjour Hadoop
    bonjour monde
    hello world
    EOF
    hdfs dfs -mkdir -p /user/root/input
    hdfs dfs -put -f sample.txt /user/root/input
    ```

2. **Vérifier** :

    ```bash
    hdfs fsck /user/root/input/sample.txt -files -blocks -racks
    hdfs dfs -ls /user/root/input
    hdfs dfs -cat /user/root/input/sample.txt
    ```

3. **Lancer le job** :

    ```bash
    hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar wordcount /user/root/input /user/root/output
    ```

4. **Consulter les résultats** :

    ```bash
    hdfs dfs -ls /user/root/output
    hdfs dfs -cat /user/root/output/part-r-00000
    ```

5. **Top 10 mots** :

    ```bash
    hdfs dfs -cat /user/root/output/part-r-00000 | sort -nr | head -n 10
    hdfs dfs -cat /user/root/output/part-r-00000 | sort      | head -n 10
    ```

6. **Nettoyage** :

    ```bash
    hdfs dfs -rm -r -f /user/root/output
    ```

### 5.2 Démo 2 : Job MapReduce personnalisé (streaming)

1. **Préparation des scripts** *(dans `/data/data`)* :

    ```bash
    cd /data/data
    ```
    Les commandes cat de création des fichiers mapper.py et reducer.py sont dans le fichier `scripts.txt`.

    ```bash
    chmod +x mapper.py reducer.py
    ```
   Ces 2 précédentes commandes ne sont importantes que si vous n'avez pas monté le volume depuis l’hôte.

2. **Exécution** :
    
    ```bash
    hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar -input  /user/demo/input/addiction.csv       -output /user/demo/output       -mapper /data/data/mapper.py       -reducer /data/data/reducer.py       -file   /data/data/mapper.py       -file   /data/data/reducer.py
    ```
   Dans le cas où  vous avez monté le volume depuis l’hôte, et utilisé ces scripts .py au lieu de les créer directement dans le container, utilisez cette commande:
    ```bash
    hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar -input /user/demo/input/addiction.csv -output /user/demo/output -mapper "python3 mapper.py" -reducer "python3 reducer.py" -file /data/scripts/mapper.py -file /data/scripts/reducer.py
    ```
   Elle permet d'exécuter les scripts Python directement dans le conteneur, en utilisant `python3` pour le mapper et le reducer.

3. **Résultats** :

    ```bash
    hdfs dfs -ls /user/demo/output
    hdfs dfs -cat /user/demo/output/part-00000 | sort -k2,2nr | head -n 10
    ```

---

## 6. Analyse des résultats externes

Pour traiter et visualiser les résultats hors de Hadoop :

1. **Installer les dépendances** :

   Dans le conteneur, installez les bibliothèques nécessaires :
    ```bash
    pip install pandas matplotlib
    ```
   Les commandes 2 et 3 seront exécutés dans le repertoire `/data/data/addiction/`.
   ```bash
    cd /data/data/addiction/
   ```

2. **Télécharger les résultats** :

   Récupérer le fichier de sortie du job MapReduce :

   ```bash
   hdfs dfs -get /user/demo/output/part-00000 ./part-00000
   ```
3. **Exécuter le script d’analyse** :
    ```bash
    python3 /data/scripts/analysis.py part-00000
    ```

> Le script `analysis.py` doit lire le fichier `part-00000`, générer un graphique et l’enregistrer sous `addiction_top20.png.png`.
Vous pouvez adapter le script pour vos propres besoins d'analyse.

4. **Visualiser les résultats** :

   Ouvrir le fichier `addiction_top20.png` pour voir les résultats de l'analyse.
---

## 7. Accès aux interfaces web Hadoop

- **HDFS UI** : [http://localhost:9870](http://localhost:9870)
- **YARN UI** : [http://localhost:8088](http://localhost:8088)

---

## 8. Nettoyage et suppression

Pour arrêter et supprimer le conteneur :

```bash
docker stop hadoop-debug
docker rm hadoop-debug
```

Pour supprimer l’image :

```bash
docker rmi silicoflare/hadoop:amd
```

---
## 9. Conclusion
Ce guide vous a permis de mettre en place un environnement Hadoop complet dans un conteneur Docker, de gérer des fichiers dans HDFS, d'exécuter des jobs MapReduce et d'analyser les résultats. Vous pouvez maintenant adapter ces étapes pour vos propres projets et données.


**Fin de la documentation.**
