from datetime import date, datetime
import flet as ft
from database.database import engine
from sqlmodel import Session, select
from models.stock_model import Ingreso, Gusto
from components.app_layout import app_layout


def ingreso_view(page: ft.Page, go_to_menu):

    page.scroll = ft.ScrollMode.AUTO

    # 🎨 COLORES UI
    LABEL_COLOR = ft.Colors.AMBER_300
    BORDER_COLOR = ft.Colors.WHITE_70
    TEXT_COLOR = "white"

    with Session(engine) as session:
        gustos = session.exec(select(Gusto)).all()

    gusto_dropdown = ft.Dropdown(
        label="Gusto",
        width=300,
        options=[ft.dropdown.Option(key=str(g.id), text=g.nombre) for g in gustos],
        color=TEXT_COLOR,
        border_color=BORDER_COLOR,
        label_style=ft.TextStyle(color=LABEL_COLOR),  # 👈 CLAVE
    )

    fecha_input = ft.TextField(
        label="Fecha",
        value=date.today().strftime("%d-%m-%Y"),
        color=TEXT_COLOR,
        border_color=BORDER_COLOR,
        label_style=ft.TextStyle(color=LABEL_COLOR),  # 👈 CLAVE
    )

    cantidad_input = ft.TextField(
        label="Cantidad",
        keyboard_type=ft.KeyboardType.NUMBER,
        hint_text="Ej: 4 o 4.5",
        color=TEXT_COLOR,
        border_color=BORDER_COLOR,
        label_style=ft.TextStyle(color=LABEL_COLOR),  # 👈 CLAVE
    )

    unidad_dropdown = ft.Dropdown(
        label="Unidades",
        value="balde",
        width=300,
        options=[
            ft.dropdown.Option(key="balde", text="Baldes"),
            ft.dropdown.Option(key="kg", text="Kilos")
        ],
        color=TEXT_COLOR,
        border_color=BORDER_COLOR,
        label_style=ft.TextStyle(color=LABEL_COLOR),  # 👈 CLAVE
    )

    resultado_text = ft.Text("", color="white")

    def guardar_ingreso(e):
        try:
            if not gusto_dropdown.value:
                raise ValueError("Selecciona un gusto")

            if not cantidad_input.value:
                raise ValueError("Ingresa una cantidad")

            gusto_id = int(gusto_dropdown.value)
            valor = cantidad_input.value.strip().replace(",", ".")
            cantidad = float(valor)
            unidad = unidad_dropdown.value

            with Session(engine) as session:
                gusto = session.get(Gusto, gusto_id)

                if not gusto:
                    raise ValueError("Gusto no válido")

                if unidad == "kg":
                    cantidad_en_kg = cantidad
                else:
                    try:
                        peso_balde = float(gusto.peso_balde)
                    except:
                        raise ValueError("Peso de balde inválido")

                    cantidad_en_kg = cantidad * peso_balde

                nuevo_ingreso = Ingreso(
                    fecha = datetime.strptime(fecha_input.value, "%d-%m-%Y").date(),
                    gusto_id=gusto_id,
                    cantidad=cantidad_en_kg,
                )

                session.add(nuevo_ingreso)
                session.commit()

            resultado_text.value = "✅ Ingreso guardado"
            cantidad_input.value = ""
            page.update()

        except Exception as ex:
            resultado_text.value = f"❌ {str(ex)}"
            page.update()

    return app_layout(
        page,
        "Ingreso de Mercadería",
        ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            controls=[
                fecha_input,
                gusto_dropdown,
                cantidad_input,
                unidad_dropdown,
                ft.FilledButton(
                    "Guardar Ingreso",
                    #width=220,
                    on_click=guardar_ingreso,
                ),
                resultado_text,
            ],
        ),
        go_to_menu,
    )