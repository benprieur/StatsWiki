import sqlite3
DB_NAME = '../StatsWiki00.db'

# Se connecter à la base de données
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Commande SQL pour ajouter une colonne à la table existante
add_column_query = '''
ALTER TABLE _wikidata
ADD COLUMN az_title TEXT;
'''

# Exécuter la commande SQL
cursor.execute(add_column_query)

# Confirmer la transaction et fermer la connexion
conn.commit()
conn.close()