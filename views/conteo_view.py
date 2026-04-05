import flet as ft
from datetime import date, datetime
from sqlmodel import Session, select
from database.database import engine
from models.stock_model import Gusto, Conteo
from components.app_layout import app_layout


def conteo_view(page: ft.Page, go_to_menu):
    
    page.scroll = ft.ScrollMode.AUTO

    LABEL_COLOR = ft.Colors.AMBER_300
    BORDER_COLOR = ft.Colors.WHITE_70
    TEXT_COLOR = "white"

    with Session(engine) as session:
        gustos = session.exec(select(Gusto)).all()

    # 🔹 CONTROLES (con ancho definido)
    gusto_dropdown = ft.Dropdown(
        label="Gusto",
        width=300,
        options=[ft.dropdown.Option(key=str(g.id), text=g.nombre) for g in gustos],
        color=TEXT_COLOR,
        border_color=BORDER_COLOR,
        label_style=ft.TextStyle(color=LABEL_COLOR),
    )

    fecha_input = ft.TextField(
        label="Fecha",
        value=date.today().strftime("%d-%m-%Y"),
        color=TEXT_COLOR,
        border_color=BORDER_COLOR,
        label_style=ft.TextStyle(color=LABEL_COLOR),
    )

    cantidad_input = ft.TextField(
        label="Cantidad",
        width=300,
        # keyboard_type=ft.KeyboardType.NUMBER,
        color=TEXT_COLOR,
        border_color=BORDER_COLOR,
        label_style=ft.TextStyle(color=LABEL_COLOR),
    )

    unidad_dropdown = ft.Dropdown(
        label="Unidad",
        value="balde",
        width=300,
        options=[
            ft.dropdown.Option(key="kg", text="Kilos"),
            ft.dropdown.Option(key="balde", text="Baldes"),
        ],
        color=TEXT_COLOR,
        border_color=BORDER_COLOR,
        label_style=ft.TextStyle(color=LABEL_COLOR),
    )

    resultado_text = ft.Text("", color="white")

    def guardar_conteo(e):
        try:
            if not gusto_dropdown.value:
                raise ValueError("Seleccioná un gusto")

            if not cantidad_input.value:
                raise ValueError("Ingresá una cantidad")

            gusto_id = int(gusto_dropdown.value)

            valor = cantidad_input.value.strip().replace(",", ".")
            try:
                cantidad = float(valor)
            except ValueError:
                raise ValueError("La cantidad debe ser un número (ej: 10 o 10.5)")
            
            unidad = unidad_dropdown.value

            with Session(engine) as session:
                gusto = session.get(Gusto, gusto_id)

                if unidad == "kg":
                    cantidad_en_kg = cantidad
                elif unidad == "balde":
                    try:
                        peso_balde = float(gusto.peso_balde)
                    except:
                        raise ValueError("El peso del balde no es válido")

                    cantidad_en_kg = cantidad * peso_balde
                else:
                    raise ValueError("Unidad inválida")

                nuevo_conteo = Conteo(
                    fecha=datetime.strptime(fecha_input.value, "%d-%m-%Y").date(),
                    gusto_id=gusto_id,
                    cantidad=cantidad_en_kg
                )

                session.add(nuevo_conteo)
                session.commit()

            resultado_text.value = "✅ Conteo guardado correctamente"
            cantidad_input.value = ""
            page.update()

        except Exception as ex:
            resultado_text.value = f"❌ {str(ex)}"
            page.update()

    return app_layout(
        page,
        "Carga de Conteo",
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
                    "Guardar",
                    #width=200,
                    on_click=guardar_conteo
                ),

                resultado_text
            ]
        ),
        go_to_menu
    )
