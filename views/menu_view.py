import flet as ft
from utils import is_admin

def menu_view(
    page: ft.Page,
    go_to_ingresos,
    go_to_conteo,
    go_to_stock,
    go_to_consumo,
    go_to_login,
    go_to_movimientos,
    go_to_gustos,
    go_to_consumo_chart,
    go_to_dashboard,
    go_to_admin,
):

    def menu_button(text, icon, color, on_click):
        return ft.Container(
            width=320,
            height=40,
            border_radius=20,
            bgcolor=color,
            on_click=lambda e: on_click(),
            padding=10,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    ft.Icon(icon, size=26, color="white"),
                    ft.Text(text, size=16, weight="bold", color="white"),
                ]
            )
        )

    def section_title(text):
        return ft.Text(
            text,
            size=16,
            weight="bold",
            color=ft.Colors.WHITE_70
        )

    return ft.Container(
        expand=True,
        padding=20,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
            controls=[

                ft.Text("Menú", size=26, weight="bold", color="white"),

                menu_button("Ingresos", ft.Icons.INBOX, "#4CAF50", go_to_ingresos),
                menu_button("Recuento Stock", ft.Icons.ASSESSMENT, "#2196F3", go_to_conteo),
                menu_button("Stock", ft.Icons.INVENTORY_2, "#FF9800", go_to_stock),
                menu_button("Nuevo gusto", ft.Icons.ADD, "#009688", go_to_gustos),

                menu_button("Consumo", ft.Icons.SHOW_CHART, "#9C27B0", go_to_consumo),
                menu_button("Movimientos", ft.Icons.LIST_ALT, "#607D8B", go_to_movimientos),
                menu_button("Top consumos", ft.Icons.PIE_CHART, "#E91E63", go_to_consumo_chart),
                menu_button("Dashboard", ft.Icons.DASHBOARD, "#3F51B5", go_to_dashboard),

                # 🔐 BOTÓN ADMIN (solo si es admin)
                menu_button("Admin", ft.Icons.ADMIN_PANEL_SETTINGS, "#F44336", go_to_admin)
                if is_admin(page) else ft.Container(),

                ft.Container(height=10),

                ft.TextButton(
                    "Cerrar sesión",
                    on_click=lambda e: go_to_login(),
                    style=ft.ButtonStyle(color=ft.Colors.RED_300)
                )
            ]
        )
    )