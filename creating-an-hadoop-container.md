# Pour commencer

## Creation d'un container hadoop

### Prerequis
- [Docker](https://docs.docker.com/get-docker/)

### Installation
1. Recuperer l'image Docker d'apache hadoop

    ```bash
    docker pull silicoflare/hadoop:amd
    ```
2. Creer le contenaire docker
    ```bash
    docker run --name hadoop-debug -it -p 9870:9870 -p 8088:8088 silicoflare/hadoop:amd bash
    ```
    Cette commande va créer un conteneur Docker avec le nom `hadoop-debug` et l'ouvrir dans un terminal interactif(root@containerid). Les ports 9870 et 8088 sont exposés pour accéder à l'interface web de Hadoop.

3. Faire certaines configurations

    ```bash
    echo "HADOOP_HOME = $HADOOP_HOME"
    which hdfs
    which yarn
    ```
   
    Cette commande va afficher le chemin d'installation de Hadoop et les chemins des executables `hdfs` et `yarn`.
    L'output est le suivant:
    ``` 
    HADOOP_HOME = /usr/local/hadoop
    /usr/local/hadoop/bin/hdfs
    /usr/local/hadoop/bin/yarn
    
    ```
    
    Maintenant, nous allons formatter le namenode et demarrer les services HDFS et YARN.
    ```bash
    hdfs namenode -format
    hdfs --daemon start namenode
    hdfs --daemon start datanode 
    yarn --daemon start resourcemanager
    yarn --daemon start nodemanager
    ```
    
    La commande `jps` permet de verifier si les services sont bien demarres:
    ```bash
    jps
    ```
    
    Dans le cas ou on veut executer le container hadoop lorsqu'il est arreté, on peut utiliser la commande suivante:
    ```bash
    docker start hadoop-debug
    docker exec -it hadoop-debug bash 
    ```
4. Créer un conteneur Hadoop avec un volume monté

   Pour créer un conteneur Hadoop avec un volume monté, vous pouvez utiliser la commande suivante :
   ```bash
   docker run --name hadoop -v "D:\python\bigdata\hadoop\hadoop-demo\data:/data/data" -it -p 9870:9870 -p 8088:8088 silicoflare/hadoop:amd bash
    ```
   Dans cette commande, le répertoire `D:\python\bigdata\hadoop\hadoop-demo\data` de votre machine hôte est monté dans le conteneur Hadoop à l'emplacement `/data/data`. 
   Vous pouvez remplacer ce chemin par le chemin de votre choix sur votre machine hôte.
   Ainsi, vous pourrez accéder aux fichiers de ce répertoire depuis le conteneur. 
   Les configurations du numero 3 s'appliquent aussi ici.

5. Création et déplacement d'un élément dans HDFS
   ```
   hdfs dfs -mkdir -p /user/demo/input
   hdfs dfs -put -f /data/data/addiction/addiction.csv /user/demo/input
   ```
    Cette commande crée un répertoire `/user/demo/input` dans HDFS et y déplace le fichier `addiction.csv` depuis le répertoire monté `/data/data` du conteneur.
   
   ```
   hdfs dfs -mkdir -p /user/demo/testinput
   hdfs dfs -D dfs.blocksize=1048576 -put -f /data/data/addiction/addiction.csv /user/demo/testinput
   ```
   Ici, nous avons spécifié la taille du bloc à 1 Mo (1048576 octets) lors du déplacement du fichier. Cela peut être utile pour optimiser le stockage et le traitement des données dans HDFS.
6. Verifier l'intégrité du fichier dans HDFS
   ```
   hdfs fsck /user/demo/input/addiction.csv -files -blocks -locations -racks
   hdfs fsck /user/demo/testinput/addiction.csv -files -blocks -locations -racks

   ```
   Cette commande permet de vérifier l'intégrité du fichier dans HDFS, en affichant les informations sur les fichiers, les blocs et les racks. Elle est utile pour s'assurer que le fichier a été correctement chargé dans HDFS et qu'il n'y a pas de problèmes d'intégrité.


### Job MapReduce
#### But: montrer le traitement distribué de Hadoop en action
1. Preparons nos scripts dans le répertoire `/data/data` monté dans le conteneur.
   ```bash
   cd /data/data
   ```
   Créons  le fichier `mapper.py` et `reducer.py`
   (Les scripts de créations sont dans le fichier `scripts.txt` dans le projet)
   Rendons les scripts exécutables:
   ```bash
   chmod +x /data/mapper.py /data/reducer.py
   ```

2. Exécuter le job MapReduce
   ```bash
   hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar -input /user/demo/input/addiction.csv -output /user/demo/output -mapper /data/mapper.py -reducer /data/reducer.py -file /data/mapper.py -file /data/reducer.py
   ```
3. Lister les fichiers de sortie:
   ```bash
   hdfs dfs -ls /user/demo/output
   ```
4. Afficher le contenu du fichier de sortie:
   ```bash
    hdfs dfs -cat /user/demo/output/part-00000
    ```
5. Afficher les 10 premiers mots triés par ordre décroissant sur la deuxieme colonne:
   ```bash
   hdfs dfs -cat /user/demo/output/part-00000 | sort -k2,2nr | head -n 10
   ```
   

### Acceder a l'interface web de Hadoop
- HDFS : http://localhost:9870
- YARN : http://localhost:8088
