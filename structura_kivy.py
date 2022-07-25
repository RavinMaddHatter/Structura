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
from plyer import filechooser
from kivy.config import Config
from os.path import sep, expanduser, isdir, dirname
import sys
Config.set('graphics', 'width', '482')
Config.set('graphics', 'height', '800')
Config.write()

Builder.load_file("structura.kv")


class StructuraLayout(Widget):
    def __init__(self, *args, **kwargs):
        super(StructuraLayout, self).__init__(*args, **kwargs)
        self.ids.browseButton.bind(on_press = self.browseForFile)
        self.ids.makePack.bind(on_press = self.browseForFile)
    def browseForFile(self, instance):
        path = filechooser.open_file(title="Pick a CSV file..", 
                             filters=[("Comma-separated Values", "*.mcstructure")])
        if len(path)>0:
            self.ids.structureFile.text = path[0]
            print(path[0])
    def makePack(self,instance):
        print("make Pack")

class Structura(App):
    def build(self):
        return StructuraLayout()

if __name__ == "__main__":
    Structura().run()
 
