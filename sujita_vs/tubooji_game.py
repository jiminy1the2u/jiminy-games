import pyxel

# 任意の定数を切っておく

WINDOW_W = 160
WINDOW_H = 120
CAT_W = 16
CAT_H = 16
MOUSE_VISIBLE = True

class App:
    # init で必要なリソースをロードする
    def __init__(self):
        pyxel.init(WINDOW_W, WINDOW_H, caption="Hello Pyxel")
        pyxel.mouse(MOUSE_VISIBLE)
        self.mouse_hold = False
        
        self.cat_direction_x = 1
        self.cat_direction_y = 1
        self.oji_x = 0; self.oji_y = 0

        pyxel.load("assets/oji1.pyxres")
        pyxel.image(0).load(0, 0, "assets/cat_16x16.png")
        pyxel.run(self.update, self.draw)

    # updateで内部的な処理を行う。ボタンの受け、数値の変動など
    def update(self):
        print(pyxel.frame_count)

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # 長押しで猫が上下反転する。btnp()は、最初のクリック判定でもTrueが返るため、
        # 長押し時限定の処理を描きたい場合、使いづらい？
        # →フラグmouse_holdを追加し、初回の押下処理で長押し誤爆しないようにセットした。
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON,30,5) and (self.mouse_hold):
            self.cat_direction_y = -self.cat_direction_y

        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and not (self.mouse_hold):
            self.cat_direction_x = -self.cat_direction_x
            self.mouse_hold = True

        if pyxel.btnr(pyxel.MOUSE_LEFT_BUTTON):
            self.mouse_hold = False

        # ojisan を move する処理
        if pyxel.btn(pyxel.KEY_LEFT):
            self.oji_x += -2
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.oji_x += 2
        if pyxel.btn(pyxel.KEY_UP):
            self.oji_y += -2
        if pyxel.btn(pyxel.KEY_DOWN):
            self.oji_y += 2

    # drawでは、updateで起きた変動を受けて、描画を更新する。（基本的に変数の操作はしない）
    def draw(self):
        pyxel.cls(pyxel.COLOR_LIGHTGRAY)
        pyxel.text(55, 41, "Hello, Pyxel!", pyxel.frame_count % 16)

        # draw static cat
        pyxel.blt(75, 45, 0, 0, 0, self.cat_direction_x * CAT_W, self.cat_direction_y * CAT_H, colkey=5)
        
        # draw dynamic cat
        # self.cat()
        
        #draw sujita
        self.sujita()
        
        # draw tubooji
        self.tubooji()        
        self.player_attack()
        
        # 1フレーム置きに、player_attackより手前にstatic catを表示する。（見た目）
        if pyxel.frame_count % 6 == 0:
            pyxel.blt(75, 45, 0, 0, 0, self.cat_direction_x * CAT_W, self.cat_direction_y * CAT_H, colkey=5)

    # マウスカーソルに追従するニャンコをdrawする
    def cat(self):
        mouse_x = pyxel.mouse_x # マウスのX座標
        mouse_y = pyxel.mouse_y # マウスのY座標
        pyxel.blt(mouse_x - CAT_H/2, mouse_y - CAT_W/2,  0, 0, 0, self.cat_direction_x * CAT_W, self.cat_direction_y * CAT_H, colkey=5)

    # つぼおじの画像を表示する。
    def tubooji(self):
        self.oji_w = 71
        self.oji_h = 55
        pyxel.blt(self.oji_x, self.oji_y, 2, 0, 0, self.cat_direction_x * self.oji_w, self.cat_direction_y * self.oji_h, colkey=7)
    
    def sujita(self):
        mouse_x = pyxel.mouse_x # マウスのX座標
        mouse_y = pyxel.mouse_y # マウスのY座標
        self.sujita_w = 47
        self.sujita_h = 63
        pyxel.blt(mouse_x - self.sujita_w/2, mouse_y - self.sujita_h/2,  1,0,0, self.cat_direction_x * self.sujita_w, self.cat_direction_y * self.sujita_h, colkey=pyxel.COLOR_WHITE)
    
    # 攻撃判定を作る
    def player_attack(self):
        attack_w = 40
        attack_h = 20
        self.oji_centor_x = self.oji_x + (self.oji_w / 2)
        self.oji_centor_y = self.oji_y + (self.oji_h / 2)
        if pyxel.btn(pyxel.MOUSE_RIGHT_BUTTON):
            pyxel.rect(pyxel.mouse_x - self.sujita_w , pyxel.mouse_y - (attack_h / 2), attack_w,attack_h,pyxel.COLOR_RED)
            
        if pyxel.btn(pyxel.KEY_SPACE):
            pyxel.tri(self.oji_x + self.oji_w, self.oji_centor_y,
                self.oji_x + self.oji_w + attack_w, self.oji_centor_y + attack_h,
                self.oji_x + self.oji_w + attack_w, self.oji_centor_y - attack_h,
                pyxel.COLOR_YELLOW)
    
    def draw_attack(self):
        pass
    
    
App()


"""
作業メモ：
・主人公クラス：つぼおじ/すじた
　    def 主人公動作()
　        →update()でコールする。
　        クリック押下()で攻撃判定
　    
　    def 攻撃判定()
　        攻撃範囲を算出する。現在の攻撃 + 現在位置で計算。
　        Hit? Yes->"敵"を破壊()->加点() : No->スカリ()->Do nothing
　    def 攻撃draw()
　        攻撃判定に即したエフェクト
　        →"攻撃判定"の範囲(x,y,w,h)は、一時的に確保しておくべき。
　    def 攻撃変更()
　        メンバ："現在の攻撃"を範囲内でインクリメントする。
　            0:パンチ,2:
　    def 加点()
　        "敵"から得点をget()する。
　        得点をメンバ：総得点にAdd()する
　
・操作：左キャラ:キーボード, 右キャラ：マウス
　
・
class HitRange:
    
    
    
    
　
・
　
・
　



"""
