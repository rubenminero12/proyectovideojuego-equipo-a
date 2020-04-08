import arcade

import UI.Element


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "XD"


class Game(arcade.Window):

    # Función que se va a ejecutar al hacer click en el botón
    def button_pressed(self):
        self.button.text = str(self.num)
        self.num += 1

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Esto manejará toda la interfaz de usuario
        self.user_interface = UI.Element.Element(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

        # Creamos un boton (posicion x, posicion y, ancho, alto)
        self.button = UI.Element.Element(50, 50, 70, 70)

        self.num = 0

        # Los sprites que usará el boton...
        self.button.set_default_sprite("Sprites/UI/button.png")  # Por defecto
        self.button.set_hovered_sprite("Sprites/UI/button_hovered.png")  # Cuando tengamos el ratón encima
        self.button.set_pressed_sprite("Sprites/UI/button_pressed.png")  # Cuando lo presionemos

        # Texto del botón (por defecto no tiene)
        self.button.text = "XDXD"
        # Color del texto del botón
        self.button.text_color = arcade.color.BLACK

        # Asignamos la función que tiene que ejecutarse al hacer click
        # (por defecto no hace nada)
        self.button.on_click = self.button_pressed

        # Añadimos el botón al juego
        self.user_interface.add_element(self.button)

    def on_update(self, delta_time: float):
        self.FPS = 1 / delta_time

    def on_draw(self):
        arcade.start_render()

        # Dibujamos toda la interfaz de usuario
        self.user_interface.draw()

        arcade.finish_render()

    def on_mouse_motion(self, x, y, dx, dy):
        # Actualizamos toda la interfaz de usuario
        self.user_interface.update(x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # Actualizamos toda la interfaz de usuario
        self.user_interface.check_clicks(True)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        # Actualizamos toda la interfaz de usuario
        self.user_interface.check_clicks(False)


def main():
    window = Game()
    arcade.set_background_color(arcade.color.FRESH_AIR)
    arcade.run()


main()
