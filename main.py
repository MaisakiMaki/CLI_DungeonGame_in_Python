from game_data import player_status, DUNGEON_MAP, MAP_SYMBOLS, enemies_list, game_log
from display import refresh_screen, clear_screen
from game_logic import get_movement_input, handle_input, generate_dungeon, add_log


def game_loop(enemies_list, items_list):
    # ゲームのメインループ

    global DUNGEON_MAP, player_status
    is_running = True
    
    # clear_screen() と refresh_screen() はループの外からは消す！

    while is_running:

        # 1. 【重要】まず画面をクリア
        clear_screen()
        
        # 2. 最新の状態を描画（前回のログもここで表示される）
        refresh_screen(DUNGEON_MAP, player_status, enemies_list, game_log)

        # 3. プレイヤーの入力を待つ
        action = get_movement_input()

        # 4. 入力に応じた処理 (ここで game_log が更新される)
        is_running = handle_input(DUNGEON_MAP, player_status, enemies_list, items_list, action)

        # 5. HPが0になったら終了
        if player_status['HP'] <= 0:
            add_log("GAME OVER...")
            is_running = False # 次のループで終了
            
        # 6. ループ終了の判定 (HPゼロまたは'q'入力)
        if not is_running:
            # 最後のログをもう一度表示
            clear_screen()
            refresh_screen(DUNGEON_MAP, player_status, enemies_list, game_log)
            if player_status['HP'] <= 0:
                print("GAME OVER...")
            else:
                print("ゲームを終了しました。")
            break # ループを抜ける
        

# メインプログラムの開始
if __name__ == "__main__":
    print("ローグライクゲーム起動")

    # 初期位置をマップに反映(最初のセットアップ)
    DUNGEON_MAP, new_enemies_list, new_items_list = generate_dungeon(player_status)
    DUNGEON_MAP[player_status['Y']][player_status['X']] = MAP_SYMBOLS["PLAYER"]

    # 敵やアイテムの初期配置ロジックはここに

    add_log("ようこそ、鳳の間に。")
    game_loop(new_enemies_list, new_items_list)