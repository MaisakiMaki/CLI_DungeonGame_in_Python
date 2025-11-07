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
        "shield": None,
        "ring": None
    },
    # (例: [{"type": "POISON", "turns": 10}, {"type": "CONFUSED", "turns": 5}])
    "status_effects": [],

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
    4: {"Max_HP_Up": 6, "Atk_Up": 3, "Def_Up": 2, "Next_Exp": 100},
    5: {"Max_HP_Up": 5, "Atk_Up": 3, "Def_Up": 2, "Next_Exp": 150},
    6: {"Max_HP_Up": 5, "Atk_Up": 4, "Def_Up": 1, "Next_Exp": 220},
    7: {"Max_HP_Up": 4, "Atk_Up": 1, "Def_Up": 2, "Next_Exp": 300},
    8: {"Max_HP_Up": 5, "Atk_Up": 2, "Def_Up": 2, "Next_Exp": 400},
    9: {"Max_HP_Up": 5, "Atk_Up": 3, "Def_Up": 2, "Next_Exp": 500},
    10: {"Max_HP_Up": 10, "Atk_Up": 5, "Def_Up": 3, "Next_Exp": 500},
    11: {"Max_HP_Up": 5, "Atk_Up": 3, "Def_Up": 2, "Next_Exp": 500},
    12: {"Max_HP_Up": 4, "Atk_Up": 2, "Def_Up": 2, "Next_Exp": 500},
    13: {"Max_HP_Up": 5, "Atk_Up": 3, "Def_Up": 2, "Next_Exp": 500},
    14: {"Max_HP_Up": 6, "Atk_Up": 2, "Def_Up": 2, "Next_Exp": 500},
    15: {"Max_HP_Up": 10, "Atk_Up": 5, "Def_Up": 2, "Next_Exp": 500},
    # HP41 ATK15 DEF10 lv5
    # HP70 ATK30 DEF20 lv10
    # HP100 ATK45 DEF30 lv15
}

# アイテムのマスターテーブル (重み, 最小階層, 最大階層, アイテムデータ)
ITEM_TABLE = [
    # BOSSDROP
    (0, 0, 0, {"name": "終わりの剣", "type": "weapon", "atk_bonus": 20, "def_bonus": 5}),
    (0, 0, 0, {"name": "始まりの盾", "type": "shield", "atk_bonus": 5, "def_bonus": 20}),
    (0, 0, 0, {"name": "オーロラの指輪", "type": "ring", "atk_bonus": 0, "def_bonus": 0, "ability": "aurora_veil"}),
    (0, 0, 0, {"name": "タキオンリング", "type": "ring", "atk_bonus": 0, "def_bonus": 0, "ability": "act_twice"}),

    # LEGEND (25F+)
    (5, 25, 99, {"name": "オリハルコンの剣", "type": "weapon", "atk_bonus": 15, "def_bonus": 3}),
    (5, 25, 99, {"name": "戦女神の盾", "type": "shield", "atk_bonus": 3, "def_bonus": 15}),
    (2, 25, 99, {"name": "奇跡のリング", "type": "ring", "atk_bonus": 0, "def_bonus": 0, "ability": "drain"}),
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
    # --- 1F-14F (vs Player Lv1-7, ATK 5-25) ---
    (50, 1, 14, {
        "name": "ゴブリン", "symbol": "G", "min_floor": 1,
        "base_HP": 10, "base_Atk": 5, "base_Def": 2, "base_Exp": 5,
        "ability": "rotten"
    }),
    (50, 5, 29, {
        "name": "スライム", "symbol": "S", "min_floor": 5,
        "base_HP": 20, "base_Atk": 5, "base_Def": 8, "base_Exp": 8,
        "ability": "split"
    }),
    (40, 5, 19, {
        "name": "石炭虫", "symbol": "C", "min_floor": 5,
        "base_HP": 25, "base_Atk": 5, "base_Def": 10, "base_Exp": 6,
        "ability": "burn"
    }),
    (30, 5, 14, {
        "name": "ポイズンスネーク", "symbol": "P", "min_floor": 5,
        "base_HP": 20, "base_Atk": 5, "base_Def": 3, "base_Exp": 7,
        "ability": "poison"
    }),
    (30, 10, 19, {
        "name": "速き者", "symbol": "F", "min_floor": 10,
        "base_HP": 25, "base_Atk": 3, "base_Def": 3, "base_Exp": 10,
        "ability": "act_twice"
    }),
    (30, 10, 24, {
        "name": "腐った死体", "symbol": "R", "min_floor": 10,
        "base_HP": 35, "base_Atk": 10, "base_Def": 8, "base_Exp": 12,
        "ability": "rotten"
    }),
    (30, 10, 19, {
        "name": "笑い歩く草", "symbol": "W", "min_floor": 10,
        "base_HP": 30, "base_Atk": 8, "base_Def": 5, "base_Exp": 10,
        "ability": "none"
    }),

    # --- 15F-29F (vs Player Lv8-12, ATK 30-45) ---
    # (Lv8/ATK30 の「一撃 (27-29dmg)」を耐えるため、HPを35-40に設定)
    (30, 15, 29, {
        "name": "ゴブリン隊長", "symbol": "H", "min_floor": 15,
        "base_HP": 35, "base_Atk": 12, "base_Def": 10, "base_Exp": 15,
        "ability": "none"
    }),
    (30, 15, 24, {
        "name": "暗黒の眼", "symbol": "D", "min_floor": 15,
        "base_HP": 35, "base_Atk": 15, "base_Def": 10, "base_Exp": 18,
        "ability": "blind"
    }),
    (30, 15, 29, {
        "name": "痺れ蛇", "symbol": "N", "min_floor": 15,
        "base_HP": 35, "base_Atk": 13, "base_Def": 10, "base_Exp": 18,
        "ability": "paralysis"
    }),
    (20, 20, 39, {
        "name": "オアシスクラゲ", "symbol": "O", "min_floor": 20,
        "base_HP": 50, "base_Atk": 10, "base_Def": 15, "base_Exp": 20,
        "ability": "heal"
    }),

    # --- 25F-39F (vs Player Lv12-14, ATK 45-55) ---
    # (Lv12/ATK45 の「一撃 (40-42dmg)」を耐えるため、HPを45-50に設定)
    (20, 25, 35, {
        "name": "ブレインショッカー", "symbol": "B", "min_floor": 25,
        "base_HP": 45, "base_Atk": 22, "base_Def": 10, "base_Exp": 25,
        "ability": "confuse"
    }),
    (20, 25, 39, {
        "name": "炎の鳥", "symbol": "I", "min_floor": 25,
        "base_HP": 45, "base_Atk": 25, "base_Def": 10, "base_Exp": 30,
        "ability": "burn"
    }),
    (20, 25, 39, {
        "name": "ジェットより速き者", "symbol": "J", "min_floor": 25,
        "base_HP": 45, "base_Atk": 12, "base_Def": 5, "base_Exp": 30,
        "ability": "act_twice"
    }),
    (20, 25, 39, {
        "name": "痺獣クイックシルバー", "symbol": "Q", "min_floor": 25,
        "base_HP": 45, "base_Atk": 20, "base_Def": 10, "base_Exp": 30,
        "ability": "paralysis"
    }),

    # --- 30F-50F (vs Player Lv13-15, ATK 50-63) ---
    # (Lv13/ATK50 の「一撃 (45-48dmg)」を耐えるため、HPを50-60に設定)
    (20, 30, 39, {
        "name": "押しだしの巨人", "symbol": "K", "min_floor": 30,
        "base_HP": 60, "base_Atk": 30, "base_Def": 10, "base_Exp": 35,
        "ability": "pusher"
    }),
    (20, 30, 39, {
        "name": "月うさぎ", "symbol": "M", "min_floor": 30,
        "base_HP": 10, "base_Atk": 40, "base_Def": 5, "base_Exp": 40,
        "ability": "gun_shot"
    }),
    (15, 30, 50, {
        "name": "ウラン鉱石虫", "symbol": "U", "min_floor": 30,
        "base_HP": 50, "base_Atk": 10, "base_Def": 45, "base_Exp": 30,
        "ability": "strong_poison"
    }),

    # --- 40F-50F (vs Player Lv15, ATK 63) ---
    # (Lv15/ATK63 の「一撃 (45-50dmg)」を耐えるため、HPを50-70に設定)
    (10, 40, 50, {
        "name": "ゴブリンの長老", "symbol": "E", "min_floor": 40,
        "base_HP": 60, "base_Atk": 40, "base_Def": 35, "base_Exp": 50,
        "ability": "none"
    }),
    (10, 40, 50, {
        "name": "玉兎ルナ", "symbol": "L", "min_floor": 40,
        "base_HP": 45, "base_Atk": 45, "base_Def": 5, "base_Exp": 50,
        "ability": "pro_shoot"
    }),
    (10, 40, 50, {
        "name": "光より速きタキオン", "symbol": "T", "min_floor": 40,
        "base_HP": 50, "base_Atk": 30, "base_Def": 20, "base_Exp": 60,
        "ability": "act_twice"
    }),
    (5, 40, 50, {
        "name": "ベールに覆われしオーロラ", "symbol": "V", "min_floor": 40,
        "base_HP": 60, "base_Atk": 25, "base_Def": 30, "base_Exp": 60,
        "ability": "aurora_veil"
    }),
    (10, 40, 50, {
        "name": "未確認生物ゼノイド", "symbol": "X", "min_floor": 40,
        "base_HP": 75, "base_Atk": 35, "base_Def": 40, "base_Exp": 70,
        "ability": "split"
    }),
    (5, 40, 50, {
        "name": "陰陽", "symbol": "Y", "min_floor": 40,
        "base_HP": 60, "base_Atk": 35, "base_Def": 35, "base_Exp": 70,
        "ability": "reverse"
    }),

    # --- BOSS (40F-50F) (固定ステータス) ---
    (1, 40, 50, {
        "name": "Ain", "symbol": "A", "min_floor": 40,
        "base_HP": 100, "base_Atk": 50, "base_Def": 50, "base_Exp": 200,
        "ability": "none"
    }),
    (1, 40, 50, {
        "name": "Zenith", "symbol": "Z", "min_floor": 40,
        "base_HP": 100, "base_Atk": 60, "base_Def": 30, "base_Exp": 200,
        "ability": "none"
    }),
]