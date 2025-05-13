# Pour commencer
## Installation
### Prérequis
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installation
1. Recuperer l'image Docker d'apache hadoop
```bash
docker pull apache/hadoop:3.4.1
```
2. Creer le contenaire docker
```bash
 docker run -d --name hadoop-shell -p 9870:9870 -p 8088:8088 apache/hadoop:3.4.1 tail -f /dev/null
```
3. Lancer le shell Hadoop
```bash
docker exec -it hadoop-shell bash
```
4. Lancer le serveur HDFS
```bash
/opt/hadoop/bin/hdfs namenode -format
```
ou bien
```bash
export HADOOP_HOME=/opt/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
```
```bash
start-dfs.sh
```
5. Lancer le serveur YARN
```bash
start-yarn.sh
```
6. Lancer le serveur MapReduce
```bash
start-mapred.sh
```
7. Acceder a l'interface web de Hadoop
- HDFS : http://localhost:9870
- YARN : http://localhost:8088
- MapReduce : http://localhost:8088/mapreduce
- JobHistory : http://localhost:19888
9. Acceder au shell Hadoop
```bash
hadoop fs -ls /
```
