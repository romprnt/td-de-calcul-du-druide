"""
Mini-projet : calcul postfixé – console + fichier.

Respect des bonnes pratiques : PEP8, Pathlib, Typing, Exceptions.
"""
import sys
from pathlib import Path
from typing import List, Union

# Constantes
OPERATEURS = {"+", "-", "*", "/"}


def lire_expression_fichier(path_str: str) -> str:
    """
    Lit une expression dans un fichier avec encodage UTF-8.

    :param path_str: Chemin du fichier
    :return: Le contenu du fichier nettoyé
    :raises FileNotFoundError: Si le fichier n'existe pas
    :raises OSError: En cas d'erreur de lecture
    """
    # Utilisation de Pathlib + encoding explicite
    path = Path(path_str)
    if not path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {path_str}")
    
    # read_text gère l'ouverture et la fermeture automatiquement
    content = path.read_text(encoding="utf-8").strip()
    
    if not content:
        raise ValueError("Expression vide dans le fichier")
    return content


def saisir_expression() -> str:
    """
    Demande une saisie utilisateur via la console.

    :return: La chaîne saisie nettoyée
    :raises ValueError: Si la saisie est vide
    """
    expr = input("Entrez votre calcul (postfixé) : ").strip()
    if not expr:
        raise ValueError("Expression vide")
    return expr


def parser_expression(expr: str) -> List[str]:
    """
    Découpe une chaîne en liste de tokens.

    :param expr: La chaîne d'expression (ex: "3 4 +")
    :return: Une liste de tokens (ex: ["3", "4", "+"])
    """
    tokens = expr.split()
    if not tokens:
        raise ValueError("Aucun token trouvé")
    return tokens


def est_nombre(tok: str) -> bool:
    """Vérifie si un token est un nombre valide"""
    try:
        float(tok)
        return True
    except ValueError:
        return False


def appliquer_operateur(op: str, a: float, b: float) -> float:
    """
    Applique l'opérateur sur deux opérandes

    :param op: L'opérateur (+, -, *, /)
    :param a: Premier opérande (gauche)
    :param b: Second opérande (droite - sommet pile)
    :raises ZeroDivisionError: Si division par zéro
    :raises ValueError: Si opérateur inconnu
    """
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        if b == 0:
            raise ZeroDivisionError("Division par zéro")
        return a / b
    
    raise ValueError(f"Opérateur non supporté : {op}")


def traiter_token(tok: str, pile: List[float]) -> None:
    """
    Traite un token individuel et met à jour la pile.

    :param tok: Le token à traiter (nombre ou opérateur)
    :param pile: La pile de calcul (modifiée en place)
    :raises ValueError: Si pile insuffisante ou token invalide
    """
    if est_nombre(tok):
        pile.append(float(tok))
        return

    if tok in OPERATEURS:
        if len(pile) < 2:
            raise ValueError(f"Pas assez d'opérandes pour '{tok}'")
        
        # Attention à l'ordre : b est au sommet (dépilé en premier)
        b = pile.pop()
        a = pile.pop()
        
        resultat = appliquer_operateur(tok, a, b)
        pile.append(resultat)
        return

    raise ValueError(f"Symbole inconnu ou invalide : '{tok}'")


def calculer_postfixe(tokens: List[str]) -> float:
    """
    Gere le calcul complet à partir d'une liste de tokens

    :param tokens: Liste des tokens
    :return: Le résultat final
    :raises ValueError: Si la pile finale est incorrecte
    """
    pile: List[float] = []
    
    for tok in tokens:
        traiter_token(tok, pile)
    
    if len(pile) != 1:
        raise ValueError(f"Expression invalide (reste {len(pile)} éléments dans la pile)")
    
    return pile[0]


def gerer_erreur(msg: Union[str, Exception], fatal: bool = True) -> None:
    """
    Affiche un message d'erreur standardisé et quitte si nécessaire.
    """
    # Utilisation de sys.stderr pour les erreurs 
    print(f"=== ERREUR : {msg} ===", file=sys.stderr)
    if fatal:
        sys.exit(1)


def main() -> int:
    """
    Point d'entrée principal (Main loop).
    Sépare l'acquisition, le parsing et le calcul.
    """
    print("--- Calculatrice Postfixée ---")
    mode = input("1 = Fichier\n2 = Console\nVotre choix : ").strip()

    try:
        # 1. Acquisition
        if mode == "1":
            chemin = input("Chemin du fichier : ").strip()
            expr = lire_expression_fichier(chemin)
        elif mode == "2":
            expr = saisir_expression()
        else:
            print("Mode inconnu.")
            return 1

        # 2. Parsing
        tokens = parser_expression(expr)

        # 3. Calcul
        res = calculer_postfixe(tokens)
        
        # 4. Affichage
        print(f"Résultat : {res}")
        return 0

    except (FileNotFoundError, ValueError, ZeroDivisionError, OSError) as e:
        # Gestion centralisée des erreurs 
        gerer_erreur(e, fatal=False)
        return 1


if __name__ == "__main__":
    # Point d'entrée clair et protégé 
    sys.exit(main())
