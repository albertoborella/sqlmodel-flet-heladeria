# import flet as ft
# from sqlmodel import Session, select
# from database.database import engine
# from models.stock_model import Gusto
# from components.app_layout import app_layout
# from controllers.stock_controller import obtener_movimientos


# def movimientos_view(page: ft.Page, go_to_menu):

#     from collections import defaultdict

#     with Session(engine) as session:
#         gustos = session.exec(select(Gusto)).all()

#         datos = []

#         for gusto in gustos:
#             movimientos = obtener_movimientos(session, gusto.id)

#             for m in movimientos:
#                 datos.append({
#                     "fecha": m["fecha"],
#                     "tipo": m["tipo"],
#                     "gusto": gusto.nombre,
#                     "cantidad": round(m["cantidad"], 2)
#                 })

#     # 🔹 ordenar global
#     orden_tipo = {
#     "Ingreso": 1,
#     "Conteo": 2,
#     "Consumo": 3,
#     }

#     datos.sort(key=lambda x: (x["fecha"], orden_tipo.get(x["tipo"], 99)))

#     # 🔹 agrupar por gusto
#     grupos = defaultdict(list)
#     for d in datos:
#         grupos[d["gusto"]].append(d)

#     # 🔹 construir filas agrupadas
#     rows = []

#     for gusto, movimientos in grupos.items():

#         # 🔹 ordenar dentro de cada gusto
#         movimientos.sort(key=lambda x: x["fecha"])

#         # 🔸 título del grupo
#         rows.append(
#             ft.DataRow(
#                 cells=[
#                     ft.DataCell(ft.Text(f"🍦 {gusto}", color="white", weight="bold")),
#                     ft.DataCell(ft.Text("")),
#                     ft.DataCell(ft.Text("")),
#                     ft.DataCell(ft.Text("")),
#                 ]
#             )
#         )

#         # 🔸 movimientos
#         for d in movimientos:
#             color = {
#                 "Ingreso": ft.Colors.GREEN_400,
#                 "Conteo": ft.Colors.BLUE_300,
#                 "Consumo": ft.Colors.RED_300,
#             }.get(d["tipo"], "white")

#             rows.append(
#                 ft.DataRow(
#                     cells=[
#                         ft.DataCell(
#                             ft.Text(
#                                 d["fecha"].strftime("%d-%m-%Y"),
#                                 color="white"
#                             )
#                         ),

#                         ft.DataCell(
#                             ft.Text(
#                                 d["tipo"],
#                                 color=color,
#                                 weight="bold"
#                             )
#                         ),

#                         ft.DataCell(ft.Text(d["gusto"], color="white")),

#                         ft.DataCell(
#                             ft.Text(
#                                 str(d["cantidad"]),
#                                 color=color
#                             )
#                         ),
#                     ]
#                 )
#             )

#         # 🔹 separador visual
#         rows.append(
#             ft.DataRow(
#                 cells=[ft.DataCell(ft.Text("")) for _ in range(4)]
#             )
#         )

#     tabla = ft.Container(
#         #height=400,
#         expand=True,
#         margin=ft.Margin.only(bottom=20),
#         content=ft.Column(
#             expand=True,
#             scroll=ft.ScrollMode.AUTO,
#             controls=[
#                 ft.DataTable(
#                     column_spacing=30,
#                     columns=[
#                         ft.DataColumn(ft.Text("Fecha", color="white")),
#                         ft.DataColumn(ft.Text("Tipo", color="white")),
#                         ft.DataColumn(ft.Text("Gusto", color="white")),
#                         ft.DataColumn(ft.Text("Kg", color="white")),
#                     ],
#                     rows=rows
#                 )
#             ]
#         )
#     )

#     return app_layout(
#         page,
#         "Movimientos históricos",
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
from controllers.stock_controller import obtener_movimientos


def movimientos_view(page: ft.Page, go_to_menu):

    from collections import defaultdict

    with Session(engine) as session:
        gustos = session.exec(select(Gusto)).all()

        datos = []

        for gusto in gustos:
            movimientos = obtener_movimientos(session, gusto.id)

            for m in movimientos:
                datos.append({
                    "fecha": m["fecha"],
                    "tipo": m["tipo"],
                    "gusto": gusto.nombre,
                    "cantidad": round(m["cantidad"], 2)
                })

    # 🔹 ordenar global
    orden_tipo = {
        "Ingreso": 1,
        "Conteo": 2,
        "Consumo": 3,
    }

    datos.sort(key=lambda x: (x["fecha"], orden_tipo.get(x["tipo"], 99)))

    # 🔹 agrupar por gusto
    grupos = defaultdict(list)
    for d in datos:
        grupos[d["gusto"]].append(d)

    # 🔥 UI MOBILE
    movimientos_ui = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=10,
        controls=[]
    )

    for gusto, movimientos in grupos.items():

        # 🔹 ordenar dentro del grupo
        movimientos.sort(key=lambda x: x["fecha"])

        # 🔸 título del gusto
        movimientos_ui.controls.append(
            ft.Text(
                f"🍦 {gusto}",
                size=16,
                weight="bold",
                color=ft.Colors.AMBER_300
            )
        )

        for d in movimientos:

            color = {
                "Ingreso": ft.Colors.GREEN_400,
                "Conteo": ft.Colors.BLUE_300,
                "Consumo": ft.Colors.RED_300,
            }.get(d["tipo"], "white")

            icono = {
                "Ingreso": ft.Icons.DOWNLOAD,
                "Conteo": ft.Icons.CHECK_CIRCLE,
                "Consumo": ft.Icons.UPLOAD,
            }.get(d["tipo"])

            movimientos_ui.controls.append(
                ft.Container(
                    border_radius=15,
                    bgcolor=ft.Colors.BLUE_GREY_700,
                    padding=12,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[

                            # 📅 info izquierda
                            ft.Row(
                                spacing=10,
                                controls=[
                                    ft.Icon(icono, color=color, size=20),

                                    ft.Column(
                                        spacing=2,
                                        controls=[
                                            ft.Text(
                                                d["fecha"].strftime("%d-%m-%Y"),
                                                size=12,
                                                color=ft.Colors.WHITE_70
                                            ),
                                            ft.Text(
                                                d["tipo"],
                                                size=14,
                                                weight="bold",
                                                color=color
                                            ),
                                        ]
                                    ),
                                ]
                            ),

                            # ⚖️ cantidad derecha
                            ft.Text(
                                f"{d['cantidad']} kg",
                                size=16,
                                weight="bold",
                                color=color
                            )
                        ]
                    )
                )
            )

    return app_layout(
        page,
        "Movimientos históricos",
        ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[movimientos_ui]
        ),
        go_to_menu
    )