# Partie 1: Installation et configuration du SGBDR & peuplement des données

Choix de l'environnement : 
- utilisation de conteneurs Docker 


### Etape 1 : Installation de PostgreSQL avec Docker
1. Créer le fichier `docker-compose.yml` avec le contenu suivant : 
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

volumes:
  postgres-data:
```
2. taper la commande `docker-compose up -d` dans le terminal :

Réponse du terminal : 
```
    D:\Dropbox\Julia\Dev\NoSQL\Liaison SGBD\Partie_1>docker-compose up -d
[+] Running 15/1
 ✔ db 14 layers [⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿]      0B/0B      Pulled                                                                                                       10.5s 
[+] Running 3/3
 ✔ Network partie_1_default         Created                                                                                                                    0.0s 
 ✔ Volume "partie_1_postgres-data"  Created                                                                                                                    0.0s 
 ✔ Container postgres-db            Started                                                                                                                    0.4s 
 ```
### Etape 2 : Création de données fictives

Pour peupler ma base de données avec des données fictives, je vais utiliser un service de génération de données comme Faker. Pour cela il faut suivre les étapes suivante : 

- **Accéder au conteneur PostgreSQL :**
utiliser la commande suivante pour accéder au conteneur PostgreSQL :
`docker exec -it postgres-db bash`

- **Connexion à PostgreSQL :**
une fois à l'intérieur du conteneur, il faut se connecter à PostgreSQL avec cette commande :
`psql -U myuser -d mydatabase`

- **Création des tables :**
création d'une table pour stocker des données fictives. Par exemple, une table **"products"** :
```
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  description TEXT,
  price DECIMAL(10, 2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

- **Peuplement des données :**
utilisation d'un script Python avec la bibliothèque Faker pour générer et insérer des données fictives dans la table. Création d'un fichier que je nomme : **populate_data.py**.

Pour exécuter ce script, il faut installer les dépendances nécessaires avec :
`pip install faker psycopg2`

Réponse du terminal : 
```
Downloading Faker-25.5.0-py3-none-any.whl (1.8 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 22.9 MB/s eta 0:00:00
Downloading psycopg2-2.9.9-cp312-cp312-win_amd64.whl (1.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 37.2 MB/s eta 0:00:00
Downloading python_dateutil-2.9.0.post0-py2.py3-none-any.whl (229 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 229.9/229.9 kB 1.6 MB/s eta 0:00:00
Downloading six-1.16.0-py2.py3-none-any.whl (11 kB)
Installing collected packages: six, psycopg2, python-dateutil, faker
  WARNING: The script faker.exe is installed in 'C:\Users\julia\AppData\Roaming\Python\Python312\Scripts' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
Successfully installed faker-25.5.0 psycopg2-2.9.9 python-dateutil-2.9.0.post0 six-1.16.0

[notice] A new release of pip is available: 23.2.1 -> 24.0
[notice] To update, run: python.exe -m pip install --upgrade pip
```

Puis il faut exécuter le script avec la commande suivante : `python populate_data.py`


### Etape 3 : Validation des données 
1. Accèder au conteneur PostgreSQL : `docker exec -it postgres-db bash`
2. Se connecter à PostgreSQL : `psql -U myuser -d mydatabase`
3. Vérifier les données insérées : `SELECT * FROM products LIMIT 10;`

Réponse du terminal : 
```
id |       name       |                                                             description                                                             | price  |         created_at
----+------------------+-------------------------------------------------------------------------------------------------------------------------------------+--------+----------------------------
  1 | Miguel Johnson   | National spring main hair make buy. Left group great character shake word. Third current move religious use culture beautiful.      | 540.16 | 2024-06-05 10:27:35.456467
  2 | Deborah Nielsen  | Reflect see house wait perhaps food store. Opportunity us participant according. Condition pressure mention somebody whether.      +| 848.80 | 2024-06-05 10:27:35.456467
    |                  | Rock down hair among environmental paper large. Firm yet want reach.                                                                |        |
  3 | Casey Schmidt    | Poor four than certain shake war able. Onto physical follow that point Democrat for Republican.                                    +| 643.66 | 2024-06-05 10:27:35.456467
    |                  | Raise adult risk unit. Want better mother audience person trial.                                                                    |        |
:
```

Et si je fais la commande `\dt` pour lister toutes les tables disponibles dans la base de données voici ce que me retourne mon terminal :  
```
mydatabase=# \dt
         List of relations
 Schema |   Name   | Type  | Owner  
--------+----------+-------+--------
 public | products | table | myuser
(1 row)
```
