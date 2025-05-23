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
   docker run --name hadoop -v "D:\python\bigdata\hadoop\hadoop-demo\ml-100k\ml-100k:/data/ml-100k" -it -p 9870:9870 -p 8088:8088 silicoflare/hadoop:amd bash
   ```
   Cela montera le répertoire `ml-100k` de votre machine hôte dans le conteneur Hadoop à l'emplacement `/data/ml-100k`. Ainsi, vous pourrez accéder aux fichiers de ce répertoire depuis le conteneur.
   Les configurations du numero 3 s'appliquent aussi ici.

5. Création et déplacement d'un élément dans HDFS
   ```
   hdfs dfs -mkdir -p /user/demo/input
   hdfs dfs -put -f /data/ml-100k/u.data /user/demo/input
   ```

### Acceder a l'interface web de Hadoop
- HDFS : http://localhost:9870
- YARN : http://localhost:8088
