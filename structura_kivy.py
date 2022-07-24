import structura
import os
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.lang import Builder

Builder.load_file("structura.kv")
class StructuraLayout(Widget):
    pass

class Structura(App):
    def build(self):
        return StructuraLayout()

if __name__ == "__main__":
    Structura().run()
