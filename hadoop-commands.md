# Hadoop Commands

## For the first demo
Cette démonstration montre comment utiliser Hadoop pour effectuer un traitement MapReduce simple sur un fichier texte. Nous allons créer un fichier texte, le charger dans HDFS, exécuter un job MapReduce pour compter les mots, et afficher les résultats.

### Creer un fichier texte d'exemple et le charger dans HDFS:
hdfs dfs -mkdir -p /user/root/input

cat > sample.txt <<EOF
bonjour Hadoop
bonjour monde
hello world
EOF

hdfs dfs -put -f sample.txt /user/root/input

### Lister les fichiers dans HDFS:
hdfs dfs -ls /user/root/input
### Exécuter un job MapReduce pour compter les mots:
hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar wordcount /user/root/input /user/root/output

### Lister les fichiers de sortie:
hdfs dfs -ls /user/root/output

### Afficher le contenu du fichier de sortie:
hdfs dfs -cat /user/$(whoami)/output/part-r-00000

### Afficher les 10 premiers mots triés par ordre décroissant:
hdfs dfs -cat /user/root/output/part-r-00000 | sort -nr | head -n 10
### Afficher les 10 premiers mots triés par ordre croissant:
hdfs dfs -cat /user/root/output/part-r-00000 | sort | head -n 10


```
hdfs fsck /user/root/input/sample.txt -files -blocks -racks
```
Cette commande permet de vérifier l'intégrité du fichier dans HDFS.

### Supprimer les fichiers de sortie:
hdfs dfs -rm -r -f /user/$(whoami)/output

## New demo
hdfs dfs -cat /user/demo/input/u.data | head -n 10

hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar wordcount /user/demo/input/u.data /user/demo/ratings-count

hdfs dfs -ls /user/demo/ratings-count &&
hdfs dfs -cat /user/demo/ratings-count/part-r-00000 | sort -nr | head -n 10