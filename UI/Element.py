import arcade


class Element:
    """Elemento de interfaz de usuario."""

    def __init__(self, pos_x, pos_y, width, height):
        self.position_x = pos_x
        self.position_y = pos_y
        self.width = width
        self.height = height

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
        self.__is_being_hovered = self.position_x < mouse_pos_x < self.position_x + self.width and self.position_y < mouse_pos_y < self.position_y + self.height

        for element in self.__elements:
            element.update(mouse_pos_x, mouse_pos_y)

    def draw(self):
        sprite = self.__get_sprite()

        if sprite is not None:
            sprite.draw()

        if self.text != "":
            arcade.draw_text(self.text, self.position_x, self.position_y + self.height / 2, self.text_color, self.font_size, self.width, align= "center", anchor_y="center")

        for element in self.__elements:
            element.draw()

    def set_sprites(self, path):
        self.set_default_sprite(path)
        self.set_hovered_sprite(path)
        self.set_pressed_sprite(path)

    def set_default_sprite(self, path):
        self.__default_sprite = arcade.Sprite(path)
        self.__default_sprite.center_x = self.position_x + self.width / 2
        self.__default_sprite.center_y = self.position_y + self.height / 2
        self.__default_sprite.width = self.width
        self.__default_sprite.height = self.height

    def set_hovered_sprite(self, path):
        self.__hovered_sprite = arcade.Sprite(path)
        self.__hovered_sprite.center_x = self.position_x + self.width / 2
        self.__hovered_sprite.center_y = self.position_y + self.height / 2
        self.__hovered_sprite.width = self.width
        self.__hovered_sprite.height = self.height

    def set_pressed_sprite(self, path):
        self.__pressed_sprite = arcade.Sprite(path)
        self.__pressed_sprite.center_x = self.position_x + self.width / 2
        self.__pressed_sprite.center_y = self.position_y + self.height / 2
        self.__pressed_sprite.width = self.width
        self.__pressed_sprite.height = self.height

    def __get_sprite(self):
        if self.__is_being_pressed:
            return self.__pressed_sprite

        if self.__is_being_hovered:
            return self.__hovered_sprite

        return self.__default_sprite

    def check_clicks(self, pressed):
        if pressed and self.__is_being_hovered:
            self.__is_being_pressed = True
            self.on_click()
        else:
            self.__is_being_pressed = False

        for element in self.__elements:
            element.check_clicks(pressed)

    def on_click(self):
        pass

    def add_element(self, element):
        self.__elements.append(element)

    def remove_element(self, element):
        self.__elements.remove(element)
