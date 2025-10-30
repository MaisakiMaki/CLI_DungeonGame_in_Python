import curses
import game_data
from game_data import player_status, DUNGEON_MAP, MAP_SYMBOLS, enemies_list, game_log
from display import refresh_screen, clear_screen
from game_logic import get_movement_input, handle_input, generate_dungeon, add_log, get_menu_input, handle_menu_input, enemy_turn, handle_drop_input, get_drop_input


def game_loop(stdscr, enemies_list, items_list):
    global DUNGEON_MAP, player_status
    
    is_running = True

    while is_running:
        
        
        # 2. 最新の状態を描画
        refresh_screen(stdscr, DUNGEON_MAP, player_status, enemies_list, items_list, game_log, game_data.game_state)

        # 3. ゲームの状態によって処理を分岐
        
        # 【修正】 game_state -> game_data.game_state
        if game_data.game_state == "playing":
            action = get_movement_input(stdscr)
            is_running = handle_input(DUNGEON_MAP, player_status, enemies_list, items_list, action)
        
        # 【修正】 game_state -> game_data.game_state
        elif game_data.game_state == "menu":
            action = get_menu_input(stdscr)
            is_running = handle_menu_input(DUNGEON_MAP, player_status, enemies_list, items_list, action)
        
        elif game_data.game_state == "drop_menu":
            action = get_drop_input(stdscr)
            is_running = handle_drop_input(DUNGEON_MAP, player_status, enemies_list, items_list, action)
        
        elif game_data.game_state == "next_floor":
            add_log(f"--- {player_status['Floor']}階に到達 ---")

            # 新しいマップ、敵、アイテムを生成
            DUNGEON_MAP, new_enemies_list, new_items_list = generate_dungeon(player_status)

            # メインのリストを新しいものに
            enemies_list.clear()
            enemies_list.extend(new_enemies_list)
            items_list.clear()
            items_list.extend(new_items_list)

            game_data.game_state = "playing"

            enemy_turn(DUNGEON_MAP, player_status, enemies_list)

        # 4. HPが0になったら終了
        if player_status['HP'] <= 0:
            add_log("GAME OVER...")
            is_running = False
            
        # 5. ループ終了の判定
        if not is_running:
            clear_screen()
            # 【修正】 game_state -> game_data.game_state
            refresh_screen(stdscr, DUNGEON_MAP, player_status, enemies_list, items_list, game_log, game_data.game_state)
            if player_status['HP'] <= 0:
                print("GAME OVER...")
            else:
                print("ゲームを終了しました。")
            
            add_log("何かキーを押すと終了します...")
            refresh_screen(stdscr, DUNGEON_MAP, player_status, enemies_list, items_list, game_log, game_data.game_state)
            stdscr.getch() # キー入力待ち
            break

def main_wrapper(stdscr):

    print("ローグライクゲーム起動")
    DUNGEON_MAP, new_enemies_list, new_items_list = generate_dungeon(player_status)

    add_log("ようこそ、鳳の間に。")
    game_loop(stdscr, new_enemies_list, new_items_list)

        

# メインプログラムの開始
if __name__ == "__main__":
    curses.wrapper(main_wrapper)