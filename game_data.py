#ゲームの現在の状態 ("playing", "menu", "next_floor", "tutorial", "game_over")
game_state = "tutorial"

player_status = {
    "Lv": 1,
    "HP": 20,
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
    5: {"Max_HP_Up": 6, "Atk_Up": 3, "Def_Up": 2, "Next_Exp": 150},
    6: {"Max_HP_Up": 5, "Atk_Up": 4, "Def_Up": 1, "Next_Exp": 220},
    7: {"Max_HP_Up": 4, "Atk_Up": 1, "Def_Up": 1, "Next_Exp": 300},
    8: {"Max_HP_Up": 5, "Atk_Up": 2, "Def_Up": 2, "Next_Exp": 400},
    9: {"Max_HP_Up": 5, "Atk_Up": 3, "Def_Up": 1, "Next_Exp": 500},
    10: {"Max_HP_Up": 10, "Atk_Up": 5, "Def_Up": 3, "Next_Exp": 0}
}

# アイテムのマスターテーブル (重み, 最小階層, 最大階層, アイテムデータ)
ITEM_TABLE = [
    # LEGEND (25F+)
    (5, 25, 99, {"name": "オリハルコンの剣", "type": "weapon", "atk_bonus": 15, "def_bonus": 3}),
    (5, 25, 99, {"name": "戦女神の盾", "type": "shield", "atk_bonus": 3, "def_bonus": 15}),
    # EPIC (15F - 24F)
    (10, 15, 24, {"name": "ミスリルの剣", "type": "weapon", "atk_bonus": 12, "def_bonus": 0}),
    (10, 15, 24, {"name": "ミスリルの盾", "type": "shield", "atk_bonus": 0, "def_bonus": 12}),
    # RARE (10F - 19F)
    (10, 10, 19, {"name": "鋼の剣", "type": "weapon", "atk_bonus": 8, "def_bonus": 0}),
    (10, 10, 19, {"name": "鋼の盾", "type": "shield", "atk_bonus": 0, "def_bonus": 8}),
    # UNCOMMON (5F-14F)
    (15, 5, 14, {"name": "鉄の剣", "type": "weapon", "atk_bonus": 5, "def_bonus": 0}),
    (15, 5, 14, {"name": "鉄の盾", "type": "shield", "atk_bonus": 0, "def_bonus": 5}),
    # COMMON (1F-7F)
    (20, 1, 7, {"name": "こん棒", "type": "weapon", "atk_bonus": 2, "def_bonus": 0}),
    (20, 1, 7, {"name": "木の盾", "type": "shield", "atk_bonus": 0, "def_bonus": 2}),
    # CONSUMABLES (Always / 10F+)
    (35, 1, 99, {"name": "おにぎり", "type": "food", "effect": 50}),
    (45, 1, 99, {"name": "薬草", "type": "potion", "effect": 10}),
    (20, 10, 99, {"name": "大きなおにぎり", "type": "food", "effect": 100}),
    (30, 10, 99, {"name": "上薬草", "type": "potion", "effect": 25}),
]

ENEMY_TABLE = [
    # (スライム: 1-5階)
    (50, 1, 5, {
        "name": "スライム", "symbol": "S",
        "base_HP": 5, "base_Atk": 3, "base_Def": 1, "base_Exp": 2
    }),
    # (ゴブリン: 3-10階)
    (30, 3, 10, {
        "name": "ゴブリン", "symbol": "G",
        "base_HP": 8, "base_Atk": 5, "base_Def": 2, "base_Exp": 5
    }),
    # (オーク: 8-15階)
    (20, 8, 15, {
        "name": "オーク", "symbol": "O",
        "base_HP": 15, "base_Atk": 8, "base_Def": 4, "base_Exp": 10
    }),
]