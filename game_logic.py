import random
from game_data import MAP_SYMBOLS

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
    
def handle_player_move(dungeon_map, status, dx, dy):
    #プレイヤーの移動とマップの更新を行う関数

    # 現在地の座標
    current_x, current_y = status['X'], status['Y']

    #移動先の座標
    new_x, new_y = current_x + dx , current_y + dy

    if is_valid_move(dungeon_map, new_x, new_y):

        # 1. 元の場所を床に戻す
        dungeon_map[current_y][current_x] = MAP_SYMBOLS["FLOOR"]

        # 2. プレイヤーの位置を更新
        status['X'], status['Y'] = new_x, new_y

        # 3. 新しい場所にプレイヤーシンボルを置く
        dungeon_map[new_y][new_x] = MAP_SYMBOLS["PLAYER"]

        # 4. 空腹度の消費
        consume_hunger(status)

        return True #移動成功
    return False # 移動失敗

def consume_hunger(status):
    # 空腹度を計算する関数

    # 特定の歩数ごとに1消費するということロジックを後にかく
    # カウンタなどを使って実装予定、今は毎ターン消費
    status['Hung'] = max(0, status['Hung'] - 1)

    if status['Hung'] == 0:
        print("空腹でもう動けない...")
        # HP減少ロジックなどを追加
    

def handle_input(dungeon_map, status, enemies_list, move):
    #入力に応じた処理を呼び出す関数

    moved = False

    # WASDの移動処理
    if move == "w": # 上移動(Yが減る)
        moved = handle_player_move(dungeon_map, status, 0, -1)
    elif move == "s": # 下移動(Yが増える)
        moved = handle_player_move(dungeon_map, status, 0, 1)
    elif move == "a": # 左移動(Xが減る)
        moved = handle_player_move(dungeon_map, status, -1, 0)
    elif move == "d": # 右移動(Xが増える)
        moved = handle_player_move(dungeon_map, status, 1, 0)
    elif move == "c": # メニュー表示
        #あとで実装
        print("メニューが開かれました")
    
    return move != 'q'

FLOOR_WIDTH = 40
FLOOR_HEIGHT = 20
MAX_ROOMS = 10
MAX_ENEMIES_PER_ROOM = 2

def create_empty_floor(width, height):
    # 全体が壁のからのフロア(二次元リスト)を作成する関数

    return [[MAP_SYMBOLS["WALL"] for _ in range(width)] for _ in range(height)]

def create_rooms(dungeon_map, x, y, w, h):
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
    x2, y2 = start_point

    # 1. X方向の通路を掘る
    for x in range(min(x1, x2), max(x1, x2) + 1):
        if 0 < x < FLOOR_WIDTH - 1 and 0 < y1 < FLOOR_HEIGHT - 1:
            dungeon_map[y1][x] = MAP_SYMBOLS["FLOOR"]
    
    # 2. Y方向の通路を掘る
    for y in range(min(y1, y2), max(y1, y2) + 1):
        if 0 < x2 < FLOOR_WIDTH - 1 and 0 < y1 < FLOOR_HEIGHT - 1:
            dungeon_map[y][x2] = MAP_SYMBOLS["FLOOR"]

def generate_dungeon(status):
    # ダンジョンマップ全体を生成するメイン関数 敵リストも追加

    dungeon_map = create_empty_floor(FLOOR_WIDTH, FLOOR_HEIGHT)
    rooms = []

    # 新しい敵リスト
    new_enemies_list = []

    for i in range(MAX_ROOMS):
        room_w = random.randint(5, 12)
        room_h = random.randint(4, 9)
        room_x = random.randint(1, FLOOR_WIDTH - room_w - 1)
        room_y = random.randint(1, FLOOR_HEIGHT - room_h - 1)

        # TODO: 部屋の重なりチェックはあとで実装。

        new_room = create_rooms(dungeon_map, room_x, room_y, room_w, room_h)
        rooms.append(new_room)

        # 最初の部屋以外に敵を配置する
        if i > 0:
            place_enemies(dungeon_map, new_room, new_enemies_list)

        # 通路で塞ぐ
        if i > 0:
            prev_center = rooms[0]['center']
            current_center = new_room['center']
            connect_rooms(dungeon_map, prev_center, current_center)
    
    if rooms:
        # 最初の部屋の中心にプレイヤーを置く
        start_x, start_y = rooms[0]['center']
        status["X"], status["Y"] = start_x, start_y

        end_x, end_y = rooms[-1]['center']
        dungeon_map[end_y][end_x] = MAP_SYMBOLS["STAIRS"]
    
    return dungeon_map, new_enemies_list

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
                    "X": enemy_x,
                    "Y": enemy_y
                }

                # 2. 敵リストに追加
                enemies_list.append(new_enemy)

                # 3. マップに 'E' を書き込む
                dungeon_map[enemy_y][enemy_x] = MAP_SYMBOLS["ENEMY"]

                # 1体配置したら次の敵へ
                break

