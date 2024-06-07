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
- Télécharger le fichier sur ton ordinateur.
- Déplacer le fichier téléchargé au répertoire `logstash/pipeline`

4. **Vérifier la configuration et les logs de Logstash :**
- relancer Docker Compose : `docker-compose up -d`
- vérifier les logs avec la commande : `docker logs logstash`
- vérifier les données dans ElasticSearch : utilisation de Postman pour faire la reqête suivante : 
