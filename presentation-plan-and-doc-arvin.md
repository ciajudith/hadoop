# Explorer Hadoop: du stockage aux traitements
## Introduction
Hadoop est un framework open source qui permet de stocker et de traiter de très grands volumes de données de manière distribuée, grace aux clusters de machines.
Un cluster de machine, qu'est ce que c'est? Il désigne un ensemble de serveurs physiques ou virtuels interconnectés et coordonnés pour fonctionner comme une seule entité: 
- chaque machine ou noeud participe au stockage et au calcul.
- si une machine tombe en panne, les autres continuent de fonctionner.
Hadoop gère aussi bien les données structurées (tableurs, bases de données) que non structurées (logs, documents texte, images), 
grâce à son système de fichiers distribué (HDFS) et à son moteur de traitement parallèle (YARN + MapReduce).
### Objectifs - Plan
Dans cette présentation, nous allons  explorer les concepts clés d’Hadoop et son positionnement dans l’écosystème Big Data,
comprendre l’architecture : HDFS pour le stockage et YARN pour la gestion des ressources, 
découvrir le modèle MapReduce : introduction au paradigme « map » et « reduce », et façon dont Hadoop orchestre l’exécution de vos fonctions métier sur chaque nœud.
et enfin voir en pratique une démonstration WordCount, l’exemple classique de MapReduce, pour illustrer en direct comment écrire, lancer et visualiser un job sur un cluster Hadoop.

## Plan de la présentation
1. Pourquoi Hadoop?
2. Architecture d'Hadoop et ses composants
3. Exécution de Hadoop
4. Flux d'un traitement (job) MapReduce
5. Cas d'utilisation
6. Démonstration: WordCount
7. Bénéfices et limites
8. Conclusion
9. Questions/Perspectives

## Pourquoi Hadoop?
Pour bien comprendre l’intérêt d’Hadoop, considérons d’abord les défis posés par l'avenement du Big Data, puis voyons pourquoi et comment Hadoop y apporte une solution cohérente.
Nous connaissons tous deja les 5 grands V: Volume, Vélocité, Variété, Véracité et Valeur.
Les bases de données relationnelles pour ne pas dire et entrepot de données traditionnels montrent rapidement leurs limites : 
- ils ne sont pas adaptées pour stocker et traiter ces données massives.
- ils sont souvent rigides et nécessitent des schémas prédéfinis, ce qui complique l’intégration de données non structurées.
- ils sont coûteux à mettre en place et à maintenir, surtout pour les entreprises qui n’ont pas encore de besoins massifs en données.
Les défis qui en resultent sont donc nombreux:
- **Stockage des données**: Comment stocker des pétaoctets de données de manière fiable et évolutive?
- **Sécurité des données**: Comment garantir la sécurité et la confidentialité des données sensibles?
- **Qualité & validation des données**:  Comment s’assurer de la qualité et de la véracité des données?
- **Analyse des données**: Comment traiter et analyser ces données massives en temps réel?

Alors comment Hadoop répond à ces défis?
L'arrivée d'Hadoop coincide avec l'explosion du Big Data et des besoins d'analyse de données massives.
Pour chacun de ces défis, Hadoop propose une solution adaptée:

| Défi                     | Solution Hadoop                                                                                                                                                                                                                                        |
|--------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Stockage des données** | • **HDFS** : découpe en blocs (64/128 Mo) et **réplication** (×3) sur un cluster de machines peu coûteuses. → Evolutivité horizontale et tolérance aux pannes.                                                                                         |
| **Sécurité des données** | • **Kerberos** pour l’authentification<br>• **Apache Ranger/Sentry** pour des politiques d’accès fines<br>• **Chiffrement** au repos (HDFS Encryption Zones) et en transit (SSL/TLS).                                                                  |
| **Qualité & validation** | • **Schema-on-read** : pas de schéma imposé à l’écriture<br>• **NiFi**, **Sqoop** pour ingestion contrôlée<br>• **Hive Metastore** & **Atlas** pour catalogage et traçabilité<br>• Jobs de nettoyage avec **MapReduce** ou **Spark**.                  |
| **Analyse des données**  | • **MapReduce** : calcul batch distribué, relance automatique des tâches échouées<br>• **YARN** : ordonnanceur de ressources (CPU/mémoire) sur le cluster<br>• Écosystème SQL (Hive, Presto) et calcul en mémoire (Spark) pour accélérer les requêtes. |

Hadoop regroupe donc plusieurs outils et technologies qui permettent de relever ces défis.
Il est important de noter que Hadoop n’est pas une solution unique, mais un écosystème de plusieurs composants qui travaillent ensemble pour répondre aux besoins du Big Data.
Nous allons ainsi explorer ses principaux composants et leur rôle dans l’architecture globale.

## Architecture d'Hadoop et ses composants
Hadoop repose sur 4 modules principaux:
- **HDFS** (Hadoop Distributed File System)
- **YARN** (Yet Another Resource Negotiator)
- **MapReduce**
- **Hadoop Common**
### HDFS
HDFS est le système de fichiers distribué d'Hadoop, conçu pour stocker de grandes quantités de données structurées ou non sur un cluster de machines.
Il est basé sur le principe de la réplication des données pour assurer la tolérance aux pannes et la disponibilité.
- **Namenode**: le maître qui gère la structure du système de fichiers et les métadonnées.
- **Datanodes**: les esclaves qui stockent réellement les données.
- **Blocs**: les fichiers sont découpés en blocs de 64 ou 128 Mo, qui sont répliqués (x3 par defaut) sur plusieurs datanodes pour assurer la redondance.

- **Écriture et lecture**: les données sont écrites sur le namenode, qui les répartit sur les datanodes. Lors de la lecture, le client interroge le namenode pour savoir où se trouvent les blocs et les lit directement à partir des datanodes.
- **Tolérance aux pannes**: si un datanode tombe en panne, HDFS continue de fonctionner grâce à la réplication des blocs sur d'autres datanodes. Le namenode détecte la panne et réplique les blocs manquants sur d'autres datanodes.
- **Scalabilité**: HDFS est conçu pour être évolutif, permettant d'ajouter facilement de nouveaux datanodes au cluster pour augmenter la capacité de stockage et de traitement.

### YARN
YARN est le gestionnaire de ressources d'Hadoop, qui permet de gérer les ressources du cluster et d'exécuter des applications distribuées.
Il est responsable de la planification et de l'exécution des tâches sur le cluster, en allouant les ressources nécessaires (CPU, mémoire) aux applications.
On appelle **container**: une unité de ressources (CPU, mémoire) allouée par YARN pour exécuter une tâche.
Il est composé de trois principaux éléments:
- **ResourceManager**: le maître qui gère les ressources du cluster et planifie les tâches.
- **NodeManager**: les esclaves qui gèrent les ressources sur chaque datanode et exécutent les tâches.
- **ApplicationMaster**: une instance par application qui gère l'exécution de l'application sur le cluster.

## Exécution de Hadoop
Hadoop offre 2 modes d'execution principaux:
- **Mode Local**: Hadoop s'exécute sur une seule machine, sans HDFS. Il est principalement utilisé pour le développement et les tests.
- **Mode Cluster**: Hadoop s'exécute sur un cluster de machines, avec HDFS pour le stockage distribué. C'est le mode utilisé pour le traitement de grandes quantités de données.
- **Mode Pseudo-Distribué**:(single-node “cluster”) Hadoop s'exécute sur une seule machine, mais simule un environnement distribué. C'est un bon compromis pour le développement et les tests avant de passer en mode cluster.
  Tout ceci pour expliquer qu'on peut installer et utiliser Hadoop sur nos pc sans disposer d'un vrai cluster de plusieurs machines.

## Flux d'un traitement (job) MapReduce

Objectif : Montrer comment Hadoop traite un job de type MapReduce.

Étapes du traitement MapReduce :

-**Input Splits** : Le fichier d'entrée est découpé en blocs (splits).

-**Map Phase** : Chaque split est traité en parallèle pour générer des paires clé/valeur intermédiaires.

-**Shuffle & Sort**: Les sorties intermédiaires sont redistribuées et triées par clé.

-**Reduce Phase** : Agrégation des résultats par clé.

-**Output** : Résultat final écrit dans HDFS.

## Cas d'utilisation

Objectif : Montrer que Hadoop est utilisé dans de nombreux secteurs.


-**Web Analytics** : traitement des logs de millions de visites web.

-**Finance** : détection de fraudes sur de gros volumes de transactions.

-**Santé** : traitement d’images médicales et séquençage ADN.

-**Télécom** : gestion de données issues des capteurs et des appels.

-**Industrie** : maintenance prédictive à partir de données IoT.


## Démonstration: WordCount



## Bénefices et limites

# Bénéfices :

-Haute scalabilité horizontale

-Tolérance aux pannes

-Open source et large écosystème (Hive, Pig, Spark…)

-Adapté aux données massives et variées

# Limites :

-Latence élevée → pas idéal pour le temps réel

-Courbe d’apprentissage

-MapReduce moins performant que Spark pour certains cas

-Infrastructure lourde à maintenir


## Conclusion
Hadoop a révolutionné la gestion et le traitement des Big Data.Bien qu'il soit parfois remplacé par Spark, il reste fondamental.Hadoop est surtout une architecture et un écosystème.
