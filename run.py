from app import create_app, db  # Importation de l'application et de l'instance de la base de données

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        # Créer toutes les tables si elles n'existent pas déjà
        print("Création des tables dans la base de données...")
        db.create_all()
        print("Tables créées avec succès.")
    
    # Lancer l'application Flask
    app.run(debug=True)
