# import flet as ft
# from sqlmodel import Session, select
# from database.database import engine
# from models.stock_model import Gusto, Conteo
# from components.app_layout import app_layout
# from controllers.stock_controller import calcular_ventas_periodo


# def consumo_view(page: ft.Page, go_to_menu):

#     def obtener_consumo():
#         datos = []
#         total_consumo = 0

#         with Session(engine) as session:
#             gustos = session.exec(select(Gusto)).all()

#             # 🔹 calcular consumo por gusto
#             for gusto in gustos:
#                 consumo = calcular_ventas_periodo(session, gusto.id)

#                 datos.append({
#                     "gusto": gusto.nombre,
#                     "consumo": consumo
#                 })

#                 total_consumo += consumo

#         # 🔹 calcular porcentajes
#         for d in datos:
#             if total_consumo > 0:
#                 porcentaje = (d["consumo"] / total_consumo) * 100
#             else:
#                 porcentaje = 0

#             d["porcentaje"] = round(porcentaje, 2)

#         return datos, total_consumo

#     # 🔹 obtener fechas del período
#     def obtener_periodo():
#         with Session(engine) as session:
#             conteos = session.exec(
#                 select(Conteo).order_by(Conteo.fecha)
#             ).all()

#             fechas = list(set([c.fecha for c in conteos]))

#             if len(fechas) >= 2:
#                 fechas.sort()
#                 return fechas[-2], fechas[-1]
#             else:
#                 return None, None

#     datos, total_consumo = obtener_consumo()
#     fecha_desde, fecha_hasta = obtener_periodo()

#     # 🔹 texto período
#     if fecha_desde and fecha_hasta:
#         titulo_periodo = f"Consumo desde {fecha_desde} hasta {fecha_hasta}"
#     else:
#         titulo_periodo = "Sin datos suficientes"

#     # 🔹 tabla
#     tabla = ft.DataTable(
#         columns=[
#             ft.DataColumn(ft.Text("Gusto", color="white")),
#             ft.DataColumn(ft.Text("Consumo (kg)", color="white")),
#             ft.DataColumn(ft.Text("%", color="white")),
#         ],
#         rows=[
#             ft.DataRow(
#                 cells=[
#                     ft.DataCell(ft.Text(d["gusto"], color="white")),
#                     ft.DataCell(ft.Text(str(round(d["consumo"], 2)), color="white")),
#                     ft.DataCell(
#                         ft.Row(
#                             alignment=ft.MainAxisAlignment.CENTER,
#                             controls=[
#                                 ft.Text(f'{d["porcentaje"]} %', color="white")
#                             ]
#                         )
#                     ),
#                 ]
#             )
#             for d in datos
#         ]
#     )

#     hay_datos = fecha_desde is not None and fecha_hasta is not None
    
#     return app_layout(
#         page,
#         "Consumo",
#         ft.Column(
#             expand=True,
#             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#             spacing=15,
#             controls=[
#                 ft.Text(titulo_periodo, color="white"),
#                 ft.Text(f"Total consumido: {round(total_consumo, 2)} kg", color="white")

#                 if hay_datos else ft.Text(""),
#                 tabla if hay_datos else ft.Column(
#                     horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#                     controls=[
#                         ft.Text("⚠️ Sin datos suficientes", color="white"),
#                         ft.Text("Necesitás al menos 2 conteos", color="white"),
#                     ]
#                 )
#             ]
#         ),
#         go_to_menu
#     )

import flet as ft
from sqlmodel import Session, select
from database.database import engine
from models.stock_model import Gusto, Conteo
from components.app_layout import app_layout
from controllers.stock_controller import calcular_ventas_periodo


def consumo_view(page: ft.Page, go_to_menu):

    def obtener_consumo():
        datos = []
        total_consumo = 0

        with Session(engine) as session:
            gustos = session.exec(select(Gusto)).all()

            for gusto in gustos:
                consumo = calcular_ventas_periodo(session, gusto.id)

                datos.append({
                    "gusto": gusto.nombre,
                    "consumo": consumo
                })

                total_consumo += consumo

        # 🔹 calcular porcentajes
        for d in datos:
            if total_consumo > 0:
                porcentaje = (d["consumo"] / total_consumo) * 100
            else:
                porcentaje = 0

            d["porcentaje"] = round(porcentaje, 2)

        return datos, total_consumo

    def obtener_periodo():
        with Session(engine) as session:
            conteos = session.exec(
                select(Conteo).order_by(Conteo.fecha)
            ).all()

            fechas = list(set([c.fecha for c in conteos]))

            if len(fechas) >= 2:
                fechas.sort()
                return fechas[-2], fechas[-1]
            else:
                return None, None

    datos, total_consumo = obtener_consumo()
    fecha_desde, fecha_hasta = obtener_periodo()

    # 🔹 texto período
    if fecha_desde and fecha_hasta:
        titulo_periodo = f"{fecha_desde.strftime('%d-%m-%Y')} → {fecha_hasta.strftime('%d-%m-%Y')}"
    else:
        titulo_periodo = "Sin datos suficientes"

    hay_datos = fecha_desde is not None and fecha_hasta is not None

    # 🔥 UI MOBILE
    consumo_ui = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=10,
        controls=[]
    )

    # 🔹 encabezado
    consumo_ui.controls.append(
        ft.Text(
            f"Período: {titulo_periodo}",
            color=ft.Colors.WHITE_70
        )
    )

    if hay_datos:
        consumo_ui.controls.append(
            ft.Text(
                f"Total consumido: {round(total_consumo, 2)} kg",
                size=16,
                weight="bold",
                color=ft.Colors.AMBER_300
            )
        )

        # 🔹 ordenar por consumo DESC (muy útil 🔥)
        datos.sort(key=lambda x: x["consumo"], reverse=True)

        for d in datos:

            # 🎨 color según porcentaje
            if d["porcentaje"] > 40:
                color = ft.Colors.RED_300
            elif d["porcentaje"] > 20:
                color = ft.Colors.ORANGE_300
            else:
                color = ft.Colors.GREEN_400

            consumo_ui.controls.append(
                ft.Container(
                    border_radius=15,
                    bgcolor=ft.Colors.BLUE_GREY_700,
                    padding=12,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[

                            # 🍦 gusto
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
                                        f"{d['porcentaje']} %",
                                        size=12,
                                        color=color
                                    ),
                                ]
                            ),

                            # ⚖️ consumo
                            ft.Text(
                                f"{round(d['consumo'], 2)} kg",
                                size=16,
                                weight="bold",
                                color=color
                            )
                        ]
                    )
                )
            )

    else:
        consumo_ui.controls.append(
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("⚠️ Sin datos suficientes", color="white"),
                    ft.Text("Necesitás al menos 2 conteos", color="white"),
                ]
            )
        )

    return app_layout(
        page,
        "Consumo",
        ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[consumo_ui]
        ),
        go_to_menu
    )