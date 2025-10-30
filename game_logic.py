import random
import game_data
from game_data import MAP_SYMBOLS, game_log, LEVEL_UP_TABLE

def add_log(message):
    #ゲームログに新しいメッセージを追加する関数
    game_log.append(message)
    if len(game_log) > 50:
        game_log.pop

def get_movement_input():
    #プレイヤーの入力を受け付ける関数
    move = input("移動方向 (w/a/s/d)、またはメニュー(c)、終了(q)を入力").lower()
    return move

def is_valid_move(dungeon_map, target_x, target_y):
    # 移動先が壁じゃないかを確認する関数

    # マップの範囲外チェック
    if not (0 <= target_y < len(dungeon_map) and 0 <= target_x < len(dungeon_map[0])):
        return False
    
    # 移動先が壁じゃないかをチェックする
    if dungeon_map[target_y][target_x] == MAP_SYMBOLS["WALL"]:
        print("壁に阻まれた...")
        return False
    
    # あとでアイテムなどの追加
    return True
    
def handle_player_move(dungeon_map, status, enemies_list, items_list, dx, dy):
    #プレイヤーの移動とマップの更新を行う関数

    # 現在地の座標
    current_x, current_y = status['X'], status['Y']

    #移動先の座標
    new_x, new_y = current_x + dx , current_y + dy

    # 壁かどうかだけチェック
    if not is_valid_move(dungeon_map, new_x, new_y):
        return False
    
    # 移動先の中身をチェック
    target_tile = dungeon_map[new_y][new_x]

    if target_tile == MAP_SYMBOLS["ENEMY"]:
        # 移動先が敵のため、攻撃
        print("敵に攻撃!")
        combat(dungeon_map, status, enemies_list, new_x, new_y)
        consume_hunger(status)
        return True
    
    elif target_tile == MAP_SYMBOLS["STAIRS"]:
        # 移動先が階段のため、降りる
        add_log("階段を見つけた! 次の階層へ進む...")
        # 階層レベルを上げる
        status["Floor"] += 1

        game_data.game_state = "next_floor"
        return True
    
    elif target_tile == MAP_SYMBOLS["ITEM"]:
        
        # 1. まず、その座標にあるアイテムを items_list から探す
        target_item_data = None
        item_to_remove = None # 拾う場合に備えて、リスト本体も覚えておく
        for item in items_list:
            coords, data = item
            if coords == (new_x, new_y): # (new_x, new_y) は移動先の座標
                target_item_data = data
                item_to_remove = item
                break

        # 2. アイテムが見つかったかどうかで分岐
        if target_item_data:
            # --- アイテムが見つかった ---
            
            # 2a. 持ち物がいっぱいかチェック
            if len(status["inventory"]) >= MAX_INVENTORY_SIZE:
                # 満タンの場合：
                # (君の要望) どのアイテムの上に乗ったかログを出す
                add_log(f"持ち物がいっぱいで、{target_item_data['name']} の上に乗った。")
                # 拾わずに、そのまま下の「移動した。」処理へ進む
                pass
            
            else:
                # 持ち物に空きがある場合：
                # (pickup_item のロジックをここで実行)
                status["inventory"].append(target_item_data)
                items_list.remove(item_to_remove)
                add_log(f"{target_item_data['name']} を拾った!")
                # そのまま下の「移動した。」処理へ進む

        else:
            # --- アイテムが見つからなかった ---
            # (これは「見えないアイテム」バグ)
            add_log("（しかし、そこには何もなかった）")
            # そのまま下の「移動した。」処理へ進む
            pass
    

    #add_log("移動した。")
    # 1. 元の場所を床に戻す
    # 1. 元の場所をどうするか？
    #    (元の場所にアイテムリストのアイテムがあるか？)
    tile_to_set = MAP_SYMBOLS["FLOOR"] # 基本は床(.)
    for (item_x, item_y), _ in items_list:
        if (item_x, item_y) == (current_x, current_y):
            # 満タンで踏んだアイテムが、ここ(元の場所)にあるはず
            tile_to_set = MAP_SYMBOLS["ITEM"] 
            break # ループ終了
    dungeon_map[current_y][current_x] = tile_to_set

    # 2. プレイヤーの位置を更新
    status['X'], status['Y'] = new_x, new_y

    # 3. 新しい場所にプレイヤーシンボルを置く
    dungeon_map[new_y][new_x] = MAP_SYMBOLS["PLAYER"]

    # 4. 空腹度の消費
    consume_hunger(status)

    return True #移動成功

def consume_hunger(status):
    # 空腹度を計算する関数
    if status['Hung'] > 0:
        if status["HP"] < status["Max_HP"]:
            status["HP"] += 1
    else:
        status['HP'] -= 1

    status["turn_counter_for_hunger"] += 1

    if status["turn_counter_for_hunger"] >= 10:
        status['Hung'] = max(0, status['Hung'] - 1)
        if status['Hung'] == 50:
            add_log("少しお腹が空いてきた")
        elif status['Hung'] == 20:
            add_log("かなりお腹が空いてきた")
        elif status['Hung'] == 0:
            add_log("空腹で倒れそうだ...")
        status["turn_counter_for_hunger"] = 0
    
def handle_input(dungeon_map, status, enemies_list, items_list, move):
    #入力に応じた処理を呼び出す関数

    moved = False

    # WASDの移動処理
    if move == "w": # 上移動(Yが減る)
        moved = handle_player_move(dungeon_map, status, enemies_list, items_list, 0, -1)
    elif move == "s": # 下移動(Yが増える)
        moved = handle_player_move(dungeon_map, status, enemies_list, items_list, 0, 1)
    elif move == "a": # 左移動(Xが減る)
        moved = handle_player_move(dungeon_map, status, enemies_list, items_list, -1, 0)
    elif move == "d": # 右移動(Xが増える)
        moved = handle_player_move(dungeon_map, status, enemies_list, items_list, 1, 0)
    elif move == "c": # メニュー表示
        # 'c'が押されたらステートをcにする
        add_log("メニューを開いた")
        game_data.game_state = "menu"
        moved = False
    
    if moved:
        enemy_turn(dungeon_map, status, enemies_list)

    return move != 'q'

FLOOR_WIDTH = 40
FLOOR_HEIGHT = 20
MAX_ROOMS = 10
MAX_ENEMIES_PER_ROOM = 1
MAX_ITEM_PER_ROOM = 3
SIGHT_RANGE = 8
MAX_INVENTORY_SIZE = 10

def create_empty_floor(width, height):
    # 全体が壁のからのフロア(二次元リスト)を作成する関数

    return [[MAP_SYMBOLS["WALL"] for _ in range(width)] for _ in range(height)]

def create_room(dungeon_map, x, y, w, h):
    # 指定された座標に部屋を生成する関数
    for i in range(y, y + h):
        for j in range(x, x + w):
            if 0 < i < FLOOR_HEIGHT - 1 and 0 < j < FLOOR_WIDTH -1:
                dungeon_map[i][j] = MAP_SYMBOLS["FLOOR"]
    
    center_x = x + w // 2
    center_y = y + h // 2
    return {'x': x, 'y': y, 'w': w, 'h': h, 'center': (center_x, center_y)}

def connect_rooms(dungeon_map, start_point, end_point):
    # 2点をL字型の通路で繋ぐ関数
    x1, y1 = start_point
    x2, y2 = end_point  # <--- 修正①：終点(end_point) を使う

    # 1. X方向の通路を掘る (y1 の高さで)
    for x in range(min(x1, x2), max(x1, x2) + 1):
        # マップの端(0と最後)は壁のまま残したいので、 1 から (WIDTH-2) の範囲を掘る
        if 1 <= x < FLOOR_WIDTH - 1 and 1 <= y1 < FLOOR_HEIGHT - 1:
            dungeon_map[y1][x] = MAP_SYMBOLS["FLOOR"]
    
    # 2. Y方向の通路を掘る (x2 の位置で)
    for y in range(min(y1, y2), max(y1, y2) + 1):
         # マップの端(0と最後)は壁のまま残したいので、 1 から (HEIGHT-2) の範囲を掘る
        if 1 <= x2 < FLOOR_WIDTH - 1 and 1 <= y < FLOOR_HEIGHT - 1: # <--- 修正②： y を使う
            dungeon_map[y][x2] = MAP_SYMBOLS["FLOOR"]

def generate_dungeon(status):
    # ダンジョンマップ全体を生成するメイン関数 敵リストも追加

    dungeon_map = create_empty_floor(FLOOR_WIDTH, FLOOR_HEIGHT)
    rooms = []
    new_enemies_list = []
    new_item_list = []
    
    current_floor = status["Floor"] 

    for i in range(MAX_ROOMS):
        room_w = random.randint(5, 12)
        room_h = random.randint(4, 9)
        room_x = random.randint(1, FLOOR_WIDTH - room_w - 1)
        room_y = random.randint(1, FLOOR_HEIGHT - room_h - 1)

        # TODO: 部屋の重なりチェックはあとで実装。

        new_room = create_room(dungeon_map, room_x, room_y, room_w, room_h)
        rooms.append(new_room)

        # 最初の部屋以外に敵を配置する
        if i > 0:
            place_enemies(dungeon_map, new_room, new_enemies_list, current_floor)
            place_items(dungeon_map, new_room, new_item_list, current_floor)

        # 通路で繋ぐ
        if i > 0:
            prev_center = rooms[i - 1]['center']
            current_center = new_room['center']
            connect_rooms(dungeon_map, prev_center, current_center)
    
    # --- 修正点：ここから ---
    if rooms:
        # 1. 最初の部屋の中心にプレイヤーの「座標」を設定
        start_room = rooms[0]
        start_x, start_y = start_room['center']
        status["X"], status["Y"] = start_x, start_y

        # 2. 最後の部屋に階段を置く
        end_room = rooms[-1]
        end_x, end_y = end_room['center']
        
        # 3. (重要) プレイヤーの部屋と階段の部屋が同じ場合
        #    (つまり、部屋が1つしか生成されなかった場合)
        if start_room == end_room: 
            
            # 階段の位置をプレイヤー(中心)からずらす
            # (部屋の左上隅の、床になっている部分に置く)
            stair_x = end_room['x'] + 1 
            stair_y = end_room['y'] + 1
            
            # もしそこがプレイヤーの開始位置(中心)なら、さらにずらす
            # (部屋が 3x3 のように小さい場合への保険じゃ)
            if (stair_x, stair_y) == (start_x, start_y):
                stair_x += 1 
            
            # 念のため、そこが床(.)か確認する
            if dungeon_map[stair_y][stair_x] == MAP_SYMBOLS["FLOOR"]:
                dungeon_map[stair_y][stair_x] = MAP_SYMBOLS["STAIRS"]
            else:
                 # それでもダメなら、もう中心に置く (上書きされるが仕方ない)
                 dungeon_map[end_y][end_x] = MAP_SYMBOLS["STAIRS"]
                
        else:
            # 部屋が別なら、安全に最後の部屋の中心に置く
            dungeon_map[end_y][end_x] = MAP_SYMBOLS["STAIRS"]
    
    else:
         add_log("エラー：部屋が生成されませんでした。")
    # --- 修正点：ここまで ---
    
    return dungeon_map, new_enemies_list, new_item_list

def place_enemies(dungeon_map, room, enemies_list, current_floor):
    # 部屋の中にランダムに敵を配置する関数

    # この部屋に何体の敵を置くか決める
    num_enemies = random.randint(0, MAX_ENEMIES_PER_ROOM)

    for _ in range(num_enemies):
        # 敵を置ける床(.)を探す
        # 100回試行して、ランダムな床(.)を見つける
        for _ in range(100):
            enemy_x = random.randint(room['x'], room['x'] + room["w"] - 1)
            enemy_y = random.randint(room['y'], room['y'] + room['h'] - 1)

            # その場所が床(.)なら、敵を配置する
            if dungeon_map[enemy_y][enemy_x] == MAP_SYMBOLS["FLOOR"]:

                # 1. 敵のステータスを辞書で定義
                #    (今は仮)
                base_hp = 5 + (current_floor * 2)
                base_atk = 3 + (current_floor // 2)
                base_def = 1 + (current_floor // 3)
                base_exp = 5 + current_floor

                new_enemy = {
                    "HP": base_hp,
                    "Atk": base_atk,
                    "Def": base_def,
                    "Exp": base_exp,
                    "X": enemy_x,
                    "Y": enemy_y,
                    "standing_on": MAP_SYMBOLS["FLOOR"]
                }

                # 2. 敵リストに追加
                enemies_list.append(new_enemy)

                # 3. マップに 'E' を書き込む
                dungeon_map[enemy_y][enemy_x] = MAP_SYMBOLS["ENEMY"]

                # 1体配置したら次の敵へ
                break

def place_items(dungeon_map, room, items_list, current_floor):
    # 部屋の中にランダムにアイテムを配置する関数

    num_items = random.randint(0, MAX_ITEM_PER_ROOM)

    for _ in range(num_items):
        for _ in range(100):
            item_x = random.randint(room['x'], room['x'] + room['w'] - 1)
            item_y = random.randint(room['y'], room['y'] + room['h'] - 1)

            if dungeon_map[item_y][item_x] == MAP_SYMBOLS["FLOOR"]:

                # --- 修正点：ここから丸ごと置き換え ---
                
                new_item = None
                
                # 1. アイテムのマスターテーブル (確率は「重み」として使う)
                # (重み, 最小階層, 最大階層, アイテムデータ)
                item_table = [
                    # RARE (10F+)
                    (10, 10, 99, {"name": "鋼の剣", "type": "weapon", "atk_bonus": 8, "def_bonus": 0}),
                    (10, 10, 99, {"name": "鋼の盾", "type": "shield", "atk_bonus": 0, "def_bonus": 8}),
                    
                    # UNCOMMON (5F-15F)
                    (15, 5, 15, {"name": "鉄の剣", "type": "weapon", "atk_bonus": 5, "def_bonus": 0}),
                    (15, 5, 15, {"name": "鉄の盾", "type": "shield", "atk_bonus": 0, "def_bonus": 5}),
                    
                    # COMMON (1F-7F)
                    (20, 1, 7, {"name": "こん棒", "type": "weapon", "atk_bonus": 2, "def_bonus": 0}),
                    (20, 1, 7, {"name": "木の盾", "type": "shield", "atk_bonus": 0, "def_bonus": 2}),
                    
                    # CONSUMABLES (Always)
                    # (重みを少し増やしておきましたぞ)
                    (35, 1, 99, {"name": "おにぎり", "type": "food", "effect": 50}),
                    (45, 1, 99, {"name": "薬草", "type": "potion", "effect": 10}),
                ]

                # 2. この階層で「出現候補」になるアイテムリストを作る
                available_items = []
                total_weight = 0
                for (prob, min_floor, max_floor, item_data) in item_table:
                    if min_floor <= current_floor <= max_floor:
                        available_items.append((prob, item_data))
                        total_weight += prob # 重みを合計

                # 3. 候補リストから、重みに応じて1つ選ぶ
                if total_weight > 0:
                    item_roll = random.randint(1, total_weight)
                    cumulative_prob = 0
                    
                    for (prob, item_data) in available_items:
                        cumulative_prob += prob
                        if item_roll <= cumulative_prob:
                            new_item = item_data.copy()
                            break
                
                # 4. 万が一、候補が0だった場合 (テーブル設定ミスの保険)
                if new_item is None:
                    new_item = {"name": "薬草", "type": "potion", "effect": 10}
                
                # --- 修正点：ここまで ---

                dungeon_map[item_y][item_x] = MAP_SYMBOLS["ITEM"]
                items_list.append(((item_x, item_y), new_item))
                break

def combat(dungeon_map, player_status, enemies_list, enemy_x, enemy_y):
    # プレイヤーの攻撃処理を行う関数

    target_enemy = None
    
    # 座標から、攻撃対象の敵オブジェクトを探す
    for enemy in enemies_list:
        if enemy["X"] == enemy_x and enemy["Y"] == enemy_y:
            target_enemy = enemy
            break
    
    if target_enemy is None:
        add_log("エラー：見えない敵を攻撃してるね？旅人さん？")
        return
    
    # 2. ダメージ計算（プレイヤーの攻撃力 - 敵の防御力）
    player_atk = get_total_atk(player_status)
    enemy_def = target_enemy["Def"]

    base_damage = (player_atk * 100) // (100 + enemy_def)

    if player_atk <= 0:
        damage = 0
    
    if base_damage <= 0:
        damage = 0
    
    else:
        variance = random.uniform(0.9, 1.1)
        damage = round(base_damage * variance)
    
    enemy_pos = (target_enemy["X"], target_enemy["Y"])

    if damage > 0:
        target_enemy["HP"] -= damage
        add_log(f"敵{enemy_pos}に{damage}のダメージを与えた! (敵{enemy_pos}残りHP: {target_enemy['HP'] if target_enemy['HP'] > 0 else '0'})")
    else:
        add_log("敵は攻撃を弾いた！")
    
    # 3. 敵のHPが0以下になったかチェック
    if target_enemy["HP"] <= 0:
        add_log("敵を倒した!")
        enemy_exp = target_enemy.get("Exp", 1)
        gain_experience(player_status, enemy_exp)
        # マップから 'E' を消して床 '.' にする
        dungeon_map[enemy_y][enemy_x] = target_enemy["standing_on"]
        # 敵のリストから削除する
        enemies_list.remove(target_enemy)

def enemy_turn(dungeon_map, player_status, enemies_list):
    #すべての敵の行動処理を行う関数
    if not enemies_list:
        return
    
    player_x, player_y = player_status["X"], player_status["Y"]
    
    #敵が複数いてもいいようにリストをコピーして処理する
    for enemy in enemies_list[:]:
        if enemy not in enemies_list:
            continue

        enemy_x, enemy_y = enemy["X"], enemy["Y"]
        
        # --- 修正点：索敵と移動方向の決定 ---

        # 1. プレイヤーとの距離を計算 (マンハッタン距離)
        distance = abs(player_x - enemy_x) + abs(player_y - enemy_y)
        
        move_x = 0
        move_y = 0

        if distance <= SIGHT_RANGE:
            # 索敵範囲内：プレイヤーを追跡 (今までのロジック)
            # (プレイヤーの方向へ進む)
            move_x = 1 if player_x > enemy_x else -1 if player_x < enemy_x else 0
            move_y = 1 if player_y > enemy_y else -1 if player_y < enemy_y else 0
        
        else:
            # 索敵範囲外：ランダムウォーク
            # (上下左右 + 停止 の5択からランダムに選ぶ)
            possible_moves = [(0, -1), (0, 1), (-1, 0), (1, 0), (0, 0)]
            move_x, move_y = random.choice(possible_moves)

        # --- 修正点：ここまで ---
        
        # --- 移動試行 (ここからは元のロジックをそのまま使う) ---
        
        # 2. 優先方向を決定
        # (索敵範囲外のランダムウォークでも、この優先ロジックは
        #  X(例:0)とY(例:1)のどちらを先に試すかを決めるだけなので、問題なく機能する)
        if abs(player_x - enemy_x) >= abs(player_y - enemy_y):
            # Xを優先

            # 2-1. X方向を試す
            new_x, new_y = enemy_x + move_x, enemy_y
            if try_enemy_move_or_attack(dungeon_map, enemy, player_status, new_x, new_y):
                continue # 行動成功
            
            # 2-2. XがダメならY方向を試す
            new_x, new_y = enemy_x, enemy_y + move_y
            if try_enemy_move_or_attack(dungeon_map, enemy, player_status, new_x, new_y):
                continue # 行動成功
        else:
            # Y方向を優先
            
            # 2-1. Y方向を試す
            new_x, new_y = enemy_x, enemy_y + move_y
            if try_enemy_move_or_attack(dungeon_map, enemy, player_status, new_x, new_y):
                continue # 行動成功

            # 2-2. YがダメならX方向を試す
            new_x, new_y = enemy_x + move_x, enemy_y
            if try_enemy_move_or_attack(dungeon_map, enemy, player_status, new_x, new_y):
                continue # 行動成功
        
        # どの方向にも動けなかった場合 (袋小路 or 停止を選んだ)
        # (何もしない)

        

def enemy_attack_player(enemy, player_status):
    #敵がプレイヤーを攻撃する関数

    player_def = get_total_def(player_status)
    enemy_atk = enemy["Atk"]

    base_damage = (enemy_atk * 100) // (100 + player_def)

    if enemy_atk <= 0:
        damage = 0
    
    if base_damage <= 0:
        damage = 0
    
    else:
        variance = random.uniform(0.9, 1.1)
        damage = round(base_damage * variance)
    
    enemy_pos = (enemy['X'], enemy['Y'])

    if damage > 0:
        player_status["HP"] -= damage
        add_log(f"敵{enemy_pos}から{damage}のダメージを受けた! 残りHP: {player_status['HP']}")
    else:
        add_log(f"敵{enemy_pos}の攻撃をかわした!")

def try_enemy_move_or_attack(dungeon_map, enemy, player_status, new_x, new_y):
    """
    敵が (new_x, new_y) へ移動または攻撃を試みる関数
    Ver.4 (アイテム/階段の上もOK)
    """

    # 0. 移動先が現在地と同じなら失敗
    if new_x == enemy["X"] and new_y == enemy["Y"]:
        return False
    
    # 1. 移動先がマップ範囲外かチェック
    if not (0 <= new_y < FLOOR_HEIGHT and 0 <= new_x < FLOOR_WIDTH):
        return False
        
    target_tile = dungeon_map[new_y][new_x]
    
    # 2. 移動先はプレイヤー？
    if target_tile == MAP_SYMBOLS["PLAYER"]:
        enemy_attack_player(enemy, player_status)
        return True
    
    # --- 修正点：ここから ---
    
    # 3. 移動先は「壁」または「他の敵」か？
    #    (この2つ "以外" なら、移動できる)
    if target_tile in [MAP_SYMBOLS["WALL"], MAP_SYMBOLS["ENEMY"]]:
        return False # 移動失敗
        
    # --- 修正点：ここまで ---

    # 4. 移動実行
    #    (移動先は 床, アイテム, 階段 のいずれか)
    
    # 元いた場所を、隠していたタイル(床, アイテム, 階段)に戻す
    dungeon_map[enemy["Y"]][enemy["X"]] = enemy["standing_on"]
    
    # 新しい場所のタイル(床, アイテム, 階段)を 'standing_on' に保存
    enemy["standing_on"] = target_tile 
    
    # 座標を更新
    enemy["X"], enemy["Y"] = new_x, new_y
    
    # マップに 'E' を書き込む
    dungeon_map[new_y][new_x] = MAP_SYMBOLS["ENEMY"]
    return True

def get_menu_input():
    #メニュー用の入力を受け付ける
    move = input("使用するアイテムの番号(0, 1...)、捨てる(d)、 または 終了(x) を入力").lower()
    return move

def handle_menu_input(dungeon_map, status, enemies_list, items_list, action):
    #メニュー入力に応じた処理を呼び出す関数
    
    if action == "x":
        # xならメニューを閉じる
        game_data.game_state = "playing"
        add_log("メニューを閉じた")
        return True # ゲームは続行
    
    elif action == "d":
        # dが押されたら、捨てるモードに移行
        game_data.game_state = "drop_menu"
        add_log("何を捨てますか？")
    
    elif action.isdigit():
        #数字が入力されたら、アイテム使用/装備を試みる
        item_index = int(action)
        inventory = status["inventory"]

        # 1. 有効なインデックスかチェック
        if not (0 <= item_index < len(inventory)):
            add_log("その番号のアイテムは持っていない。")
            return True # ゲームは続行 (ターン消費なし)
        
        # 2. アイテムの種類によって処理を分岐
        item = inventory[item_index]
        item_type = item.get("type", "unknown")
        
        turn_consumed = False # ターンが消費されたか

        if item_type in ["potion", "food"]:
            # 消費アイテムの場合
            turn_consumed = use_item(status, item_index)
        
        elif item_type in ["weapon", "shield"]:
            # 装備アイテムの場合
            turn_consumed = equip_item(status, item_index)
            
        else:
            # どちらでもない場合
            add_log(f"{item.get('name')} は使ったり装備したりできない。")

        # 3. ターン消費の処理
        if turn_consumed:
            # アイテム使用/装備に成功したら、メニューを閉じて敵のターンへ
            game_data.game_state = "playing"
            # 敵のターンを呼び出す
            consume_hunger(status)
            enemy_turn(dungeon_map, status, game_data.enemies_list)
        else:
            # アイテム使用失敗(満タンなど)または装備失敗
            # (ログは各関数内で出ているはず)
            pass
            
    elif action == "q":
        return False # ゲーム終了
    
    return True # ゲーム続行

def get_drop_input():
    #捨てるアイテム用の入力
    move = input("捨てるアイテムの番号(0, 1...) または 終了(x) を入力").lower()
    return move

def drop_item(dungeon_map, player_status, items_list, item_index):
    """
    指定されたインデックスのアイテムを足元に置く関数
    
    - 足元にアイテムが「ない」場合は、そのまま置く (ドロップ)
    - 足元にアイテムが「ある」場合は、足元のアイテムを拾ってから置く (スワップ)
    """
    
    inventory = player_status["inventory"]
    
    # 1. 有効なインデックスかチェック
    if not (0 <= item_index < len(inventory)):
        add_log("その番号のアイテムは持っていない。")
        return False

    player_x, player_y = player_status["X"], player_status["Y"]
    
    # 2. 足元にあるアイテムを探す (スワップ用)
    item_on_floor_data = None
    item_on_floor_to_remove = None # items_list から削除するための実体
    
    for item in items_list:
        coords, data = item
        if coords == (player_x, player_y):
            item_on_floor_data = data
            item_on_floor_to_remove = item
            break # アイテムを1つ見つけたら終了
            
    # 3. 捨てるアイテムを取得 (インベントリから先に削除)
    item_to_drop = inventory.pop(item_index)

    # 4. 足元にアイテムがあったか？ (スワップ処理)
    if item_on_floor_data:
        
        # 4a. 足元のアイテムを items_list から削除
        items_list.remove(item_on_floor_to_remove)
        
        # 4b. 足元のアイテムをインベントリに追加
        # (注：10個の時に1個捨て(pop)てから1個拾うので、数は10個のまま。
        inventory.append(item_on_floor_data)
        
        # 4c. 捨てたアイテムを items_list に追加 (足元に置く)
        items_list.append(((player_x, player_y), item_to_drop))
        
        # 4d. マップの見た目は '!' のまま (変わらない)
        
        add_log(f"{item_on_floor_data['name']} を拾い、{item_to_drop['name']} を足元に置いた。")

    else:
        # 5. 足元に何もなかった場合 (通常のドロップ)
        
        # 5a. 捨てたアイテムを items_list に追加 (足元に置く)
        items_list.append(((player_x, player_y), item_to_drop))
        
        # 5b. マップの見た目を '!' に変更
        dungeon_map[player_y][player_x] = MAP_SYMBOLS["ITEM"]
        
        add_log(f"{item_to_drop['name']} を足元に捨てた。")

    return True # ターン消費

def handle_drop_input(dungeon_map, status, enemies_list, items_list, action):
    #捨てる入力に応じた処理を呼び出す関数
    if action == "x":
        # xならメニューを閉じる
        game_data.game_state = "playing"
        #add_log("捨てるのをやめた")
        return True
    
    elif action.isdigit():
        #数字が入力されたらアイテムを捨てる
        item_index = int(action)

        turn_consumed = drop_item(dungeon_map, status, items_list, item_index)

        if turn_consumed:
            game_data.game_state = "playing"
            consume_hunger(status)
            enemy_turn(dungeon_map, status, game_data.enemies_list)
        else:
            pass
    
    elif action == "q":
        return False
    
    return True
def use_item(player_status, item_index):
    #指定されたインデックスのアイテムを使用する関数

    inventory = player_status["inventory"]

    # 有効なインデックスかチェック
    if not (0 <= item_index < len(inventory)):
        add_log("無は使えないよ")
        return
    
    item_to_use = inventory[item_index]
    item_type = item_to_use.get("type", "unknown")

    if item_type == "potion":

        if player_status["HP"] >= player_status["Max_HP"]:
            add_log("もうHPは満タンだ。")
            return False

        # HP回復
        heal_amount = item_to_use["effect"]
        player_status["HP"] += heal_amount

        # Max_HPを超えないようにする
        if player_status["HP"] > player_status["Max_HP"]:
            player_status["HP"] = player_status["Max_HP"]
        
        add_log(f"{item_to_use['name']} を使った! HPが {heal_amount} 回復した!")

        inventory.pop(item_index)
        return True

    elif item_type == "food":

        recover_amount = item_to_use["effect"]

        if player_status["Hung"] >= player_status["Max_Hung"]:
            add_log("お腹は空いてない。")
            return False
        
        player_status["Hung"] = min(player_status["Max_Hung"], player_status["Hung"] + recover_amount)
        add_log(f"{item_to_use['name']} を食べた! 空腹度が {recover_amount} 回復した!")

        inventory.pop(item_index)
        return True
    
    elif item_type in ["weapon", "shield"]:
        add_log(f"{item_to_use['name']} は装備するものだ。")
        return False

    else:
        add_log(f"{item_to_use['name']} は今使えない。")
        return False

def equip_item(player_status, item_index):
    # 指定されたインデックスのアイテムを装備する関数
    inventory = player_status["inventory"]

    # アイテムが存在するか確認
    if not (0 <= item_index < len(inventory)):
        add_log("エラー: 無は装備できないよ")
        return False
    
    item_to_equip = inventory[item_index]
    item_type = item_to_equip.get("type")

    # 装備スロットを決定

    equip_slot = None
    if item_type == "weapon":
        equip_slot = "weapon"
    elif item_type == "shield":
        equip_slot = "shield"
    else:
       add_log(f"{item_to_equip.get('name')} は装備できない。")
       return False
    
    # 装備の交換処理
    current_equipment = player_status["Equipment"].get(equip_slot)

    if current_equipment:
        if len(player_status["inventory"]) >= MAX_INVENTORY_SIZE:
            add_log(f"持ち物がいっぱいで {current_equipment('name')} を外せない!")
            return False

    player_status["Equipment"][equip_slot] = item_to_equip

    inventory.pop(item_index)

    # 古い装備をインベントリに戻す
    if current_equipment:
        inventory.append(current_equipment)
        add_log(f"{current_equipment.get('name')} を外し、 {item_to_equip.get('name')} を装備した!")
    else:
        add_log(f"{item_to_equip.get('name')} を装備した!")
    
    return True
    
def get_total_atk(player_status):
    # 素のAtkと装備品のAtkボーナスを合計した値を返す
    base_atk = player_status["Atk"]
    weapon = player_status["Equipment"].get("weapon")

    if weapon:
        # 武器を装備していれば、ボーナスを加算
        base_atk += weapon.get("atk_bonus", 0)

    return base_atk

def get_total_def(player_status):
    # 素のDefと装備品のDefボーナスを合計した値を返す
    base_def = player_status["Def"]
    shield = player_status["Equipment"].get("shield")

    if shield:
        # 盾を装備していれば、ボーナスを加算
        base_def += shield.get("def_bonus", 0)
    
    return base_def

def gain_experience(player_status, exp_amount):
    
    player_status["Exp"] += exp_amount
    add_log(f"{exp_amount} の経験値を獲得した。(現在: {player_status['Exp']}/{player_status['Next_Exp']})")
    while player_status["Exp"] >= player_status["Next_Exp"]:
        level_up(player_status)

def level_up(player_status):

    next_level = player_status["Lv"] + 1
    level_data = LEVEL_UP_TABLE.get(next_level)

    if not level_data:
        player_status["Next_HP"] = 100000000
        add_log("君は最大レベルまで達したようだ。")
        player_status["Exp"] = player_status["Next_Exp"] - 1
        return
    
    player_status["Lv"] += 1
    player_status["Max_HP"] += level_data["Max_HP_Up"]
    player_status["Atk"] += level_data["Atk_Up"]
    player_status["Def"] += level_data["Def_Up"]

    player_status["HP"] = player_status["Max_HP"]
    # player_status["Hung"] = player_status["Max_Hung"]

    player_status["Exp"] -= player_status["Next_Exp"]
    player_status["Next_Exp"] = level_data["Next_Exp"]

    add_log(f"レベルが {player_status['Lv']} に上がった!")
    add_log(f"最大HPが {level_data['Max_HP_Up']}、攻撃力が {level_data['Atk_Up']}、防御力が {level_data['Def_Up']} 上がった!")

