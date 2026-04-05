import flet as ft
import matplotlib.pyplot as plt
import random
from sqlmodel import Session
from database.database import engine
from controllers.stock_controller import obtener_top_consumos
from components.app_layout import app_layout


def consumo_chart_view(page: ft.Page, go_to_menu):

    LABEL_COLOR = ft.Colors.AMBER_300
    BORDER_COLOR = ft.Colors.WHITE_70
    TEXT_COLOR = "white"

    # 🔹 selector TOP
    top_selector = ft.Dropdown(
        label="Top gustos",
        width=100,
        value="10",
        options=[
            ft.dropdown.Option("5"),
            ft.dropdown.Option("10"),
            ft.dropdown.Option("20"),
        ],
        color=TEXT_COLOR,
        border_color=BORDER_COLOR,
        label_style=ft.TextStyle(color=LABEL_COLOR),
        text_align=ft.TextAlign.CENTER,
    )


    chart_image = ft.Image(
                            src="https://via.placeholder.com/400x300?text=Cargando...",
                            width=400, 
                            height=300, 
                            fit="contain"
                            )

    def generar_grafico(e=None):
        with Session(engine) as session:
            top_n = int(top_selector.value)
            datos = obtener_top_consumos(session, top_n=top_n)

        gustos = [d["gusto"] for d in datos]
        valores = [d["consumo"] for d in datos]

        total = sum(valores)

        # 🔹 colores (TOP vs resto)
        colores = []
        for g in gustos:
            if g == "Resto":
                colores.append("gray")
            else:
                colores.append(f"#{random.randint(0, 0xFFFFFF):06x}")

        # 🔹 gráfico
        plt.figure(figsize=(8, 4))
        bars = plt.bar(gustos, valores)

        # 🔹 aplicar colores
        for bar, color in zip(bars, colores):
            bar.set_color(color)

        # 🔹 porcentajes arriba
        for i, v in enumerate(valores):
            if total > 0:
                porcentaje = (v / total) * 100
                plt.text(i, v, f"{porcentaje:.1f}%", ha="center", va="bottom", fontsize=8)

        plt.title("Consumo por gusto")
        plt.xticks(rotation=45)
        plt.tight_layout()

        ruta = "chart.png"
        plt.savefig(ruta)
        plt.close()

        chart_image.src = ruta
        page.update()

    # 🔹 evento cambio selector
    top_selector.on_change = generar_grafico

    # 🔹 generar al iniciar
    generar_grafico()

    return app_layout(
        page,
        "Mayores consumos",
        ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            controls=[
                top_selector,
                chart_image
            ]
        ),
        go_to_menu
    )