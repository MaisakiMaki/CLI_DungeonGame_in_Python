from game_data import MAP_SYMBOLS

def get_movement_input():
    move = input("移動方向 (w/a/s/d)、またはメニュー(c)、終了(q)を入力").lower()
    return move

def is_valid_move(dungeon_map, target_x, target_y):
    if not (0 <= target_y < len(dungeon_map) and 0 <= target_x < len(dungeon_map[0])):
        return False
    
    if dungeon_map[target_y][target_x] == MAP_SYMBOLS["WALL"]:
        print("壁に阻まれた...")
        return False
    
    # あとでアイテムなどの追加
    return True
    
def handle_player_move(dungeon_map, status, dx, dy):
    current_x, current_y = status['X'], status['Y']

    new_x, new_y = current_x + dx , current_y + dy

    if is_valid_move(dungeon_map, new_x, new_y):
        dungeon_map[current_y][current_x] = MAP_SYMBOLS["FLOOR"]

        status['X'], status['Y'] = new_x, new_y
        dungeon_map[new_y][new_x] = MAP_SYMBOLS["PLAYER"]

        consume_hunger(status)

        return True
    return False

def consume_hunger(status):
    status['Hung'] = max(0, status['Hung'] - 1)

    if status['Hung'] == 0:
        print("空腹でもう動けない...")
    

def handle_input(dungeon_map, status, move):

    moved = False

    if move == "w":
        moved = handle_player_move(dungeon_map, status, 0, -1)
    elif move == "s":
        moved = handle_player_move(dungeon_map, status, 0, 1)
    elif move == "a":
        moved = handle_player_move(dungeon_map, status, -1, 0)
    elif move == "d":
        moved = handle_player_move(dungeon_map, status, 1, 0)
    elif move == "c":
        #あとで実装
        print("メニューが開かれました")
    
    return move != 'q'

