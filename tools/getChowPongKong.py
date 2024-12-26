import pandas as pd
import numpy as np


#need to extract first too

# 載入數據
csv_path = 'processed_mahjong_data.csv'
data = pd.read_csv(csv_path)

# 定義索引標籤
index_labels = [
    "Dora indicators", "POV hand", "P0 melds", "P1 melds", "P2 melds", "P3 melds",
    "P0 pool", "P1 pool", "P2 pool", "P3 pool",
    "P0 discards", "P1 discards", "P2 discards", "P3 discards"
]
first_row_labels = [
    "Round wind", "Dealer", "POV player", "Riichi sticks", "Honba sticks", "Wall tiles",
    "P0 score", "P1 score", "P2 score", "P3 score", "P0 riichi", "P1 riichi", "P2 riichi", "P3 riichi",
    *["Padding"] * 18,
    "Round Number", "Step Number"
]
remaining_rows_labels = [
    "1 man", "2 man", "3 man", "4 man", "5 man", "6 man", "7 man", "8 man", "9 man",
    "1 pin", "2 pin", "3 pin", "4 pin", "5 pin", "6 pin", "7 pin", "8 pin", "9 pin",
    "1 sou", "2 sou", "3 sou", "4 sou", "5 sou", "6 sou", "7 sou", "8 sou", "9 sou",
    "East", "South", "West", "North", "Haku", "Hatsu", "Chun"
]

# 定義檢查吃牌和碰牌的函數
def can_chow(hand, discard_tile):
    suits = ['man', 'pin', 'sou']
    tile_name_to_index = {
        'man': list(range(9)),
        'pin': list(range(9, 18)),
        'sou': list(range(18, 27))
    }
    for suit in suits:
        for i in range(1, 8):
            if hand[tile_name_to_index[suit][i-1]] > 0 and hand[tile_name_to_index[suit][i]] > 0 and discard_tile == f"{i+1} {suit}":
                return True
            if hand[tile_name_to_index[suit][i]] > 0 and hand[tile_name_to_index[suit][i+1]] > 0 and discard_tile == f"{i} {suit}":
                return True
            if hand[tile_name_to_index[suit][i-1]] > 0 and hand[tile_name_to_index[suit][i+1]] > 0 and discard_tile == f"{i} {suit}":
                return True
    return False

def can_pung(hand, discard_tile):
    if hand is None:
        return False
    tile_index = remaining_rows_labels.index(discard_tile)
    return hand[tile_index] >= 2

def can_kong(hand, discard_tile):
    if hand is None:
        return False
    tile_index = remaining_rows_labels.index(discard_tile)
    return hand[tile_index] >= 3

def detect_melds_change(round, previous_melds, current_melds):
    if previous_melds is None or current_melds is None:
        return None
    diffs = np.where(previous_melds != current_melds)[0]
    if len(diffs) == 3:
        # 檢查是否是吃牌
        meld_tiles = [remaining_rows_labels[idx] for idx in diffs]
        if len(set(meld_tiles)) == 3:
            # 三個不同的牌，可能是吃牌
            return 'chow'
    elif len(diffs) == 1:
        # 檢查是否是碰牌或槓牌
        diff_index = diffs[0]
        if current_melds[diff_index] == 4:
            return 'kong'
        else:
            return 'pong'
    return None

# 解析數據和檢查吃牌碰牌
chow_rounds = []
pong_rounds = []
kong_rounds = []

nowRound = -1

hands = {f"P{i}_hand": None for i in range(4)}
full_hands = {f"P{i}_full_hand": None for i in range(4)}
melds = {f"P{i}_melds": None for i in range(4)}

previous_discard = None
previous_discard_num = None

for row_index in range(1, len(data) - 1):
    row_data = data.iloc[row_index, :-1].values
    output = data.iloc[row_index][510]
    reshaped_data = row_data.reshape(15, 34)

    # 分割數據
    first_row_df = pd.DataFrame([reshaped_data[0]], columns=first_row_labels)
    remaining_rows_df = pd.DataFrame(reshaped_data[1:], index=index_labels, columns=remaining_rows_labels)

    getRound = first_row_df['Round Number'].iloc[0]
    pov_player = first_row_df['POV player'].iloc[0]
    player_hand = remaining_rows_df.loc['POV hand'].values  
    current_melds = remaining_rows_df.loc[f'P0 melds'].values

    if nowRound != getRound:
        nowRound = getRound
        hands = {f"P{i}_hand": None for i in range(4)}
        melds = {f"P{i}_melds": None for i in range(4)}

    if previous_discard is not None and pov_player is not None:
        previous_player = (pov_player - 1) % 4
        previous_discard_tile = remaining_rows_labels[previous_discard_num]

        meld_change = detect_melds_change(row_index, melds[f'P{pov_player}_melds'], current_melds)
        if meld_change == 'chow':
            chow_rounds.append((row_index, pov_player, 'chow', True, previous_discard_tile, hands[f'P{pov_player}_hand'], full_hands[f'P{pov_player}_full_hand']))
        elif meld_change == 'pong':
            pong_rounds.append((row_index, pov_player, 'pong', True, previous_discard_tile, hands[f'P{pov_player}_hand'], full_hands[f'P{pov_player}_full_hand']))
        elif meld_change == 'kong':
            kong_rounds.append((row_index, pov_player, 'kong', True, previous_discard_tile, hands[f'P{pov_player}_hand'], full_hands[f'P{pov_player}_full_hand']))

        # 檢查吃牌
        if can_chow(player_hand, previous_discard_tile) and previous_discard_num < 27 and meld_change != "chow":
            chow_rounds.append((row_index, pov_player, 'chow', False, previous_discard_tile, player_hand, remaining_rows_df.values))
        # 檢查碰牌
        for i in range(4):
          if can_pung(hands[f'P{i}_hand'], previous_discard_tile) and meld_change != "pong":
              pong_rounds.append((row_index, pov_player, 'pong', False, previous_discard_tile, hands[f'P{i}_hand'], full_hands[f'P{i}_full_hand']))
        
        for i in range(4):
          if can_kong(hands[f'P{i}_hand'], previous_discard_tile) and meld_change != "kong":
              kong_rounds.append((row_index, pov_player, 'kong', False, previous_discard_tile,hands[f'P{i}_hand'], full_hands[f'P{i}_full_hand']))

          

    # 更新玩家的手牌和吃碰資訊
    hands[f'P{pov_player}_hand'] = player_hand
    full_hands[f'P{pov_player}_full_hand'] = remaining_rows_df.values
    melds[f'P{pov_player}_melds'] = current_melds

    # 更新前一回合打出的牌
    previous_data = row_data
    previous_discard = remaining_rows_labels[output]
    previous_discard_num = int(output)

# 輸出結果
for round_info in chow_rounds:
    round_idx, player, action, taken, discard_tile, hand, full_hand = round_info
    # print(f"Round {round_idx}: Player {player} can {action} ({discard_tile}). Action taken: {taken}")
    print(f"can {action} ({discard_tile}). Action taken: {taken}")
    print(f"Player's hand: {hand}")
    print("-" * 50)
    print(f"full_data:\n {full_hand}")
    print("-" * 50)

print("-" * 50)
print("-" * 50)
print("-" * 50)
for round_info in pong_rounds:
    round_idx, player, action, taken, discard_tile, hand, full_hand = round_info
    # print(f"Round {round_idx}: Player {player} can {action} ({discard_tile}). Action taken: {taken}")
    print(f"can {action} ({discard_tile}). Action taken: {taken}")
    print(f"Player's hand: {hand}")
    print("-" * 50)
    print(f"full_data:\n {full_hand}")
    print("-" * 50)

print("-" * 50)
print("-" * 50)
print("-" * 50)
for round_info in kong_rounds:
    round_idx, player, action, taken, discard_tile, hand, full_hand = round_info
    # print(f"Round {round_idx}: Player {player} can {action} ({discard_tile}). Action taken: {taken}")
    print(f"can {action} ({discard_tile}). Action taken: {taken}")
    print(f"Player's hand: {hand}")
    print("-" * 50)
    print(f"full_data:\n {full_hand}")
    print("-" * 50)


