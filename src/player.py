from engine import *

class Player:
    def __init__(self):
        self.x = width() / 2
        self.y = height() / 2

    def render(self, frame: float, look: list):
        img = Player.render.textures

        if len(img) == 0:
            img['leg']  = load_image('textures/player/leg.png')
            img['body'] = load_image('textures/player/body.png')
            img['arm']  = load_image('textures/player/arm.png')
            img['head'] = load_image('textures/player/head.png')
        
        def leg(x: float, y: float, deg: float):
            pushMatrix()
            translate(x, y)
            rotate(deg)
            translate(-img['leg'].width / 2, -img['leg'].height)
            image(img['leg'], 0, 0)
            popMatrix()
        def body(x: float, y: float):
            image(img['body'], x - img['body'].width / 2, y)
        def arm(x: float, y: float, deg: float):
            pushMatrix()
            translate(x, y + img['body'].height)
            rotate(deg)
            translate(-img['arm'].width / 2, -img['arm'].height)
            image(img['arm'], 0, 0)
            popMatrix()
        def head(x: float, y: float, mx: float, my: float):            
            deg = math.degrees(math.atan2(my - (y + img['body'].height), mx - x))
            
            pushMatrix()
            translate(x, y + img['body'].height)
            if abs(deg) > 90:
                scale(-1, 1)
                rotate(-deg + 180)
            else:
                rotate(deg)
            print(deg)
            translate(-img['head'].width / 2, 0)
            image(img['head'], 0, 0)
            popMatrix()

        leg(self.x, self.y, 45 * math.sin(frame * 1.5))
        leg(self.x, self.y, 45 * math.sin(math.pi + frame * 1.5))
        arm(self.x, self.y, 45 * math.sin(math.pi + frame * 1.5))
        body(self.x, self.y)
        arm(self.x, self.y, 45 * math.sin(frame * 1.5))
        head(self.x, self.y, look[0], look[1])

Player.render.textures = {}