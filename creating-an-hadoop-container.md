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
Cette commande va creer un conteneur Docker avec le nom `hadoop-debug` et l'ouvrir dans un terminal interactif(root@containerid). Les ports 9870 et 8088 sont exposés pour accéder à l'interface web de Hadoop.
3. Faire certaines configurations
```bash
echo "HADOOP_HOME = $HADOOP_HOME"
which hdfs
which yarn
```
Cette commande va afficher le chemin d'installation de Hadoop et les chemins des executables `hdfs` et `yarn`.
L'output est le suivant:
``` bash
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

Dans le cas ou on veut executer le container hadoop lorsqu'il est arrete, on peut utiliser la commande suivante:
```bash
docker start hadoop-debug
docker exec -it hadoop-debug bash 
```
