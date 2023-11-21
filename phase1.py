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
    params = {'début': date_debut, 'fin': date_fin,}
    response = requests.get(url=url, params=params)

    try:
        response = response.json()  # Raises HTTPError for bad responses
        historique = response['historique']
    except Exception as e:
        print(f"Erreur: {e}")
        return []

    resultats = []
    for date, valeurs in historique.items():
        if valeurs[valeur] is not None:
            resultats.append((datetime.strptime(date, '%Y-%m-%d').date(), valeurs[valeur]))
    
    return sorted(resultats)

        # Filtrer les données en fonction de la valeur demandée
def main():
    args = analyser_commande()

    for symbole in args.symboles:
        debut = args.debut or args.fin
        fin = args.fin or datetime.now().strftime('%Y-%m-%d')

        historique = produire_historique(symbole, debut, fin, args.valeur)

        print(f"titre={symbole}: valeur={args.valeur}, début={debut}, fin={fin}")
        print(historique)

if __name__ == "__main__":
    main()

    #commentaire