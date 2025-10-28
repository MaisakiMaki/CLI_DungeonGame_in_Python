player_status = {
    "Lv": 1,
    "HP": 20,
    "Max_HP": 20,
    "Atk": 5,
    "Def": 3,
    "Hung": 100,
    "Max_Hung": 100,
    # 現在の座標のX座標
    "X": 2,
    # 現在の座標のY座標
    "Y": 2,
    "Floor": 1
}


# DUNGEON_MAP は空
DUNGEON_MAP = []

# この階層に出現する敵のリスト
enemies_list = []

game_log = []

# MAP記号の定義
MAP_SYMBOLS = {
    "WALL": '#',
    "FLOOR": '.',
    "PLAYER": '@',
    "ENEMY": 'E',
    "STAIRS": '<'
}