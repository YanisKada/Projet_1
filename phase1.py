import argparse
import requests
from datetime import datetime

def analyser_commande():
    """
    Générer un interpréteur de commande.

    Returns:
        Un objet Namespace tel que retourné par parser.parse_args().
        Cet objet aura l'attribut «symboles» représentant la liste des
        symboles à traiter, et les attributs «début», «fin» et «valeur»
        associés aux arguments optionnels de la ligne de commande.
    """
    parser = argparse.ArgumentParser(description="Extraction de valeurs historiques pour un ou plusieurs symboles boursiers.")
    parser.add_argument("symboles", nargs="+", help="Nom d'un symbole boursier")
    parser.add_argument("-d", "--début", type=str, help="Date recherchée la plus ancienne (format: AAAA-MM-JJ)")
    parser.add_argument("-f", "--fin", type=str, help="Date recherchée la plus récente (format: AAAA-MM-JJ)")
    parser.add_argument("-v", "--valeur", choices=["fermeture", "ouverture", "min", "max", "volume"], default="fermeture",
                        help="La valeur désirée (par défaut: fermeture)")

    return parser.parse_args()

def produire_historique(symbole, date_debut, date_fin, valeur):
    url = f'https://pax.ulaval.ca/action/{symbole}/historique/'
    
    params = {
        'début': date_debut,
        'fin': date_fin,
    }

    response = requests.get(url=url, params=params)

    try:
        response.raise_for_status()  # Raises HTTPError for bad responses
        data = response.json()
        historique = data['historique']

        # Filtrer les données en fonction de la valeur demandée
        historique_filtré = [(date, entry[valeur]) for date, entry in historique.items()]

        # Trier par date
        historique_filtré.sort()

        return historique_filtré

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête : {e}")
        return []

def afficher_resultats(symbole, valeur, date_debut, date_fin, historique):
    print(f"titre={symbole}: valeur={valeur}, début={date_debut}, fin={date_fin}")
    print(historique)

if __name__ == "__main__":
    args = analyser_commande()

    date_debut = args.début if args.début else datetime.today().strftime('%Y-%m-%d')
    date_fin = args.fin if args.fin else datetime.today().strftime('%Y-%m-%d')

    for symbole in args.symboles:
        historique = produire_historique(symbole, date_debut, date_fin, args.valeur)
        afficher_resultats(symbole, args.valeur, date_debut, date_fin, historique)

        #commentaire