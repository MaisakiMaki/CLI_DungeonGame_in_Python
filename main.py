from game_data import player_status, DUNGEON_MAP, MAP_SYMBOLS
from display import refresh_screen
from game_logic import get_movement_input, handle_input

def game_loop():
    global DUNGEON_MAP, player_status

    is_running = True
    
    while is_running:

        refresh_screen(DUNGEON_MAP, player_status)

        action = get_movement_input()

        is_running = handle_input(DUNGEON_MAP, player_status, action)

        if player_status['HP'] <= 0:
            print("GAME OVER...")
            is_running = False

if __name__ == "__main__":
    print("ローグライクゲーム起動")

    DUNGEON_MAP[player_status['Y']][player_status['X']] = MAP_SYMBOLS["PLAYER"]

    game_loop()