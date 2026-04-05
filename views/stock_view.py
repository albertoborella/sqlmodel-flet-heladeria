# import flet as ft
# from sqlmodel import Session, select
# from database.database import engine
# from models.stock_model import Gusto
# from components.app_layout import app_layout
# from controllers.stock_controller import calcular_stock


# def stock_view(page: ft.Page, go_to_menu):

#     def obtener_stock():
#         datos = []

#         with Session(engine) as session:
#             gustos = session.exec(select(Gusto)).all()

#             for gusto in gustos:
#                 # ✅ USAR CONTROLLER
#                 kg = calcular_stock(session, gusto.id)

#                 try:
#                     peso_balde = float(gusto.peso_balde)
#                     baldes = kg / peso_balde
#                 except:
#                     baldes = 0

#                 datos.append({
#                     "gusto": gusto.nombre,
#                     "kg": round(kg, 2),
#                     "baldes": round(baldes, 2)
#                 })

#         return datos

#     datos = obtener_stock()

#     tabla = ft.DataTable(
#         columns=[
#             ft.DataColumn(ft.Text("Gusto", color="white")),
#             ft.DataColumn(ft.Text("Kg", color="white")),
#             ft.DataColumn(ft.Text("Baldes", color="white")),
#         ],
#         rows=[
#             ft.DataRow(
#                 cells=[
#                     ft.DataCell(ft.Text(d["gusto"], color="white")),
#                     ft.DataCell(ft.Text(str(d["kg"]), color="white")),
#                     ft.DataCell(ft.Text(str(d["baldes"]), color="white")),
#                 ]
#             )
#             for d in datos
#         ]
#     )

#     return app_layout(
#         page,
#         "Stock Actual",
#         ft.Column(
#             expand=True,
#             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#             controls=[tabla]
#         ),
#         go_to_menu
#     )

import flet as ft
from sqlmodel import Session, select
from database.database import engine
from models.stock_model import Gusto
from components.app_layout import app_layout
from controllers.stock_controller import calcular_stock


def stock_view(page: ft.Page, go_to_menu):

    def obtener_stock():
        datos = []

        with Session(engine) as session:
            gustos = session.exec(select(Gusto)).all()

            for gusto in gustos:
                kg = calcular_stock(session, gusto.id)

                try:
                    peso_balde = float(gusto.peso_balde)
                    baldes = kg / peso_balde
                except:
                    baldes = 0

                datos.append({
                    "gusto": gusto.nombre,
                    "kg": round(kg, 2),
                    "baldes": round(baldes, 2)
                })

        return datos

    datos = obtener_stock()

    # 🔥 UI MOBILE
    stock_ui = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=10,
        controls=[]
    )

    for d in datos:

        # 🎨 color según stock
        if d["kg"] <= 0:
            color = ft.Colors.RED_300
        elif d["kg"] < 10:
            color = ft.Colors.ORANGE_300
        else:
            color = ft.Colors.GREEN_400

        stock_ui.controls.append(
            ft.Container(
                border_radius=15,
                bgcolor=ft.Colors.BLUE_GREY_700,
                padding=12,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[

                        # 🍦 Gusto
                        ft.Column(
                            spacing=2,
                            controls=[
                                ft.Text(
                                    d["gusto"],
                                    size=16,
                                    weight="bold",
                                    color=ft.Colors.AMBER_300
                                ),
                                ft.Text(
                                    f"{d['baldes']} baldes",
                                    size=12,
                                    color=ft.Colors.WHITE_70
                                ),
                            ]
                        ),

                        # ⚖️ Stock en kg
                        ft.Text(
                            f"{d['kg']} kg",
                            size=18,
                            weight="bold",
                            color=color
                        )
                    ]
                )
            )
        )

    return app_layout(
        page,
        "Stock Actual",
        ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[stock_ui]
        ),
        go_to_menu
    )