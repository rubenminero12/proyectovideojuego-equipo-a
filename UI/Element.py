import arcade

import UI.Anchor


class Element:
    """
    Clase que representa un elemento de interfaz de usuario.
    """

    def __init__(self, pos_x: float, pos_y: float, width: float, height: float, anchor: UI.Anchor = UI.Anchor.BOTTOM_LEFT) -> UI.Element:
        """
        :param pos_x: posición en el eje x.
        :param pos_y: posición en el eje y.
        :param width: ancho.
        :param height: alto.
        :param anchor: origen de coordenadas.
        """
        self.__original_pos_x = pos_x
        self.__original_pos_y = pos_y

        self.position_x = pos_x
        self.position_y = pos_y
        self.width = width
        self.height = height

        self.anchor = anchor

        # child elements
        self.__elements = []

        self.__is_being_pressed = False
        self.__is_being_hovered = False

        self.__default_sprite = None
        self.__hovered_sprite = None
        self.__pressed_sprite = None

        self.text = ""
        self.font_size = 16
        self.text_color = arcade.color.BLACK

    def update(self, mouse_pos_x, mouse_pos_y):
        """
        Llamar cuando se mueve el ratón.
        Comprueba si este elemento (o alguno de los elementos que contiene) está debajo del ratón.

        :param mouse_pos_x: posición X del ratón.
        :param mouse_pos_y: posición Y del ratón.
        :return: None
        """
        self.__is_being_hovered = self.position_x < mouse_pos_x < self.position_x + self.width and self.position_y < mouse_pos_y < self.position_y + self.height

        for element in self.__elements:
            element.update(mouse_pos_x, mouse_pos_y)

    def update_position(self, parent_pos_x, parent_pos_y, parent_width, parent_height):
        """
        Actualiza la posición de este elemento respecto al elemento que lo contiene.

        :param parent_pos_x: posición en el eje X del elemento padre.
        :param parent_pos_y: posición en el eje Y del elemento padre.
        :param parent_width: ancho del elemento padre.
        :param parent_height: alto del elemento padre.
        :return: None
        """
        if self.anchor == UI.Anchor.BOTTOM_LEFT:
            self.position_x = self.__original_pos_x + parent_pos_x
            self.position_y = self.__original_pos_y + parent_pos_y

        elif self.anchor == UI.Anchor.BOTTOM_RIGHT:
            self.position_x = parent_pos_x + parent_width - self.__original_pos_x - self.width
            self.position_y = self.__original_pos_y + parent_pos_y

        elif self.anchor == UI.Anchor.TOP_LEFT:
            self.position_x = self.__original_pos_x + parent_pos_x
            self.position_y = parent_pos_y + parent_height - self.__original_pos_y - self.height

        elif self.anchor == UI.Anchor.TOP_RIGHT:
            self.position_x = parent_pos_x + parent_width - self.__original_pos_x - self.width
            self.position_y = parent_pos_y + parent_height - self.__original_pos_y - self.height

        elif self.anchor == UI.Anchor.CENTER:
            self.position_x = parent_pos_x + parent_width / 2 - self.width / 2
            self.position_y = parent_pos_y + parent_height / 2 - self.height / 2

        elif self.anchor == UI.Anchor.TOP:
            self.position_x = parent_pos_x + parent_width / 2 - self.width / 2
            self.position_y = parent_pos_y + parent_height - self.__original_pos_y - self.height

        elif self.anchor == UI.Anchor.BOTTOM:
            self.position_x = parent_pos_x + parent_width / 2 - self.width / 2
            self.position_y = self.__original_pos_y + parent_pos_y

        elif self.anchor == UI.Anchor.LEFT:
            self.position_x = self.__original_pos_x + parent_pos_x
            self.position_y = parent_pos_y + parent_height / 2 - self.height / 2

        elif self.anchor == UI.Anchor.RIGHT:
            self.position_x = parent_pos_x + parent_width - self.__original_pos_x - self.width
            self.position_y = parent_pos_y + parent_height / 2 - self.height / 2

        self.__update_sprite_positions()

        for element in self.__elements:
            element.update_position(self.position_x, self.position_y, self.width, self.height)

    def draw(self):
        """
        Dibuja este elemento (y los elementos que contiene).

        :return: None
        """
        sprite = self.__get_sprite()

        if sprite is not None:
            sprite.draw()

        if self.text != "":
            arcade.draw_text(self.text, self.position_x, self.position_y + self.height / 2, self.text_color,
                             self.font_size, self.width, align="center", anchor_y="center")

        for element in self.__elements:
            element.draw()

    def set_sprites(self, path):
        """
        Carga los sprites del elemento.

        :param path: imagen que se va a gargar.
        :return: None
        """
        self.set_default_sprite(path)
        self.set_hovered_sprite(path)
        self.set_pressed_sprite(path)

    def set_default_sprite(self, path):
        """
        Carga el sprite por defecto del elemento.

        :param path: imagen que se va a gargar.
        :return: None
        """
        self.__default_sprite = arcade.Sprite(path)
        self.__update_sprite_positions()

    def set_hovered_sprite(self, path):
        """
        Carga el sprite del elemento cuando tiene el ratón encima.

        :param path: imagen que se va a gargar.
        :return: None
        """
        self.__hovered_sprite = arcade.Sprite(path)
        self.__update_sprite_positions()

    def set_pressed_sprite(self, path):
        """
        Carga el sprite del elemento cuando está siendo clickado.

        :param path: imagen que se va a gargar.
        :return: None
        """
        self.__pressed_sprite = arcade.Sprite(path)
        self.__update_sprite_positions()

    def __get_sprite(self):
        if self.__is_being_pressed:
            return self.__pressed_sprite

        if self.__is_being_hovered:
            return self.__hovered_sprite

        return self.__default_sprite

    def __update_sprite_positions(self):
        if self.__default_sprite is not None:
            self.__default_sprite.center_x = self.position_x + self.width / 2
            self.__default_sprite.center_y = self.position_y + self.height / 2
            self.__default_sprite.width = self.width
            self.__default_sprite.height = self.height

        if self.__hovered_sprite is not None:
            self.__hovered_sprite.center_x = self.position_x + self.width / 2
            self.__hovered_sprite.center_y = self.position_y + self.height / 2
            self.__hovered_sprite.width = self.width
            self.__hovered_sprite.height = self.height

        if self.__pressed_sprite is not None:
            self.__pressed_sprite.center_x = self.position_x + self.width / 2
            self.__pressed_sprite.center_y = self.position_y + self.height / 2
            self.__pressed_sprite.width = self.width
            self.__pressed_sprite.height = self.height

    def check_clicks(self, pressed: bool):
        """
        Comprueba si el ratón está haciendo click en este elemento (y los elementos que contiene)
        y ejecuta on_click si se está haciendo click.

        Llamar en on_mouse_press y on_mouse_released.

        :param pressed: True en on_mouse_press, False en on_mouse_release.
        :return: None
        """
        if pressed and self.__is_being_hovered:
            self.__is_being_pressed = True
            self.on_click()
        else:
            self.__is_being_pressed = False

        for element in self.__elements:
            element.check_clicks(pressed)

    def on_click(self):
        """
        Función que se ejecuta cuando se hace click sobre este elemento.

        :return: None
        """
        pass

    def add_element(self, element):
        """
        Añade un elemento a esta interfaz de usuario.

        :param element: elemento a añadir.
        :return: None
        """
        element.update_position(self.position_x, self.position_y, self.width, self.height)
        self.__elements.append(element)

    def remove_element(self, element):
        """
        Quita un elemento de esta interfaz de usuario.

        :param element: elemento a retirar.
        :return: None
        """
        self.__elements.remove(element)
