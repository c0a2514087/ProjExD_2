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
    vx, vy = +5, +5
    clock = pg.time.Clock()

    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            print("ゲームオーバー")
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])#動きをなかったことにする
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
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

