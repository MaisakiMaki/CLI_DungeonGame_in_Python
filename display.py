from game_data import player_status

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
    print("-" * 30)
    print(f"< Lv:{status['Lv']} HP:{status['HP']}/{status['Max_HP']} 空腹度:{status['Hung']}/{status['Max_Hung']}")
    print("-" * 30)

def refresh_screen(dungeon_map, status, enemies_list):
    # 画面全体を更新する関数
    clear_screen()
    draw_map(dungeon_map)
    draw_status(status)

