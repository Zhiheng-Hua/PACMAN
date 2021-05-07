import pyxel


class App:
    def __init__(self):
        pyxel.init(160, 120, caption="Hello Pyxel")  # init 窗口设置
        pyxel.image(2).load(0, 0, "assets/pyxel_logo_38x16.png")  # image(0~2): 三个image bank # load(x, y)到图像库内
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(5)
        pyxel.text(55, 41, "Hello, Pyxel!", pyxel.frame_count % 16)
        pyxel.blt(61, 66, 2, 0, 0, 38, 16, 0)  # 图像库到画布(画布x,y, img, 图像库x,y, 尺寸w,h, colkey视为透明色)


App()
