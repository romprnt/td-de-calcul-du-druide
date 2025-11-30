"""Mini-projet : calcul postfixé – console + fichier."""
import sys

def lire_expression_fichier(path):
    """Lit une expression dans un fichier."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            expr = f.read().strip()
        return expr if expr else "ERREUR: expression vide"
    except FileNotFoundError:
        return "ERREUR: fichier introuvable"
    except OSError:
        return "ERREUR: erreur lecture fichier"


def saisir_expression():
    """Saisie console."""
    expr = input("Entrez votre calcul (postfixé) : ").strip()
    return expr if expr else "ERREUR: expression vide"

def parser_expression(expr):
    """Découpe en tokens."""
    if expr.startswith("ERREUR"): return expr
    tokens = expr.split()
    return tokens if tokens else "ERREUR: expression vide"

def est_nombre(tok):
    """Test numérique."""
    try: float(tok); return True
    except (ValueError, TypeError): return False

def appliquer_operateur(op, a, b):
    """Applique a op b."""
    if op == "+": return a + b
    if op == "-": return a - b
    if op == "*": return a * b
    if op == "/":
        if b == 0: raise ZeroDivisionError("Division par zéro")
        return a / b
    raise ValueError(f"Opérateur non supporté: {op}")

def traiter_token(tok, pile):
    """Traite un token."""
    if est_nombre(tok):
        pile.append(float(tok)); return None
    if tok in {"+", "-", "*", "/"}:
        if len(pile) < 2: return f"ERREUR: pas assez d'opérandes pour '{tok}'"
        b, a = pile.pop(), pile.pop()
        try: pile.append(appliquer_operateur(tok, a, b))
        except (ValueError, ZeroDivisionError) as e: return f"ERREUR: {e}"
        return None
    return f"ERREUR: symbole inconnu '{tok}'"

def calculer_postfixe(tokens):
    """Calcule postfixe."""
    if isinstance(tokens, str) and tokens.startswith("ERREUR"): return tokens
    pile = []
    for tok in tokens:
        err = traiter_token(tok, pile)
        if err: return err
    return pile[0] if len(pile) == 1 else f"ERREUR: expression invalide (pile={len(pile)})"

def gerer_erreur(msg, fatal=True):
    """Gère les erreurs."""
    print("=== ERREUR ==="); print(msg)
    if fatal: sys.exit(1)

def main():
    """Flow principal."""
    mode = input("1=Fichier, 2=Console : ").strip()
    if mode == "1":
        chemin = input("Chemin du fichier : ").strip()
        expr = lire_expression_fichier(chemin)
    elif mode == "2":
        expr = saisir_expression()
    else:
        gerer_erreur("Mode inconnu", True)

    res = calculer_postfixe(parser_expression(expr))
    if isinstance(res, str) and res.startswith("ERREUR"):
        gerer_erreur(res, False)
    else:
        print("Résultat :", res)

if __name__ == "__main__":
    main()
