from game_data import player_status

def clear_screen():
    print("\n" * 50)

def draw_map(dungeon_map):
    print(f"--- 鳳の間 {player_status['Floor']}階 ---")

    for row in dungeon_map:
        print("".join(row))

def draw_status(status):
    print("-" * 30)
    print(f"< Lv:{status['Lv']} HP:{status['HP']}/{status['Max_HP']} 空腹度:{status['Hung']}/{status['Max_Hung']}")
    print("-" * 30)

def refresh_screen(dungeon_map, status):
    clear_screen()
    draw_map(dungeon_map)
    draw_status(status)

