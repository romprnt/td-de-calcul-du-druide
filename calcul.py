"""Mini-projet : Drôle de calcul du druide – version console uniquement."""

# -------------------------------------------------------
# Code structuré en services, ≤12 lignes chacun
# -------------------------------------------------------

def saisir_expression():
    """Lit une expression postfixée depuis la console."""
    expr = input("Entrez votre calcul (postfixé) : ").strip()
    if not expr:
        return "ERREUR: expression vide"
    return expr


def parser_expression(expr):
    """Découpe la chaîne en tokens."""
    if expr.startswith("ERREUR"):
        return expr
    tokens = expr.strip().split()
    if not tokens:
        return "ERREUR: expression vide"
    return tokens


def est_nombre(tok):
    """Vérifie si le token est un nombre."""
    try:
        float(tok)
        return True
    except (ValueError, TypeError):
        return False


def appliquer_operateur(op, a, b):
    """Applique a op b."""
    if op == "+": return a + b
    if op == "-": return a - b
    if op == "*": return a * b
    if op == "/":
        if b == 0:
            raise ZeroDivisionError("Division par zéro")
        return a / b
    raise ValueError(f"Opérateur non supporté: {op}")


def calculer_postfixe(tokens):
    """Exécute un calcul postfixé via pile."""
    if isinstance(tokens, str) and tokens.startswith("ERREUR"):
        return tokens
    pile = []
    for tok in tokens:
        if est_nombre(tok):
            pile.append(float(tok))
        elif tok in {"+", "-", "*", "/"}:
            if len(pile) < 2:
                return f"ERREUR: pas assez d'opérandes pour '{tok}'"
            b, a = pile.pop(), pile.pop()
            try:
                pile.append(appliquer_operateur(tok, a, b))
            except (ValueError, ZeroDivisionError) as e:
                return f"ERREUR: {e}"
        else:
            return f"ERREUR: symbole inconnu '{tok}'"
    return pile[0] if len(pile) == 1 else f"ERREUR: expression invalide (pile={len(pile)})"


def gerer_erreur(msg, fatal=True):
    """Affiche un message d’erreur."""
    print("=== ERREUR ===")
    print(msg)
    if fatal:
        import sys
        sys.exit(1)


def main():
    """Point d’entrée du programme."""
    expr = saisir_expression()
    tokens = parser_expression(expr)
    resultat = calculer_postfixe(tokens)

    if isinstance(resultat, str) and resultat.startswith("ERREUR"):
        gerer_erreur(resultat, fatal=False)
    else:
        print("Résultat :", resultat)


if __name__ == "__main__":
    main()
