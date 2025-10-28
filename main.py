from game_data import player_status, DUNGEON_MAP, MAP_SYMBOLS
from display import refresh_screen
from game_logic import get_movement_input, handle_input, generate_dungeon

def game_loop():
    # ゲームのメインループ

    global DUNGEON_MAP, player_status

    is_running = True
    
    while is_running:

        # 画面の更新
        refresh_screen(DUNGEON_MAP, player_status)

        # プレイヤーの入力を待つ
        action = get_movement_input()

        # 入力に応じた処理
        is_running = handle_input(DUNGEON_MAP, player_status, action)

        # HPが0になったら終了
        if player_status['HP'] <= 0:
            print("GAME OVER...")
            is_running = False

# メインプログラムの開始
if __name__ == "__main__":
    print("ローグライクゲーム起動")

    # 初期位置をマップに反映(最初のセットアップ)
    DUNGEON_MAP = generate_dungeon(player_status)
    DUNGEON_MAP[player_status['Y']][player_status['X']] = MAP_SYMBOLS["PLAYER"]

    # 敵やアイテムの初期配置ロジックはここに
    game_loop()