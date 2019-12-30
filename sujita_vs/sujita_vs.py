import pyxel

# アプリグローバルな定数を切っておく
WINDOW_W = 200
WINDOW_H = 120
MOUSE_VISIBLE = True

# Ground Level
STAGE_GL = WINDOW_H - 20

HP_BAR_W = WINDOW_W / 2 -10


#TODO: make Cat class
CAT_W = 16
CAT_H = 16

class App:
    # init で必要なリソースをロードする
    def __init__(self):
        pyxel.init(WINDOW_W, WINDOW_H, caption="Hello Pyxel")
        pyxel.mouse(MOUSE_VISIBLE)
        pyxel.load("assets/sujita.pyxres")
        pyxel.image(0).load(0, 0, "assets/cat_16x16.png")

        self.reset()
        pyxel.run(self.update, self.draw)

    # reset variables
    def reset(self):
        self.chara_direction_x = 1
        self.chara_direction_y = 1

        #self.oji_x = 0; self.oji_y = 0
        self.tubooji = Tubooji()
        self.sujita = Sujita()


    # updateで内部的な処理を行う。ボタンの受け、数値の変動など
    def update(self):
        print(pyxel.frame_count)

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_F12):
            self.reset()

        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            self.chara_direction_x = -self.chara_direction_x

        self.tubooji.update()
        self.sujita.update()

    # drawでは、updateで起きた変動を受けて、描画を更新する。（基本的に変数の操作はしない）
    def draw(self):
        pyxel.cls(pyxel.COLOR_LIGHTGRAY)

        # draw static cat
        pyxel.text(WINDOW_W / 2 -16 ,WINDOW_H / 2 - pyxel.FONT_HEIGHT, "Hello, Sujita!", pyxel.COLOR_ORANGE) 
        pyxel.blt(WINDOW_W / 2 - (CAT_W/2), WINDOW_H / 2, 0, 0, 0, self.chara_direction_x * CAT_W, self.chara_direction_y * CAT_H, colkey=5)

        # draw status
        self.draw_status()
        # draw players
        self.sujita.draw()
        self.tubooji.draw()
        # draw Attack
        self.draw_player_attack()

    # draw Game Status
    def draw_status(self):
        # Status BG
        pyxel.rect(0, STAGE_GL, WINDOW_W, WINDOW_H - STAGE_GL, pyxel.COLOR_PERPLE)
        pyxel.line(WINDOW_W / 2 , STAGE_GL, WINDOW_W / 2 , WINDOW_H, pyxel.COLOR_BLACK)
        pyxel.line(0, STAGE_GL, WINDOW_W, STAGE_GL, pyxel.COLOR_BLACK)

        # Tubo HP Bar
        pyxel.rect(0+5, STAGE_GL+5, HP_BAR_W , WINDOW_H - STAGE_GL-10, pyxel.COLOR_BLACK)
        pyxel.rect(0+5, STAGE_GL+5, HP_BAR_W * self.tubooji.hp / self.tubooji.MAX_HP , WINDOW_H - STAGE_GL-10, pyxel.COLOR_YELLOW)

        # Sujita HP Bar
        pyxel.rect(WINDOW_W / 2 + 5, STAGE_GL+5, HP_BAR_W , WINDOW_H - STAGE_GL-10, pyxel.COLOR_BLACK)
        pyxel.rect(WINDOW_W / 2 + 5, STAGE_GL+5, HP_BAR_W * self.sujita.hp / Sujita.MAX_HP , WINDOW_H - STAGE_GL-10, pyxel.COLOR_YELLOW)

    # 攻撃判定を作る
    def draw_player_attack(self):
        attack_w = 40
        attack_h = 20

        #tubooji attack: KEY_SPACE
        oji_centor_x = self.tubooji.x + (Tubooji.WIDTH  / 2)
        oji_centor_y = self.tubooji.y + (Tubooji.HEIGHT / 2)
        if pyxel.btn(pyxel.KEY_SPACE):
            pyxel.rect(self.tubooji.x + Tubooji.WIDTH, oji_centor_y - (attack_h / 2), attack_w,attack_h,pyxel.COLOR_RED)

        # sujita attack: KEY_RIGHT_CONTROL
        suji_centor_x = self.sujita.x + (Sujita.WIDTH  / 2)
        suji_centor_y = self.sujita.y + (Sujita.HEIGHT / 2)
        if pyxel.btn(pyxel.KEY_RIGHT_CONTROL):
            # Triangle Beam!
            pyxel.tri(self.sujita.x, suji_centor_y,
                self.sujita.x - attack_w, suji_centor_y + attack_h,
                self.sujita.x - attack_w, suji_centor_y - attack_h,
                pyxel.COLOR_YELLOW)

class Tubooji:
    # Image mapping
    IMAGE_N = 1
    IMAGE_X = 64
    IMAGE_Y = 0
    WIDTH = 64
    HEIGHT = 64
    MAX_HP = 4

    def __init__(self,x=0,y=0):
        self.x = x
        self.y = STAGE_GL - self.HEIGHT
        self.hp = Sujita.MAX_HP
        self.alive = True

    def update(self):
        self.damage()
        if not self.alive:
            return

        # move 処理
        if pyxel.btn(pyxel.KEY_A):
            self.x += -2
        if pyxel.btn(pyxel.KEY_D):
            self.x += 2

        """ 上下動は抑制
        if pyxel.btn(pyxel.KEY_W):
            self.y += -2
        if pyxel.btn(pyxel.KEY_S):
            self.y += 2
        """

    def damage(self):
        if pyxel.btnp(pyxel.KEY_P):
            self.hp -= 1
        if(self.hp <= 0):
            self.alive = False

    def draw(self):
        pyxel.blt(self.x, self.y , Tubooji.IMAGE_N, Tubooji.IMAGE_X, Tubooji.IMAGE_Y, Tubooji.WIDTH, Tubooji.HEIGHT, colkey=pyxel.COLOR_WHITE)
        if not self.alive:
            pyxel.text(0 + 5, 0, "TUBO is DEAD !!", pyxel.COLOR_RED)


class Sujita:
    # Image mapping
    IMAGE_N = 1
    IMAGE_X = 0
    IMAGE_Y = 0
    WIDTH = 64
    HEIGHT = 64
    MAX_HP = 4

    def __init__(self,x=0,y=0):
        self.x = x + 150
        self.y = STAGE_GL - self.HEIGHT
        self.hp = Sujita.MAX_HP
        self.alive = True

    def update(self):
        self.damage()
        if not self.alive:
            return

        # move 処理
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x += -2
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 2

        """ 上下動は抑制
        if pyxel.btn(pyxel.KEY_UP):
            self.y += -2
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += 2
        """

    def damage(self):
        if pyxel.btnp(pyxel.KEY_K):
            self.hp -= 1

        if(self.hp <= 0):
            self.alive = False

    def draw(self):
        pyxel.blt(self.x, self.y, Sujita.IMAGE_N, Sujita.IMAGE_X, Sujita.IMAGE_Y, Sujita.WIDTH, Sujita.HEIGHT, colkey=pyxel.COLOR_WHITE)
        if not self.alive:
            pyxel.text(WINDOW_W /2 + 5, 0, "SUJITA is DEAD !!", pyxel.COLOR_RED)

App()


"""
作業メモ：
・HP




"""
