import curses
import game_data
from game_data import player_status, DUNGEON_MAP, MAP_SYMBOLS, enemies_list, game_log
from display import refresh_screen, clear_screen

from game_logic import (get_movement_input, handle_input, generate_dungeon, add_log, 
                        get_menu_input, handle_menu_input, enemy_turn, handle_drop_input, 
                        get_drop_input, get_quit_confirm_input, handle_quit_confirm_input,
                        is_affected_by, handle_status_effects)
import pygame

def game_loop(stdscr, dungeon_map, enemies_list, items_list):
    global player_status
    
    is_running = True

    while is_running:

        is_blind_now = is_affected_by(player_status, "BLIND")
        
        # 2. 最新の状態を描画 (これは stdscr が必要なので OK)
        refresh_screen(stdscr, dungeon_map, player_status, enemies_list, items_list, game_log, game_data.game_state, is_blind_now)

        num_player_actions = 1
        num_enemy_actions = 1

        equipped_ring = player_status["Equipment"].get("ring")
        is_fast = equipped_ring and equipped_ring.get("ability") == "act_twice"
        is_paralyzed = is_affected_by(player_status, "PARALYSIS")

        if is_fast and is_paralyzed:
            num_player_actions = 1
            num_enemy_actions = 1
        elif is_fast:
            num_player_actions = 2
            num_enemy_actions = 1
        elif is_paralyzed:
            num_player_actions = 1
            num_enemy_actions = 2

        # 3. ゲームの状態によって処理を分岐
        if game_data.game_state == "tutorial":
            # チュートリアル画面では、Enterキーだけを待つ
            key_code = stdscr.getch()
            if key_code == curses.KEY_ENTER or key_code == 10:
                game_data.game_state = "playing" # ゲーム開始
        
        elif game_data.game_state == "playing":
                for _ in range(num_player_actions):
                    if player_status['HP'] <= 0: break
                    action = get_movement_input(stdscr) # (get_... は stdscr が必要)
                    is_running = handle_input(dungeon_map, player_status, enemies_list, items_list, action)

                    if not is_running: break
                    if game_data.game_state != "playing": break
                    if num_player_actions > 1:
                        refresh_screen(stdscr, dungeon_map, player_status, enemies_list, items_list, game_log, game_data.game_state, is_blind_now)

                if not is_running or player_status['HP'] <= 0:
                    continue
                    
                if num_enemy_actions > 1:
                    add_log("動きが鈍く、敵が連続で行動する!")

                for _ in range(num_enemy_actions):
                    if player_status['HP'] <= 0: break
                    enemy_turn(dungeon_map, player_status, enemies_list)
        
        elif game_data.game_state == "menu":
            action = get_menu_input(stdscr) # (get_... は stdscr が必要)
            is_running = handle_menu_input(dungeon_map, player_status, enemies_list, items_list, action)
            if is_running and game_data.game_state == "playing":

                if num_enemy_actions > 1:
                    add_log("動きが鈍く、敵が連続で行動する!")

                for _ in range(num_enemy_actions):
                    if player_status['HP'] <= 0: break
                    enemy_turn(dungeon_map, player_status, enemies_list)


        
        elif game_data.game_state == "drop_menu":
            action = get_drop_input(stdscr) # (get_... は stdscr が必要)
            is_running = handle_drop_input(dungeon_map, player_status, enemies_list, items_list, action)
            if is_running and game_data.game_state == "playing":
                if num_enemy_actions > 1:
                    add_log("動きが鈍く、敵が連続で行動する!")

                for _ in range(num_enemy_actions):
                    if player_status['HP'] <= 0: break
                    enemy_turn(dungeon_map, player_status, enemies_list)
        
        elif game_data.game_state == "confirm_quit":
            action = get_quit_confirm_input(stdscr)
            is_running = handle_quit_confirm_input(action)

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
            is_blind_now = is_affected_by(player_status, "BLIND")
            refresh_screen(stdscr, dungeon_map, player_status, enemies_list, items_list, game_log, game_data.game_state, is_blind_now)

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

    try:
        curses.start_color()
        curses.use_default_colors()

        curses.init_pair(1, curses.COLOR_RED, -1)
        curses.init_pair(2, 227, -1)
        curses.init_pair(3, curses.COLOR_GREEN, -1) # ペア3: 緑 (プレイヤー)

    except curses.error:
        pass

    try:
        pygame.mixer.init() # 音楽エンジンを起動
        pygame.mixer.music.load('src/runateElf.mp3') # BGMを読み込む
        pygame.mixer.music.set_volume(0.1) # ★音量を 50% に設定 (0.0 ～ 1.0)
        pygame.mixer.music.play(-1) # ★-1 で「無限ループ再生」
    except Exception as e:
        add_log(f"BGMエラー: {e}")

    print("ローグライクゲーム起動")
    DUNGEON_MAP, new_enemies_list, new_items_list = generate_dungeon(player_status)

    add_log("ようこそ、鳳の間に。")
    game_loop(stdscr, DUNGEON_MAP, new_enemies_list, new_items_list)

    pygame.mixer.music.stop() # BGM停止

        

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