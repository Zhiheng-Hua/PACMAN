import pyxel
from numpy import random
from time import sleep

class App:
    keyboard = [1, 0, 0, 0]  # [left, up, right, down] -- 0:off, 1: on
    # monster type index {'red': 0, 'blue': 1, 'yellow': 2, 'green': 3}
    monster_from_bank = {0: [(0, 0, 8, 8, 0), (0, 16, 8, 8, 0), (0, 0, -8, 8, 0)],  # from img bank 0
                         1: [(8, 0, 8, 8, 0), (8, 16, 8, 8, 0), (8, 0, -8, 8, 0)],  # (u,v,w,h, [colkey])
                         2: [(0, 8, 8, 8, 0), (0, 24, 8, 8, 0), (0, 8, -8, 8, 0)],  # [left, up, right]
                         3: [(8, 8, 8, 8, 0), (8, 24, 8, 8, 0), (8, 8, -8, 8, 0)]}  # down: random(left/right)
    pacman_from_bank = [[(24, 0, 8, 8, 0),
                         (24, 8, 8, 8, 0)],  # open[hor, ver]
                        [(16, 0, 8, 8, 0),
                         (16, 8, 8, 8, 0)]]  # close[hor, ver]
    black_grid = (32, 16, 8, 8)

    def __init__(self):
        pyxel.init(128, 136, caption="PAC-MAN")
        pyxel.load("assets/pacman.pyxres")

        self.score = 0
        self.extra_score = 0
        self.win = False
        self.lives_number = 3
        self.game_over = False
        self.eaten_pellets = []

        # pacman
        self.pacman_x = 49
        self.pacman_y = 112
        self.pac_dir = 0    # 0: horizontal, 1: vertical
        self.pacman_alive = True

        self.monster_init()  # initialize monsters

        pyxel.run(self.update, self.draw)

    def monster_init(self):
        # monsters
        self.m0 = [48, 56, 1, 3, True, 100, 0, 0]  # m_x, m_y, m_front, m_back_dir, m_alive, timer1, type, timer2
        self.m1 = [56, 56, 1, 3, True, 150, 1, 0]  # m_front: (0~2) [left(/down), up, right];  if down: set to 0
        self.m2 = [64, 56, 1, 3, True, 200, 2, 0]  # m_back_dir: (0~3) [left, up, right, down]
        self.m3 = [56, 40, 1, 3, True, 50, 3, 0]

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):  # press q to quit
            pyxel.quit()

        # update pacman
        self.update_pacman()

        # update monsters
        self.update_monsters(self.m0)
        self.update_monsters(self.m1)
        self.update_monsters(self.m2)
        self.update_monsters(self.m3)

        # update score
        if 15 in [pyxel.pget(self.pacman_x + 3, self.pacman_y + 3), pyxel.pget(self.pacman_x + 4, self.pacman_y + 4)]:
            self.score += 10
            self.eaten_pellets.append((self.pacman_x, self.pacman_y))
            if self.score >= 1300:
                self.win = True
                self.game_over = True

        if 14 in [pyxel.pget(self.pacman_x + 3, self.pacman_y + 3), pyxel.pget(self.pacman_x + 4, self.pacman_y + 4)]:
            self.score += 50
            self.eaten_pellets.append((self.pacman_x, self.pacman_y))
            self.change_monsters(self.m0)
            self.change_monsters(self.m1)
            self.change_monsters(self.m2)
            self.change_monsters(self.m3)
            if self.score >= 1300:
                self.win = True
                self.game_over = True

    def eat_monsters(self):
        if [self.pacman_x, self.pacman_y] == [self.m0[0], self.m0[1]]:
            self.extra_score += 100
            self.m0 = [56, 56, 1, 3, True, 30, 0, 0]
            self.reset_monster_bank(0)
        if [self.pacman_x, self.pacman_y] == [self.m1[0], self.m1[1]]:
            self.extra_score += 100
            self.m1 = [56, 56, 1, 3, True, 30, 1, 0]
            self.reset_monster_bank(1)
        if [self.pacman_x, self.pacman_y] == [self.m2[0], self.m2[1]]:
            self.extra_score += 100
            self.m2 = [56, 56, 1, 3, True, 30, 2, 0]
            self.reset_monster_bank(2)
        if [self.pacman_x, self.pacman_y] == [self.m3[0], self.m3[1]]:
            self.extra_score += 100
            self.m3 = [56, 56, 1, 3, True, 30, 3, 0]
            self.reset_monster_bank(3)

    def change_monsters(self, m):
        m[4] = False
        m[7] = 250
        self.monster_from_bank[m[6]][0] = (0, 32, 8, 8, 0)
        self.monster_from_bank[m[6]][1] = (0, 32, 8, 8, 0)
        self.monster_from_bank[m[6]][2] = (8, 32, 8, 8, 0)

    def update_monsters(self, m):
        if not (48 <= m[0] < 72 and 48 <= m[1] < 64) and m[5] == 0:
            self.move_monsters(m)
        else:
            self.draw_monsters(m)
            m[5] -= 1
            if m[5] == 0:
                m[:] = [56, 40, 1, 3, m[4], 0, m[6], m[7]]

        if m[4] == False:
            self.eat_monsters()
            m[7] -= 1        # timer2 - 1
            if m[7] == 0:
                m[4] = True
                self.reset_monster_bank(m[6])

    def reset_monster_bank(self, index):
        if index == 0:
            self.monster_from_bank[0] = [(0, 0, 8, 8, 0), (0, 16, 8, 8, 0), (0, 0, -8, 8, 0)]
        if index == 1:
            self.monster_from_bank[1] = [(8, 0, 8, 8, 0), (8, 16, 8, 8, 0), (8, 0, -8, 8, 0)]
        if index == 2:
            self.monster_from_bank[2] = [(0, 8, 8, 8, 0), (0, 24, 8, 8, 0), (0, 8, -8, 8, 0)]
        if index == 3:
            self.monster_from_bank[3] = [(8, 8, 8, 8, 0), (8, 24, 8, 8, 0), (8, 8, -8, 8, 0)]

    def move_monsters(self, m):  # m: [m_x, m_y, m_front, m_back_dir, m_alive]
        dir_condition = self.dir_ok_to_go(m[0], m[1])  # dir_dict.key: (left, up, right, down)
        try:
            dir_dict = {i: dir_condition[i] for i in range(4) if (dir_condition[i] and i != m[3])}
            move = random.choice(list(dir_dict.keys()))  # next movement
        except:
            dir_dict = {i: dir_condition[i] for i in range(4) if (dir_condition[i])}
            move = random.choice(list(dir_dict.keys()))  # next movement
        if move == 0:    # turn left
            m[0] -= 1
            m[2] = 0
            m[3] = 2
        elif move == 1:  # go up
            m[1] -= 1
            m[2] = 1
            m[3] = 3
        elif move == 2:  # turn right
            m[0] += 1
            m[2] = 2
            m[3] = 0
        else:            # go downward
            m[1] += 1
            m[2] = 0
            m[3] = 1

    def update_pacman(self):
        if not (self.captured_by_monsters(self.m0)
                or self.captured_by_monsters(self.m1)
                or self.captured_by_monsters(self.m2)
                or self.captured_by_monsters(self.m3)):
            dir_condition = self.dir_ok_to_go(self.pacman_x, self.pacman_y)  # [left, up, right, down]
            if pyxel.btn(pyxel.KEY_LEFT) and dir_condition[0]:
                self.pac_dir = 0
                self.pacman_from_bank[0][0] = (24, 0, 8, 8, 0)  # set image in bank: open hor
                self.pacman_from_bank[1][0] = (16, 0, 8, 8, 0)  # set image in bank: close hor
                self.keyboard[0] = 1
                self.keyboard[1] = self.keyboard[2] = self.keyboard[3] = 0

            if pyxel.btn(pyxel.KEY_RIGHT) and dir_condition[2]:
                self.pac_dir = 0
                self.pacman_from_bank[0][0] = (24, 0, -8, 8, 0)
                self.pacman_from_bank[1][0] = (16, 0, -8, 8, 0)
                self.keyboard[2] = 1
                self.keyboard[0] = self.keyboard[1] = self.keyboard[3] = 0

            if pyxel.btn(pyxel.KEY_UP) and dir_condition[1]:
                self.pac_dir = 1
                self.pacman_from_bank[0][1] = (24, 8, 8, 8, 0)
                self.pacman_from_bank[1][1] = (16, 8, 8, 8, 0)
                self.keyboard[1] = 1
                self.keyboard[0] = self.keyboard[2] = self.keyboard[3] = 0

            if pyxel.btn(pyxel.KEY_DOWN) and dir_condition[3]:
                self.pac_dir = 1
                self.pacman_from_bank[0][1] = (24, 8, 8, -8, 0)
                self.pacman_from_bank[1][1] = (16, 8, 8, -8, 0)
                self.keyboard[3] = 1
                self.keyboard[0] = self.keyboard[1] = self.keyboard[2] = 0

            if self.keyboard[0] == 1 and dir_condition[0]:
                self.pacman_x = self.pacman_x - 1
            elif self.keyboard[1] == 1 and dir_condition[1]:
                self.pacman_y = self.pacman_y - 1
            elif self.keyboard[2] == 1 and dir_condition[2]:
                self.pacman_x = self.pacman_x + 1
            elif self.keyboard[3] == 1 and dir_condition[3]:
                self.pacman_y = self.pacman_y + 1
        else:
            # back to the origin
            self.pacman_x = 49
            self.pacman_y = 112
            self.pac_dir = 0
            self.pacman_alive = True
            self.keyboard = [1, 0, 0, 0]
            self.pacman_from_bank[0][0] = (24, 0, 8, 8, 0)  # set image in bank: open hor
            self.pacman_from_bank[1][0] = (16, 0, 8, 8, 0)  # set image in bank: close hor

    def dir_ok_to_go(self, x, y):
        to_check = [True, True, True, True]  # [left, up, right, down]
        for i in range(0, 8):
            if pyxel.pget(x - 1, y + i) in [1, 2]:
                to_check[0] = False
            if pyxel.pget(x + i, y - 1) in [1, 2]:
                to_check[1] = False
            if pyxel.pget(x + 8, y + i) in [1, 2]:
                to_check[2] = False
            if pyxel.pget(x + i, y + 8) in [1, 2]:
                to_check[3] = False
        return to_check

    def captured_by_monsters(self, m):
        if m[4]:
            monster_color = [8, 12, 9, 3]
            for i in monster_color:
                if i in [pyxel.pget(self.pacman_x + 3, self.pacman_y + 3),
                         pyxel.pget(self.pacman_x + 4, self.pacman_y + 4)]:
                    self.pacman_alive = False
                    self.lives_number -= 1
                    if self.lives_number <= 0:
                        self.game_over = True
                    for i in range(4):
                        self.reset_monster_bank(i)
                    self.monster_init()
                    return True          # pacman is captured
            return False
        else:
            return False

    def draw(self):
        if not self.game_over:
            pyxel.bltm(0, 0, 0, 0, 0, 256, 256)  # initial tilemap

            if len(self.eaten_pellets) != 0:
                for i in range(len(self.eaten_pellets)):
                    pyxel.blt(self.eaten_pellets[i][0], self.eaten_pellets[i][1], 0, *self.black_grid)

            # draw pacman
            pyxel.blt(self.pacman_x,
                      self.pacman_y,
                      0,
                      *self.pacman_from_bank[0 if pyxel.frame_count % 4 < 2 else 1][self.pac_dir])

            # draw monster
            self.draw_monsters(self.m0)
            self.draw_monsters(self.m1)
            self.draw_monsters(self.m2)
            self.draw_monsters(self.m3)

            # draw score
            s = "SCORE {:>4}".format(self.score + self.extra_score)
            pyxel.text(5, 4, s, 0)
            pyxel.text(4, 4, s, 7)

            # show number of lives left
            for i in range(self.lives_number):
                pyxel.blt(i * 8, 128, 0, 24, 24, 8, 8, 0)
        else:
            pyxel.cls(8)
            s = "GAME OVER" if not self.win else "YOU WIN!"
            pyxel.text(29, 40, s, 1)
            pyxel.text(28, 40, s, 7)
            s2 = "Press 'R' to Restart"
            pyxel.text(29, 56, s2, 1)
            pyxel.text(28, 56, s2, 7)
            s2 = "Press 'Q' to Quit"
            pyxel.text(29, 72, s2, 1)
            pyxel.text(28, 72, s2, 7)
            if pyxel.btn(pyxel.KEY_R):
                self.game_over = False
                self.__init__()

    def draw_monsters(self, m):
        if m[4]:
            pyxel.blt(m[0], m[1], 0, *self.monster_from_bank[m[6]][m[2]])
        else:
            pyxel.blt(m[0], m[1], 0, *self.monster_from_bank[m[6]][2 if pyxel.frame_count % 16 < 8 and 0 < m[7] < 75 else 0])


App()

