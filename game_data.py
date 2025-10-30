#ゲームの現在の状態 ("playing", "menu", "next_floor")
game_state = "playing"

player_status = {
    "Lv": 1,
    "HP": 10,
    "Max_HP": 20,
    "Atk": 5,
    "Def": 3,
    "Hung": 100,
    "Max_Hung": 100,
    "Exp": 0,
    "Next_Exp": 10,

    "Equipment": {
        "weapon": None,
        "shield": None
    },

    "turn_counter_for_hunger": 0,
    # 現在の座標のX座標
    "X": 2,
    # 現在の座標のY座標
    "Y": 2,
    "Floor": 1,
    "inventory": []
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
    "STAIRS": '<',
    "ITEM": '!'
}

LEVEL_UP_TABLE ={
    2: {"Max_HP_Up": 5, "Atk_Up": 2, "Def_Up": 1, "Next_Exp": 25},
    3: {"Max_HP_Up": 5, "Atk_Up": 2, "Def_Up": 2, "Next_Exp": 50},
    4: {"Max_HP_Up": 6, "Atk_Up": 3, "Def_Up": 1, "Next_Exp": 100},
}