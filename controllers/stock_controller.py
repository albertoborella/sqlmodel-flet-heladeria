from sqlmodel import Session, select, func
from models.stock_model import Ingreso, Conteo


def calcular_stock(session: Session, gusto_id: int) -> float:
    """
    Calcula el stock actual de un gusto:
    último conteo + ingresos posteriores
    """

    # 🔍 Último conteo
    ultimo_conteo = session.exec(
        select(Conteo)
        .where(Conteo.gusto_id == gusto_id)
        .order_by(Conteo.fecha.desc())
    ).first()

    if ultimo_conteo:
        # 📊 Suma de ingresos posteriores (incluye mismo día)
        total_ingresos = session.exec(
            select(func.sum(Ingreso.cantidad))
            .where(
                Ingreso.gusto_id == gusto_id,
                Ingreso.fecha >= ultimo_conteo.fecha
            )
        ).one()

        total_ingresos = total_ingresos or 0

        stock = ultimo_conteo.cantidad + total_ingresos

    else:
        # 👉 Si nunca hubo conteo → todo lo ingresado es stock
        total_ingresos = session.exec(
            select(func.sum(Ingreso.cantidad))
            .where(Ingreso.gusto_id == gusto_id)
        ).one()

        stock = total_ingresos or 0

    return stock


def calcular_ventas_periodo(session: Session, gusto_id: int) -> float:
    """
    Calcula el consumo entre los dos últimos conteos
    """

    conteos = session.exec(
        select(Conteo)
        .where(Conteo.gusto_id == gusto_id)
        .order_by(Conteo.fecha)
    ).all()

    if len(conteos) < 2:
        return 0

    conteo_inicial = conteos[-2]
    conteo_final = conteos[-1]

    # 📊 Suma de ingresos entre ambos conteos
    total_ingresos = session.exec(
        select(func.sum(Ingreso.cantidad))
        .where(
            Ingreso.gusto_id == gusto_id,
            Ingreso.fecha > conteo_inicial.fecha,
            Ingreso.fecha <= conteo_final.fecha
        )
    ).one()

    total_ingresos = total_ingresos or 0

    ventas = (conteo_inicial.cantidad + total_ingresos) - conteo_final.cantidad

    return ventas


def resumen_gusto(session: Session, gusto) -> dict:
    """
    Devuelve un resumen completo de un gusto
    (útil para tablas o dashboards)
    """

    stock = calcular_stock(session, gusto.id)
    ventas = calcular_ventas_periodo(session, gusto.id)

    return {
        "gusto": gusto.nombre,
        "stock": round(stock, 2),
        "ventas": round(ventas, 2)
    }

def obtener_movimientos(session, gusto_id):
    movimientos = []

    conteos = session.exec(
        select(Conteo)
        .where(Conteo.gusto_id == gusto_id)
        .order_by(Conteo.fecha)
    ).all()

    ingresos = session.exec(
        select(Ingreso)
        .where(Ingreso.gusto_id == gusto_id)
        .order_by(Ingreso.fecha)
    ).all()

    # 🔹 agregar ingresos
    for ing in ingresos:
        movimientos.append({
            "fecha": ing.fecha,
            "tipo": "Ingreso",
            "cantidad": float(ing.cantidad)
        })

    # 🔹 agregar conteos
    for c in conteos:
        movimientos.append({
            "fecha": c.fecha,
            "tipo": "Conteo",
            "cantidad": float(c.cantidad)
        })

    # 🔹 calcular consumos entre conteos
    for i in range(1, len(conteos)):
        c1 = conteos[i - 1]
        c2 = conteos[i]

        ingresos_periodo = [
            ing for ing in ingresos
            if c1.fecha < ing.fecha <= c2.fecha
        ]

        total_ingresos = sum(i.cantidad for i in ingresos_periodo)

        consumo = (c1.cantidad + total_ingresos) - c2.cantidad

        movimientos.append({
            "fecha": c2.fecha,
            "tipo": "Consumo",
            "cantidad": round(consumo, 2)
        })

    # 🔹 ordenar todo junto (CLAVE)
    movimientos.sort(key=lambda x: x["fecha"])

    return movimientos

def obtener_top_consumos(session, top_n=10):
    from sqlmodel import select
    from models.stock_model import Gusto

    gustos = session.exec(select(Gusto)).all()

    consumos = []

    for gusto in gustos:
        consumo = calcular_ventas_periodo(session, gusto.id)

        if consumo > 0:
            consumos.append({
                "gusto": gusto.nombre,
                "consumo": consumo
            })

    # 🔹 ordenar de mayor a menor
    consumos.sort(key=lambda x: x["consumo"], reverse=True)

    # 🔹 separar top y resto
    top = consumos[:top_n]
    resto = consumos[top_n:]

    total = sum(c["consumo"] for c in consumos)

    # 🔹 sumar resto
    if resto:
        total_resto = sum(c["consumo"] for c in resto)
        top.append({
            "gusto": "Otros",
            "consumo": total_resto
        })

    # 🔹 calcular %
    for c in top:
        c["porcentaje"] = round((c["consumo"] / total) * 100, 2) if total > 0 else 0

    return top