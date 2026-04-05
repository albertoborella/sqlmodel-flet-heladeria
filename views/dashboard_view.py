import flet as ft
from config import cargar_config
from sqlmodel import Session, select
from database.database import engine
from models.stock_model import Gusto
from components.app_layout import app_layout
from controllers.stock_controller import calcular_stock, calcular_ventas_periodo

import matplotlib.pyplot as plt
import base64
from io import BytesIO


def dashboard_view(page: ft.Page, go_to_menu):

    config = cargar_config()
    stock_minimo = config.get("stock_minimo", 10)

    total_stock = 0
    total_consumo = 0
    top_gusto = "-"
    alertas = []

    labels = []
    valores = []

    with Session(engine) as session:
        gustos = session.exec(select(Gusto)).all()

        consumos = []

        for gusto in gustos:

            # 🔹 STOCK
            stock = calcular_stock(session, gusto.id)
            total_stock += stock

            if stock < stock_minimo:
                alertas.append(f"⚠️ {gusto.nombre}: stock bajo ({round(stock,1)} kg)")

            # 🔹 CONSUMO
            consumo = calcular_ventas_periodo(session, gusto.id)
            total_consumo += consumo

            if consumo > 0:
                consumos.append((gusto.nombre, consumo))

        # 🔹 TOP
        consumos.sort(key=lambda x: x[1], reverse=True)

        top = consumos[:5]
        resto = consumos[5:]

        if top:
            top_gusto = top[0][0]

        if resto:
            otros = sum(x[1] for x in resto)
            top.append(("Otros", otros))

        labels = [x[0] for x in top]
        valores = [x[1] for x in top]

    # 🔹 ALERTAS GENERALES
    if total_stock < stock_minimo * 2:
        alertas.append("⚠️ Stock total bajo")

    if total_consumo == 0:
        alertas.append("⚠️ No hay datos de consumo")

    # 🎨 TARJETAS
    def metric_card(title, value, color):
        return ft.Container(
            width=150,
            height=100,
            bgcolor=color,
            border_radius=20,
            padding=10,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(title, size=12, color="white"),
                    ft.Text(value, size=18, weight="bold", color="white"),
                ]
            )
        )

    # 📊 GRÁFICO
    if valores:
        fig, ax = plt.subplots()
        ax.pie(valores, labels=labels, autopct="%1.1f%%")
        ax.set_title("Consumo por gusto")

        buf = BytesIO()
        plt.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)

        img_base64 = base64.b64encode(buf.read()).decode()

        chart_control = ft.Image(
            src=f"data:image/png;base64,{img_base64}",
            width=350,
            height=250
        )
    else:
        chart_control = ft.Text("Sin datos para mostrar", color="white")

    # ⚠️ ALERTAS
    if alertas:
        alertas_controls = [ft.Text(a, color=ft.Colors.RED_300) for a in alertas]
    else:
        alertas_controls = [ft.Text("✅ Todo en orden", color="green")]

    return app_layout(
        page,
        "Dashboard",
        ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            controls=[

                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.TextButton(
                            "Menú",
                            icon=ft.Icons.MENU,
                            on_click=lambda e: go_to_menu(),
                            style=ft.ButtonStyle(color="white")
                        )
                    ]
                ),

                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    wrap=True,
                    spacing=10,
                    controls=[
                        metric_card("Stock (kg)", str(round(total_stock, 1)), "#FF9800"),
                        metric_card("Consumo", str(round(total_consumo, 1)), "#9C27B0"),
                        metric_card("Top gusto", top_gusto, "#2196F3"),
                    ]
                ),

                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text("Alertas", weight="bold", color="white"),
                        *alertas_controls
                    ]
                ),

                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text("Top consumos", color="white"),
                        chart_control
                    ]
                )
            ]
        ),
        go_to_menu
    )