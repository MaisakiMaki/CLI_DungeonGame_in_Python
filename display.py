from game_data import player_status
from game_logic import get_total_atk, get_total_def

def clear_screen():
    # ターミナル画面をクリアにする関数
    print("\n" * 50)

def draw_map(dungeon_map):
    # マップの表示関数
    print(f"--- 鳳の間 {player_status['Floor']}階 ---")

    # マップの描画
    for row in dungeon_map:
        print("".join(row))

def draw_status(status):
    # ステータスの表示関数

    total_atk = get_total_atk(status)
    total_def = get_total_def(status)

    print("-" * 30)
    print(f"< Lv:{status['Lv']} HP:{status['HP']}/{status['Max_HP']} 空腹度:{status['Hung']}/{status['Max_Hung']}")
    print(f"< Atk:{total_atk} Def:{total_def}")
    print("-" * 30)

def draw_log(log_list):
    #ゲームのログを画面に描画する関数
    print("-" * 30)
    print("【ログ】")
    # ログリストの下から最大5件を表示する
    display_logs = log_list[-10:]
    for message in display_logs:
        print(f"> {message}")

def draw_menu(inventory, Equipment):
    #メニュー画面を描画する関数
    print("-" * 30)
    print("【装備】")
    weapon = Equipment.get("weapon")
    shield = Equipment.get("shield")

    print(f" 武器: {weapon['name'] if weapon else 'なし'} 盾: {shield['name'] if shield else 'なし'}")
    print("【持ち物】")

    if not inventory:
        print("何も持っていない。")
    else:
        #番号付きでアイテム一覧を表示
        for i, item in enumerate(inventory):
            print(f"{i}: {item['name']}")
    print("-" * 30)

def refresh_screen(dungeon_map, status, enemies_list, game_log, game_state):
    # 画面全体を更新する関数
    draw_map(dungeon_map)
    draw_status(status)
    draw_log(game_log)

    if game_state == "menu":
        draw_menu(status["inventory"], status["Equipment"])


