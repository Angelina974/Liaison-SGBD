# Partie 2: Synchronisation des données du SGBDR avec ElasticSearch

**Choix de l'environnement :**
Je vais utiliser Docker pour déployer Logstash, comme pour PostgreSQL dans la première partie du TP.

### Etape 1: Installation de Logstash
1. **Ajout de Logstash au fichier `docker-compose.yml` :**
il faut étendre notre fichier `docker-compose.yml` pour inclure Logstash et ElasticSearch :
```
version: '3.8'
services:
  db:
    image: postgres:latest
    container_name: postgres-db
    environment:
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
      POSTGRES_DB: mydatabase
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.17.3
    container_name: elasticsearch
    environment:
      - discovery.type=single-node
    ports:
      - "9200:9200"
      - "9300:9300"
    volumes:
      - es-data:/usr/share/elasticsearch/data

  logstash:
    image: docker.elastic.co/logstash/logstash:7.17.3
    container_name: logstash
    volumes:
      - ./logstash/pipeline:/usr/share/logstash/pipeline
    depends_on:
      - db
      - elasticsearch

volumes:
  postgres-data:
  es-data:
```
2. **Création du fichier de configuration de Logstash :**
création d'un répertoire `logstash/pipeline` et à l'intérieur, créer un fichier nommé `logstash.conf` avec le contenu suivant :
```
input {
  jdbc {
    jdbc_connection_string => "jdbc:postgresql://db:5432/mydatabase"
    jdbc_user => "myuser"
    jdbc_password => "mypassword"
    jdbc_driver_class => "org.postgresql.Driver"
    jdbc_driver_library => "/usr/share/logstash/postgresql-42.2.18.jar"
    statement => "SELECT id, name, description, price, created_at FROM products"
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "products"
    document_id => "%{id}"
  }
}
```

3. **Télécharger le fichier jar du driver PostgreSQL :**

Télécharger le fichier JDBC manuellement :

- Ouvrir un navigateur web et accèder à https://jdbc.postgresql.org/download/postgresql-42.2.18.jar.
- Télécharger le fichier sur son ordinateur.
- Déplacer le fichier téléchargé au répertoire `logstash/pipeline`

### Etape 2 : Validation de la synchronisation
1. **Vérifier la configuration et les logs de Logstash :**
- relancer Docker Compose : `docker-compose restart logstash`
- vérifier les logs avec la commande : `docker logs logstash`
- se rendre dans le conteneur logstash : `docker exec -it logstash bash`
- vérifier la connexion à ElasticSearch depuis le conteneur logstash : `curl -X GET "http://elasticsearch:9200"`

Réponse du terminal : 
```
{
  "name" : "45491b18b9f2",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "loAsKQrhTjWCBLHPYYnhnQ",
  "version" : {
    "number" : "7.17.3",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "5ad023604c8d7416c9eb6c0eadb62b14e766caff",
    "build_date" : "2022-04-19T08:11:19.070913226Z",
    "build_snapshot" : false,
    "lucene_version" : "8.11.1",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
```
  
2. **Vérifier les indices dans ElasticSearch :**
- vérifier si l'index products existe dans ElasticSearch après s'être connecter au conteneur Logstash : `curl -X GET "http://localhost:9200/_cat/indices?v"`

Réponse du terminal :
```
health status index            uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   .geoip_databases FUe7jtz4T7SrgXpnNKy5JA   1   0         33           29     30.5mb         30.5mb
yellow open   products         Ma4M1VkfQQ2kEq9Rj7o3YA   1   1          0            0       226b           226b
```