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

        pickup_item(status, items_list, new_x, new_y)
    

    add_log("移動した。")
    # 1. 元の場所を床に戻す
    dungeon_map[current_y][current_x] = MAP_SYMBOLS["FLOOR"]

    # 2. プレイヤーの位置を更新
    status['X'], status['Y'] = new_x, new_y

    # 3. 新しい場所にプレイヤーシンボルを置く
    dungeon_map[new_y][new_x] = MAP_SYMBOLS["PLAYER"]

    # 4. 空腹度の消費
    consume_hunger(status)

    return True #移動成功

def consume_hunger(status):
    # 空腹度を計算する関数

    # 特定の歩数ごとに1消費するということロジックを後にかく
    # カウンタなどを使って実装予定、今は毎ターン消費
    status['Hung'] = max(0, status['Hung'] - 1)

    if status['Hung'] == 0:
        print("空腹でもう動けない...")
        # HP減少ロジックなどを追加
    

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
MAX_ENEMIES_PER_ROOM = 2
MAX_ITEM_PER_ROOM = 2

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

    # 新しい敵リスト
    new_enemies_list = []

    #この階層のアイテムリスト
    new_item_list = []

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
            place_enemies(dungeon_map, new_room, new_enemies_list)
            place_items(dungeon_map, new_room, new_item_list)

        # 通路で塞ぐ
        if i > 0:
            prev_center = rooms[i - 1]['center']
            current_center = new_room['center']
            connect_rooms(dungeon_map, prev_center, current_center)
    
    if rooms:
        # 最初の部屋の中心にプレイヤーを置く
        start_x, start_y = rooms[0]['center']
        status["X"], status["Y"] = start_x, start_y

        end_x, end_y = rooms[-1]['center']
        dungeon_map[end_y][end_x] = MAP_SYMBOLS["STAIRS"]
    
    return dungeon_map, new_enemies_list, new_item_list

def place_enemies(dungeon_map, room, enemies_list):
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
                new_enemy = {
                    "HP": 5,
                    "Atk": 2,
                    "Def": 1,
                    "Exp": 5,
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

def place_items(dungeon_map, room, items_list):
    # 部屋の中にランダムにアイテムを配置する関数

    num_items = random.randint(0, MAX_ITEM_PER_ROOM)

    for _ in range(num_items):
        for _ in range(100):
            item_x = random.randint(room['x'], room['x'] + room['w'] - 1)
            item_y = random.randint(room['y'], room['y'] + room['h'] - 1)

            # その場所が床(.)ならアイテムを配置
            if dungeon_map[item_y][item_x] == MAP_SYMBOLS["FLOOR"]:

                item_roll = random.randint(1, 100)
                new_item = None

                if item_roll <= 40:
                    new_item = {
                        "name": "薬草",
                        "type": "potion",
                        "effect": 10 # 10回復
                    }
                elif item_roll <= 70:
                    new_item = {
                        "name": "おにぎり",
                        "type": "food",
                        "effect": 50 # 10回復
                    }
                elif item_roll <= 85:
                    new_item = {
                        "name": "こんぼう",
                        "type": "weapon",
                        "atk_bonus": 2,
                        "def_bonus": 0
                    }
                else:
                    new_item = {
                        "name": "木の盾",
                        "type": "shield",
                        "atk_bonus": 0,
                        "def_bonus": 2 # 防御力 +2
                    }
                dungeon_map[item_y][item_x] = MAP_SYMBOLS["ITEM"]

                #アイテムリストに追加
                #x,y座標とアイテム辞書をダブルで保存

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
    # (game_data.py の Atk, Def を使うぞ)
    damage = max(0, player_status["Atk"] - target_enemy["Def"])
    enemy_pos = (target_enemy["X"], target_enemy["Y"])

    if damage > 0:
        target_enemy["HP"] -= damage
        add_log(f"敵{enemy_pos}に{damage}のダメージを与えた! (敵{enemy_pos}残りHP: {target_enemy['HP']})")
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

    #add_log("--- 敵のターン ---")
    if not enemies_list:
        #add_log("敵は誰もいなかった")
        return
    
    player_x, player_y = player_status["X"], player_status["Y"]
    
    #敵が複数いてもいいようにリストをコピーして処理する
    for enemy in enemies_list[:]:

        #敵がリストがら削除されているか確認
        if enemy not in enemies_list:
            continue

        enemy_x, enemy_y = enemy["X"], enemy["Y"]

        # --- 索敵と移動アルゴリズム ---

        move_x = 1 if player_x > enemy_x else -1 if player_x < enemy_x else 0
        move_y = 1 if player_y > enemy_y else -1 if player_y < enemy_y else 0

        if abs(player_x - enemy_x) >= abs(player_y - enemy_y):
            #Xを優先

            # Xを試す
            new_x, new_y = enemy_x + move_x, enemy_y
            if try_enemy_move_or_attack(dungeon_map, enemy, player_status, new_x, new_y):
                continue
            
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

        #add_log(f"敵({enemy['X']}, {enemy['Y']})はまごまごしている")


        

def enemy_attack_player(enemy, player_status):
    #敵がプレイヤーを攻撃する関数

    #ダメージ計算はアルテリオス
    damage = max(0, enemy["Atk"] - player_status["Def"])
    enemy_pos = (enemy['X'], enemy['Y'])

    if damage > 0:
        player_status["HP"] -= damage
        add_log(f"敵{enemy_pos}から{damage}のダメージを受けた! 残りHP: {player_status['HP']}")
    else:
        add_log(f"敵{enemy_pos}の攻撃をかわした!")

def try_enemy_move_or_attack(dungeon_map, enemy, player_status, new_x, new_y):

    # 0. 移動先が何もないなら失敗
    if new_x == enemy["X"] and new_y == enemy["Y"]:
        return False
    
    # 1. 移動先はプレイヤー？
    if dungeon_map[new_y][new_x] == MAP_SYMBOLS["PLAYER"]:
        enemy_attack_player(enemy, player_status)
        return True
    
    # 2. 移動先は有効な床か？
    if is_valid_move(dungeon_map, new_x, new_y) and \
       dungeon_map[new_y][new_x] != MAP_SYMBOLS["ENEMY"]:
        
        #移動を実行
        dungeon_map[enemy["Y"]][enemy["X"]] = enemy["standing_on"]
        enemy["standing_on"] = dungeon_map[new_y][new_x]
        enemy["X"], enemy["Y"] = new_x, new_y
        dungeon_map[new_y][new_x] = MAP_SYMBOLS["ENEMY"]
        return True
    
    return False

def pickup_item(player_status, items_list, item_x, item_y):

    target_item_data = None
    item_to_remove = None

    # 座標から、アイテムデータをitem_listから探す
    for item in items_list:
        coords, data = item
        if coords == (item_x, item_y):
            target_item_data = data
            item_to_remove = item
            break
    
    if target_item_data:
        #プレイヤーのインベントリに追加
        player_status["inventory"].append(target_item_data)

        # items_list から削除
        items_list.remove(item_to_remove)

        # ログに追加
        add_log(f"{target_item_data['name']} を拾った!")
    else:
        add_log("エラー：見えないアイテムを拾ったみたいだね、旅人さん")

def get_menu_input():
    #メニューようの入力を受け付ける
    move = input("使用するアイテムの番号(0, 1...) または 終了(x) を入力").lower()
    return move

def handle_menu_input(status, items_list, action):
    #メニュー入力に応じた処理を呼び出す関数
    global game_state
    
    if action == "x":
        # xならメニューを閉じる
        game_data.game_state = "playing"
        add_log("メニューを閉じた")
    
    elif action.isdigit():
        #数字が入力されたら、アイテム使用を試みる
        item_index = int(action)
        item_used = use_item(status, item_index)

        if item_used:
            #アイテムを使ったら自動でメニューを閉じてターンが進む
            game_data.game_state = "playing"
            # TODO: 敵のターンをここで呼び出す
            enemy_turn(game_data.DUNGEON_MAP, status, game_data.enemies_list)

    
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
    player_status["Hung"] = player_status["Max_Hung"]

    player_status["Exp"] -= player_status["Next_Exp"]
    player_status["Next_Exp"] = level_data["Next_Exp"]

    add_log(f"レベルが {player_status['Lv']} に上がった!")
    add_log(f"最大HPが {level_data['Max_HP_Up']}、攻撃力が {level_data['Atk_Up']}、防御力が {level_data['Def_Up']} 上がった!")