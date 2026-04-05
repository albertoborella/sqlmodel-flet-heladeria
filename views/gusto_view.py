import flet as ft
from sqlmodel import Session
from database.database import engine
from models.stock_model import Gusto
from components.app_layout import app_layout


def gusto_view(page: ft.Page, go_to_menu):

    LABEL_COLOR = ft.Colors.AMBER_300
    BORDER_COLOR = ft.Colors.WHITE_70
    TEXT_COLOR = ft.Colors.WHITE

    nombre_input = ft.TextField(
        label="Nombre del gusto",
        width=300,
        color=TEXT_COLOR,
        border_color=BORDER_COLOR,
        label_style=ft.TextStyle(color=LABEL_COLOR),
    )

    peso_input = ft.TextField(
        label="Peso del balde (kg)",
        width=300,
        keyboard_type=ft.KeyboardType.NUMBER,
        color=TEXT_COLOR,
        border_color=BORDER_COLOR,
        label_style=ft.TextStyle(color=LABEL_COLOR),
    )

    resultado = ft.Text("", color="white")

    def guardar(e):
        e.control.disabled = True
        page.update()

        try:
            nombre = nombre_input.value.strip()

            if not nombre:
                raise ValueError("Ingresá un nombre")

            if not peso_input.value:
                raise ValueError("Ingresá el peso del balde")

            valor = peso_input.value.strip().replace(",", ".")

            try:
                peso = float(valor)
            except:
                raise ValueError("Peso inválido (ej: 6.5 o 6,5)")

            with Session(engine) as session:
                nuevo = Gusto(
                    nombre=nombre,
                    peso_balde=peso
                )
                session.add(nuevo)
                session.commit()

            resultado.value = "✅ Gusto agregado"
            nombre_input.value = ""
            peso_input.value = ""

        except Exception as ex:
            resultado.value = f"❌ {str(ex)}"

        finally:
            e.control.disabled = False
            page.update()

    return app_layout(
        page,
        "Nuevo gusto",
        ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            controls=[
                nombre_input,
                peso_input,

                ft.FilledButton(
                    "Guardar",
                    #width=200,
                    on_click=guardar
                ),

                resultado
            ]
        ),
        go_to_menu
    )