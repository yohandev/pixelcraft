from framework import Sketch, App

class Minecraft2D(Sketch):
    def name(self) -> str:
        return "Minecraft2D"

    def on_start(self, app: App):
        self.grass = app.load_texture("../res/tiles/grass.png")
        self.dirt = app.load_texture("../res/tiles/dirt.png")

    def on_draw(self, app: App):
        app.fill_tex(self.grass)
        app.rect(500, 500, 40)

        app.fill_tex(self.dirt)
        app.rect(500, 460, 40)

Minecraft2D().run()