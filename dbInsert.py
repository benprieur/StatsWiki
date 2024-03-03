import sqlite3
from constants import DB_NAME

'''
    insert_by_day_by_lang
'''
def insert_by_day_by_lang(lang, year, month, day, articles):

    daily_table = f'{lang}_{year}_day'
    monthly_table = f'{lang}_{year}_month'
    yearly_table = f'{lang}_{year}'
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    column_name = f"_{year}{month:02d}{day:02d}"
    for article in articles:
        cursor.execute(f"SELECT 1 FROM {daily_table} WHERE article = ? AND {column_name} IS NOT NULL", (article['article'],))
        exists = cursor.fetchone()

        if exists:
            cursor.execute(f"UPDATE {daily_table} SET {column_name} = {column_name} + ? WHERE article = ?", (article['views'], article['article']))
        else:
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