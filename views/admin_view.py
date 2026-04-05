import os
import flet as ft
import shutil
from sqlmodel import Session, select
from database.database import engine
from config import cargar_config, guardar_config
from datetime import datetime
from models.user_model import User
from models.stock_model import Conteo, Gusto, Ingreso
from components.app_layout import app_layout
from utils import is_admin


def admin_view(page: ft.Page, go_to_menu):

    if not is_admin(page):
        return app_layout(
            page,
            "Acceso denegado",
            ft.Text("No tenés permisos", color="red"),
            go_to_menu
        )

    LABEL_COLOR = ft.Colors.AMBER_300
    BORDER_COLOR = ft.Colors.WHITE_70
    TEXT_COLOR = ft.Colors.WHITE

    config = cargar_config()

    # =========================
    # 🔐 USUARIOS
    # =========================

    username_input = ft.TextField(
        label="Username",
        width=300,
        color=TEXT_COLOR,
        border_color=BORDER_COLOR,
        label_style=ft.TextStyle(color=LABEL_COLOR)
    )

    password_input = ft.TextField(
        label="Password",
        password=True,
        width=300,
        color=TEXT_COLOR,
        border_color=BORDER_COLOR,
        label_style=ft.TextStyle(color=LABEL_COLOR)
    )

    admin_checkbox = ft.Checkbox(
        label="Es administrador",
        value=False,
        label_style=ft.TextStyle(color=LABEL_COLOR)
    )

    resultado_user = ft.Text("", color="white")

    def crear_usuario(e):
        try:
            username = username_input.value.strip()
            password = password_input.value.strip()

            if not username or not password:
                raise ValueError("Completar todos los campos")

            with Session(engine) as session:
                existe = session.exec(
                    select(User).where(User.username == username)
                ).first()

                if existe:
                    raise ValueError("El usuario ya existe")

                nuevo = User(
                    username=username,
                    password=password,
                    is_admin=admin_checkbox.value
                )

                session.add(nuevo)
                session.commit()

            resultado_user.value = "✅ Usuario creado"
            username_input.value = ""
            password_input.value = ""
            admin_checkbox.value = False
            page.update()

        except Exception as ex:
            resultado_user.value = f"❌ {str(ex)}"
            page.update()

    # =========================
    # 🗑 GUSTOS
    # =========================

    with Session(engine) as session:
        gustos = session.exec(select(Gusto)).all()

    gusto_dropdown = ft.Dropdown(
        label="Seleccionar gusto",
        width=300,
        options=[ft.dropdown.Option(str(g.id), g.nombre) for g in gustos],
        color=TEXT_COLOR,
        border_color=BORDER_COLOR,
        label_style=ft.TextStyle(color=LABEL_COLOR),
    )

    resultado_gusto = ft.Text("", color="white")

    def borrar_gusto(e):
        try:
            if not gusto_dropdown.value:
                raise ValueError("Seleccionar un gusto")

            gusto_id = int(gusto_dropdown.value)

            with Session(engine) as session:
                ingresos = session.exec(
                    select(Ingreso).where(Ingreso.gusto_id == gusto_id)
                ).first()

                conteos = session.exec(
                    select(Conteo).where(Conteo.gusto_id == gusto_id)
                ).first()

                if ingresos or conteos:
                    raise ValueError("No se puede borrar: tiene movimientos")

                gusto = session.get(Gusto, gusto_id)

                if not gusto:
                    raise ValueError("No existe el gusto")

                session.delete(gusto)
                session.commit()

            resultado_gusto.value = "🗑 Gusto eliminado"
            gusto_dropdown.value = None
            page.update()

        except Exception as ex:
            resultado_gusto.value = f"❌ {str(ex)}"
            page.update()

    # =========================
    # ⚙️ CONFIGURACIÓN
    # =========================

    stock_minimo_input = ft.TextField(
        label="Stock mínimo alerta (kg)",
        width=300,
        value=str(config.get("stock_minimo", 10)),
        color=TEXT_COLOR,
        border_color=BORDER_COLOR,
        label_style=ft.TextStyle(color=LABEL_COLOR),
    )

    nombre_heladeria_input = ft.TextField(
        label="Nombre de la heladería",
        width=300,
        value=config.get("nombre_heladeria", "Mi Heladería"),
        color=TEXT_COLOR,
        border_color=BORDER_COLOR,
        label_style=ft.TextStyle(color=LABEL_COLOR),
    )

    resultado_config = ft.Text("", color="white")

    def guardar_configuracion(e):
        try:
            stock_minimo = float(stock_minimo_input.value.strip().replace(",", "."))
            nombre = nombre_heladeria_input.value.strip()

            if not nombre:
                raise ValueError("El nombre no puede estar vacío")

            config["stock_minimo"] = stock_minimo
            config["nombre_heladeria"] = nombre

            guardar_config(config)

            resultado_config.value = "✅ Configuración guardada"
            page.update()

        except Exception as ex:
            resultado_config.value = f"❌ {str(ex)}"
            page.update()

    # =========================
    # 💾 BACKUP
    # =========================

    resultado_backup = ft.Text("", color="white")

    def exportar_db(e):
        try:
            origen = "database.db"

            if not os.path.exists(origen):
                raise ValueError("No se encontró la base de datos")

            fecha = datetime.now().strftime("%Y-%m-%d_%H-%M")
            destino = os.path.join(os.getcwd(), f"backup_{fecha}.db")

            shutil.copy(origen, destino)

            resultado_backup.value = f"✅ Exportado en:\n{destino}"
            page.update()

        except Exception as ex:
            resultado_backup.value = f"❌ {str(ex)}"
            page.update()

    # =========================
    # 🧩 UI
    # =========================

    return app_layout(
        page,
        "Administración",
        ft.Container(
            expand=True,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=25,
                scroll=ft.ScrollMode.AUTO,
                controls=[

                    # 🔐 USUARIOS
                    ft.Text("Crear usuario", size=18, weight="bold", color="white"),
                    username_input,
                    password_input,
                    admin_checkbox,
                    ft.FilledButton("Crear usuario", width=200, on_click=crear_usuario),
                    resultado_user,

                    ft.Divider(color="white"),

                    # 🗑 GUSTOS
                    ft.Text("Borrar gusto", size=18, weight="bold", color="white"),
                    gusto_dropdown,
                    ft.FilledButton("Eliminar gusto", width=200, bgcolor=ft.Colors.RED_400, on_click=borrar_gusto),
                    resultado_gusto,

                    ft.Divider(color="white"),

                    # ⚙️ CONFIG
                    ft.Text("Configuración", size=18, weight="bold", color="white"),
                    nombre_heladeria_input,
                    stock_minimo_input,
                    ft.FilledButton("Guardar configuración", width=250, on_click=guardar_configuracion),
                    resultado_config,

                    ft.Divider(color="white"),

                    # 💾 BACKUP
                    ft.Text("Backup", size=18, weight="bold", color="white"),
                    ft.FilledButton("Exportar base de datos", width=250, icon=ft.Icons.DOWNLOAD, on_click=exportar_db),
                    resultado_backup,
                ]
            )
        ),
        go_to_menu
    )