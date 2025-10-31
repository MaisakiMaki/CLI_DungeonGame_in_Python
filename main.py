import curses
import game_data
from game_data import player_status, DUNGEON_MAP, MAP_SYMBOLS, enemies_list, game_log
from display import refresh_screen, clear_screen
from game_logic import get_movement_input, handle_input, generate_dungeon, add_log, get_menu_input, handle_menu_input, enemy_turn, handle_drop_input, get_drop_input


def game_loop(stdscr, dungeon_map, enemies_list, items_list):
    global player_status
    
    is_running = True

    while is_running:
        
        # 2. 最新の状態を描画 (これは stdscr が必要なので OK)
        refresh_screen(stdscr, dungeon_map, player_status, enemies_list, items_list, game_log, game_data.game_state)

        # 3. ゲームの状態によって処理を分岐
        if game_data.game_state == "tutorial":
            # チュートリアル画面では、Enterキーだけを待つ
            key_code = stdscr.getch()
            if key_code == curses.KEY_ENTER or key_code == 10:
                game_data.game_state = "playing" # ゲーム開始
        
        elif game_data.game_state == "playing":
            action = get_movement_input(stdscr) # (get_... は stdscr が必要)
            is_running = handle_input(dungeon_map, player_status, enemies_list, items_list, action)
        
        elif game_data.game_state == "menu":
            action = get_menu_input(stdscr) # (get_... は stdscr が必要)
            is_running = handle_menu_input(dungeon_map, player_status, enemies_list, items_list, action)
        
        elif game_data.game_state == "drop_menu":
            action = get_drop_input(stdscr) # (get_... は stdscr が必要)
            is_running = handle_drop_input(dungeon_map, player_status, enemies_list, items_list, action)


        elif game_data.game_state == "next_floor":
            add_log(f"--- {player_status['Floor']}階に到達 ---")

            # 新しいマップ、敵、アイテムを生成
            dungeon_map, new_enemies_list, new_items_list = generate_dungeon(player_status)

            # メインのリストを新しいものに
            enemies_list.clear()
            enemies_list.extend(new_enemies_list)
            items_list.clear()
            items_list.extend(new_items_list)

            game_data.game_state = "playing"

            enemy_turn(dungeon_map, player_status, enemies_list)

        # 4. HPが0になったら終了
        if player_status['HP'] <= 0:
            game_data.game_state = "game_over" # <--- 修正点：状態を変える
            add_log("GAME OVER...")
            is_running = False
            
        # 5. ループ終了の判定
        if not is_running:
        
        # (ログを更新)
            if game_data.game_state != "game_over": # (q で終了した場合)
                add_log("ゲームを終了しました。")
        
        # --- 修正点：ログメッセージを変更 ---
            add_log("【Enterキー】を押すと終了します...")
        
        # (最終画面を描画)
            refresh_screen(stdscr, dungeon_map, player_status, enemies_list, items_list, game_log, game_data.game_state)

        # --- 修正点：ここから ---
        # 「何かキー」ではなく、「Enterキー」だけを待つ
            while True:
                key_code = stdscr.getch()
            
                # curses.KEY_ENTER (Enterキー) か、
                # (環境によっては)
                # 
                # (ASCIIコードの 10) をチェック
                if key_code == curses.KEY_ENTER or key_code == 10:
                    break
            # (それ以外のキー (w,a,s,dなど) は無視する)
        # --- 修正点：ここまで ---
            
            break

def main_wrapper(stdscr):

    print("ローグライクゲーム起動")
    DUNGEON_MAP, new_enemies_list, new_items_list = generate_dungeon(player_status)

    add_log("ようこそ、鳳の間に。")
    game_loop(stdscr, DUNGEON_MAP, new_enemies_list, new_items_list)

        

# メインプログラムの開始
if __name__ == "__main__":
    
    # --- 修正点：ここから ---
    try:
        # 1. curses の「お作法（wrapper）」を普通に呼ぶ
        curses.wrapper(main_wrapper)

    except Exception as e:
        # 2. (重要) もし curses がエラーを隠蔽（いんぺい）しようとしても、
        #    ここで捕まえて、強制的に表示する
        
        print("--- 墜落（クラッシュ）しました！ ---")
        print("エラーの原因:")
        import traceback
        traceback.print_exc()
        
    # --- 修正点：ここまで ---