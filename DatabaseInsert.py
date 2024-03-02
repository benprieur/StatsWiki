import sqlite3
from GlobalData import DB_NAME


def insert_data_date_lang(lang, yy, mm, dd, articles):

    daily_table = f'{lang}_{yy}_day'
    monthly_table = f'{lang}_{yy}_month'
    yearly_table = f'{lang}_{yy}'
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Insertion dans la table journalière
    # cursor.execute("INSERT INTO table_name (column1, column2, column3) VALUES (?, ?, ?)", (article_name, views_count, article_date))

#/////////
# Mise à jour des tables quotidiennes
#/////////   
    column_name = f"_{yy}{mm:02d}{dd:02d}"
    for article in articles:
        cursor.execute(f"SELECT 1 FROM {daily_table} WHERE article = ? AND {column_name} IS NOT NULL", (article['article'],))
        exists = cursor.fetchone()

        if exists:
        # Mise à jour des vues pour l'article existant à cette date
            cursor.execute(f"UPDATE {daily_table} SET {column_name} = {column_name} + ? WHERE article = ?", (article['views'], article['article']))
        else:
        # Insérer une nouvelle ligne ou mettre à jour une ligne existante pour un autre jour
        # Cela suppose que votre table a d'autres colonnes pour gérer correctement les insertions uniques
            cursor.execute(f"INSERT INTO {daily_table} (article, {column_name}) VALUES (?, ?) ON CONFLICT(article) DO UPDATE SET {column_name} = EXCLUDED.{column_name}", (article['article'], article['views']))


#/////////
# Mise à jour des tables mensuelles
#/////////   
    column_month_name = f"_{mm:02d}"
    for article in articles:
        # Vérification de l'existence de l'article dans la table
        cursor.execute(f"SELECT \"{column_month_name}\" FROM {monthly_table} WHERE article = ?", (article['article'],))
        result = cursor.fetchone()
            
        if result:
            # Mise à jour des vues si l'article existe déjà
            new_views = result[0] + article['views']
            cursor.execute(f"UPDATE {monthly_table} SET \"{column_month_name}\" = ? WHERE article = ?", (new_views, article['article']))
        else:
            # Création d'une nouvelle ligne si l'article n'existe pas
            cursor.execute(f"INSERT INTO {monthly_table} (article, \"{column_month_name}\") VALUES (?, ?)", 
                               (article['article'], article['views']))
#/////////
# Mise à jour des tables annuelles
#/////////            
    column_month_name = f"_{mm:02d}"
    for article in articles:
        # Vérification de l'existence de l'article dans la table
        cursor.execute(f"SELECT views FROM {yearly_table} WHERE article = ?", (article['article'],))
        result = cursor.fetchone()
            
        if result:
            # Mise à jour des vues si l'article existe déjà
            new_views = result[0] + article['views']
            cursor.execute(f"UPDATE {yearly_table} SET views = ? WHERE article = ?", (new_views, article['article']))
        else:
            # Création d'une nouvelle ligne si l'article n'existe pas
            cursor.execute(f"INSERT INTO {yearly_table} (article, views) VALUES (?, ?)", 
                               (article['article'], article['views']))
    
    # Validation des modifications
    conn.commit()
    
    # Fermeture de la connexion
    conn.close()