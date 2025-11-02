import curses
from game_data import player_status
from game_logic import get_total_atk, get_total_def
import game_data

def clear_screen(stdscr):
    # ターミナル画面をクリアにする関数
    stdscr.clear()

def draw_map(stdscr, dungeon_map, player_status, enemies_list, items_list):
    # 0行目からマップを描画
    
    # 1. 描画用の「完成図」を作る (これは前回の手術と同じ)
    display_map = [row[:] for row in dungeon_map]

    # 1a. アイテム(!)を上書き
    for (ix, iy), item_data in items_list: 
        if 0 <= iy < len(display_map) and 0 <= ix < len(display_map[0]):
            display_map[iy][ix] = game_data.MAP_SYMBOLS["ITEM"]
    
    # 1b. 敵(E)を上書き
    for enemy in enemies_list:
        ex, ey = enemy['X'], enemy['Y']
        
        # (重要) 座標がマップ範囲内か、先にチェック
        # (※ 0 < ey ではなく 0 <= ey が正しい)
        if 0 <= ey < len(display_map) and 0 <= ex < len(display_map[0]):
            
            # (重要) チェックの「中」で、敵のシンボルを描画
            display_map[ey][ex] = enemy.get("symbol", game_data.MAP_SYMBOLS["ENEMY"])
            
    # 1c. プレイヤー(@)を上書き
    px, py = player_status['X'], player_status['Y']
    if 0 <= py < len(display_map) and 0 <= px < len(display_map[0]):
        display_map[py][px] = game_data.MAP_SYMBOLS["PLAYER"]

    # 2. 完成したマップを、(y, x) 座標を指定して描画
    # (0, 0) は左上隅
    stdscr.addstr(0, 0, f"--- 鳳の間 {player_status['Floor']}階 ---")
    
    for y, row in enumerate(display_map):
        # (y+1) で、階層表示の下 (1行目) からマップを描画
        stdscr.addstr(y + 1, 0, "".join(row))

def draw_status(stdscr, status):
    # マップの下 (y=21) にステータスを描画
    
    total_atk = get_total_atk(status)
    total_def = get_total_def(status)

    stdscr.addstr(22, 0, "-" * 30)
    stdscr.addstr(23, 0, f"< Lv:{status['Lv']} HP:{status['HP']}/{status['Max_HP']} 満腹度:{status['Hung']}/{status['Max_Hung']}")
    # (プロンプトと被らないよう、プロンプトは y=23 にした)
    stdscr.addstr(24, 0, f"< Atk:{total_atk} Def:{total_def}")
    # stdscr.addstr(24, 0, "-" * 30)

def draw_log(stdscr, log_list):
    # ログを画面の右側 (x=45) に描画
    
    stdscr.addstr(0, 45, "-" * 30)
    stdscr.addstr(1, 45, "【ログ】")
    
    display_logs = log_list[-10:] # 最大10件
    for i, message in enumerate(display_logs):
        # (y=2 から 11 まで)
        stdscr.addstr(i + 2, 45, f"> {message.ljust(27)}") # ljust で長さを揃える

def draw_menu(stdscr, inventory, Equipment):
    # メニュー画面を「画面全体」を使って描画
    
    stdscr.addstr(1, 2, "--- メニュー ---")
    
    stdscr.addstr(3, 2, "【装備】")
    weapon = Equipment.get("weapon")
    shield = Equipment.get("shield")
    stdscr.addstr(4, 4, f"武器: {weapon['name'] if weapon else 'なし'}")
    stdscr.addstr(5, 4, f"盾  : {shield['name'] if shield else 'なし'}")
    
    stdscr.addstr(7, 2, "【持ち物】")
    if not inventory:
        stdscr.addstr(8, 4, "何も持っていない。")
    else:
        # y=8 から y=17 までの10行
        for i, item in enumerate(inventory):
            if i >= 10: break 
            stdscr.addstr(i + 8, 4, f"{i}: {item['name']}")

def draw_tutorial_screen(stdscr):
    """チュートリアル画面を描画する関数"""
    stdscr.addstr(3, 5, "ようこそ、鳳の間に。")
    
    stdscr.addstr(6, 7, "--- 操作方法 ---")
    stdscr.addstr(8, 7, "--- プレイ画面中 ---")
    stdscr.addstr(9, 7, "w, a, s, d : 移動/攻撃")
    stdscr.addstr(10, 7, "c           : メニュー (アイテム使用 / 装備)")
    stdscr.addstr(11, 7, "q           : ゲーム終了")
    
    stdscr.addstr(13, 7, "@ : あなた")
    stdscr.addstr(14, 7, "A to Z : 敵")
    stdscr.addstr(15, 7, "! : アイテム")
    stdscr.addstr(16, 7, "< : 階段")


    stdscr.addstr(18, 7, "--- メニュー画面中 ---")
    stdscr.addstr(19, 7, "0 to 9 : アイテム選択")
    stdscr.addstr(20, 7, "d : アイテムを捨てる/床のアイテムと交換")
    
    stdscr.addstr(23, 5, "【Enterキー】を押してゲームを開始します...")

def refresh_screen(stdscr, dungeon_map, status, enemies_list, items_list, game_log, game_state):
    # 画面全体を更新する関数
    
    # 1. 画面をクリア (curses)
    stdscr.clear() 
    
    # --- 修正点：ここから ---
    
    # 2. HPに基づいて「文字色モード」を決定
    color_pair_num = 0 # 0 はデフォルト (白 on 黒)
    try:
        if status["Max_HP"] > 0:
            hp_percent = status['HP'] / status['Max_HP']
            if hp_percent <= 0.2:
                color_pair_num = 1 # 赤 (ペア1)
            elif hp_percent <= 0.5:
                color_pair_num = 2 # 黄色 (ペア2)
        
        # 画面全体に、決定した「文字色」を適用
        if color_pair_num != 0:
            stdscr.attron(curses.color_pair(color_pair_num))
        
    except curses.error:
        pass # 色が使えなくても続行
    # --- 修正点：ここまで ---

    try:
        # 3. 各パーツを描画
        # (attron のおかげで、これら全てが自動的に設定した色で描画される)
        if game_state == "menu" or game_state == "drop_menu":
            draw_menu(stdscr, status["inventory"], status["Equipment"])
        
        elif game_state == "tutorial":
            draw_tutorial_screen(stdscr)
            
        else: # (game_state == "playing" など)
            draw_map(stdscr, dungeon_map, status, enemies_list, items_list)
            draw_status(stdscr, status)
            draw_log(stdscr, game_log)

    except curses.error:
        pass 
        
    # --- 修正点：ここから ---
    # 4. 適用した「文字色」を解除
    try:
        if color_pair_num != 0:
            stdscr.attroff(curses.color_pair(color_pair_num))
    except curses.error:
        pass
    # --- 修正点：ここまで ---

    # 5. 最後に、画面を「更新（リフレッシュ）」
    stdscr.refresh()

