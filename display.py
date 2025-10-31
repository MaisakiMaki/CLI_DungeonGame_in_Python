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
        if 0 <= ey < len(display_map) and 0 <= ex < len(display_map[0]):
            display_map[ey][ex] = game_data.MAP_SYMBOLS["ENEMY"]
            
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
    # stdscr.addstr(23, 0, f"< Atk:{total_atk} Def:{total_def}")
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

def refresh_screen(stdscr, dungeon_map, status, enemies_list, items_list, game_log, game_state):
    # 画面全体を更新する関数
    
    # 1. 画面をクリア (curses)
    stdscr.clear()
    
    try:
        # --- 修正点：ここから ---
        if game_state == "menu" or game_state == "drop_menu":
            # 2a. 「メニュー画面」を描画
            # (マップ、ステータス、ログは描画しない)
            draw_menu(stdscr, status["inventory"], status["Equipment"])
            
            # (この後、game_logic.py の get_menu_input が
            #  y=25 にプロンプトを描画する)
            
        else: # (game_state == "playing" などの場合)
            # 2b. 「通常のゲーム画面」を描画
            draw_map(stdscr, dungeon_map, status, enemies_list, items_list)
            draw_status(stdscr, status)
            draw_log(stdscr, game_log)
            
            # (この後、game_logic.py の get_movement_input が
            #  y=25 にプロンプトを描画する)
        # --- 修正点：ここまで ---

    except curses.error:
        pass # (ウィンドウサイズが小さすぎるとエラー)

    # 3. 最後に、画面を「更新（リフレッシュ）」
    stdscr.refresh()

