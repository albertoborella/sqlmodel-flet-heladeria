def convertir_a_kg(cantidad: float, unidad: str, peso_balde: float) -> float:
    if unidad == "kg":
        return cantidad
    elif unidad == "balde":
        return cantidad * peso_balde
    else:
        return cantidad
    
def get_user(page):
    return getattr(page, "user", None)


def is_admin(page):
    return getattr(page, "is_admin", False)

def logout(page):
    page.user = None
    page.is_admin = False