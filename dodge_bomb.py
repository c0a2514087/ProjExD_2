import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectか爆弾Rect
    戻り値：タプル（横方向の判定結果, 縦方向の判定結果）
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface)   -> None:
    """
    
    ゲームオーバーを表示する関数
    引数：画面Surface
    戻り値：なし
    
    """
    go_img = pg.Surface((WIDTH, HEIGHT))  # ゲームオーバー用の空のSurfaceを作る。
    go_rct = go_img.get_rect()  # ゲームオーバー用のRectを取得する
    go_img.set_alpha(220) # 透明度を設定する
    font = pg.font.Font(None, 60)  # フォント（Noneはデフォルトのフォント、60はサイズ）
    text = font.render("GAME OVER", True, (255, 255, 255))  # gameoverのテキスト
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2)) 
    img=pg.image.load("fig/8.png")  # こうかとんの画像を読み込む
    img_rect=img.get_rect(center=(WIDTH // 2+150, HEIGHT // 2))
    img_rect2=img.get_rect(center=(WIDTH // 2-150, HEIGHT // 2))
    go_img.blit(img, img_rect)  # こうかとんの画像右
    go_img.blit(img, img_rect2)  # こうかとんの画像左
    go_img.blit(text, text_rect)  # テキスト貼り付け
    screen.blit(go_img, go_rct)  # 画面出力
    pg.display.update()  #画面を更新する
    time.sleep(5) # 5秒間表示する
    return
def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """"
    爆弾の画像と加速のリストを初期化する関数
    引数：なし
    戻り値：爆弾の大きさ変更画像のリストと段階的な加速のリスト
    """

    bb_imgs=[]
    bb_accs=[a for a in range(1,11)]
    for r in range(1,11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255,0,0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
    return bb_imgs, bb_accs
def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """"
    こうかとんの画像を移動方向に応じて変えるための辞書を作成する関数
    引数：なし 
    戻り値：移動方向をキー、対応するこうかとんの画像を値とする辞書
    """
    kk_dict = {
        (0, 0):pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 1),
        (0, -5):pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"), True, False), 90, 1),
        (0, +5):pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"), True, False), 270, 1),
        (-5, 0):pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 1),
        (+5, 0):pg.transform.flip(pg.image.load("fig/3.png"), True, False),
        (-5, -5):pg.transform.rotozoom(pg.image.load("fig/3.png"), 315, 1),
        (+5, -5):pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"), True, False), 45, 1),
        (-5, +5):pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 1),
        (+5, +5):pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"), True, False), 305, 1)
        }  #拡大と反転を組み合わせたいときは　pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"), True, False), 270, 1)　のようにする
    return kk_dict
def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
        # 爆弾の初期化
    bb_img = pg.Surface((20, 20))  # 爆弾用の空のSurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 半径10の赤い円を描画
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()  # 爆弾Rect
    bb_rct.centerx = random.randint(0, WIDTH)  # 横初期座標
    bb_rct.centery = random.randint(0, HEIGHT)  # 縦初期座標
    vx, vy = +5, +5 # 爆弾の速度
    clock = pg.time.Clock()

    tmr = 0
    bb_imgs, bb_accs = init_bb_imgs()
    kk_dict = get_kk_imgs()
    while True:
        
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            print("ゲームオーバー")
            return
        screen.blit(bg_img, [0, 0]) #背景

        #爆弾１の速度と画像の更新
        avx = vx * bb_accs[min(tmr//500, 9)] #爆弾の速度を加速させる
        avy = vy * bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)] #爆弾の画像を更新する
        bb_img.set_colorkey((0, 0, 0))

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])#動きをなかったことにする
        screen.blit(kk_img, kk_rct) 

        #爆弾１の当たり判定と移動
        bb_rct.move_ip(avx, avy) #爆弾を移動させる
        bb_rct.width=bb_imgs[min(tmr//500, 9)].get_rect().width #爆弾の横サイズを更新 
        bb_rct.height=bb_imgs[min(tmr//500, 9)].get_rect().height #爆弾の縦サイズを更新
        kk_img = kk_dict.get(tuple(sum_mv), kk_dict[(0, 0)])

        yoko, tate = check_bound(bb_rct)
        if not yoko: #横方向にはみでているなら
            vx *= -1
        if not tate: #縦方向にはみでているなら
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

