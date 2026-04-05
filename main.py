import flet as ft
from database.database import create_db_and_tables, crear_admin
from scripts.cargar_gustos_iniciales import cargar_gustos_iniciales

from views.admin_view import admin_view
from views.login import login_view
from views.menu_view import menu_view
from views.dashboard_view import dashboard_view

from views.conteo_view import conteo_view
from views.stock_view import stock_view
from views.ingreso_view import ingreso_view
from views.consumo_view import consumo_view
from views.movimientos_view import movimientos_view
from views.consumo_chart_view import consumo_chart_view
from views.gusto_view import gusto_view


def main(page: ft.Page):
    page.title = "Stock de Heladería"
    page.bgcolor = ft.Colors.BLUE_GREY_800
    page.padding = 0
    page.spacing = 0

    # 🔹 navegación base

    def go_to_login():
        page.clean()
        page.add(login_view(page, go_to_dashboard))

    def go_to_dashboard():
        page.clean()
        page.add(dashboard_view(page, go_to_menu))

    def go_to_menu():
        page.clean()
        page.add(
            menu_view(
                page,
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
            )
        )

    # 🔹 pantallas

    def go_to_ingresos():
        page.clean()
        page.add(ingreso_view(page, go_to_menu))

    def go_to_conteo():
        page.clean()
        page.add(conteo_view(page, go_to_menu))

    def go_to_stock():
        page.clean()
        page.add(stock_view(page, go_to_menu))

    def go_to_consumo():
        page.clean()
        page.add(consumo_view(page, go_to_menu))

    def go_to_movimientos():
        page.clean()
        page.add(movimientos_view(page, go_to_menu))

    def go_to_consumo_chart():
        page.clean()
        page.add(consumo_chart_view(page, go_to_menu))

    def go_to_gustos():
        page.clean()
        page.add(gusto_view(page, go_to_menu))

    def go_to_admin():
        page.clean()
        page.add(admin_view(page, go_to_menu))
    
    # 👉 inicio
    go_to_login()


if __name__ == "__main__":
    create_db_and_tables()
    crear_admin()
    ft.run(main, assets_dir="assets")