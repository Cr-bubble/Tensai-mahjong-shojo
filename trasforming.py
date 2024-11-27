import pandas as pd
import numpy as np

# 載入數據
csv_path = 'processed_mahjong_data.csv'
data = pd.read_csv(csv_path)

# 選取需要的行數據
row_index = 5
row_data = data.iloc[row_index, :-1].values

# 重塑為 15x34 格式
reshaped_data = row_data.reshape(15, 34)
index_labels = [
    "Dora indicators",
    "POV hand",
    "P0 melds",
    "P1 melds",
    "P2 melds",
    "P3 melds",
    "P0 pool",
    "P1 pool",
    "P2 pool",
    "P3 pool",
    "P0 discards",
    "P1 discards",
    "P2 discards",
    "P3 discards"
]
# 第一份資料 - 第一行索引
first_row_labels = [
    "Round wind", "Dealer", "POV player", "Riichi sticks", "Honba sticks", "Wall tiles",
    "P0 score", "P1 score", "P2 score", "P3 score", "P0 riichi", "P1 riichi", "P2 riichi", "P3 riichi",
    *["Padding"] * 18,
    "Round Number", "Step Number"
]
first_row_df = pd.DataFrame([reshaped_data[0]],columns=first_row_labels)

# 第二份資料 - 剩餘行索引
remaining_rows_labels = [
    "1 man", "2 man", "3 man", "4 man", "5 man", "6 man", "7 man", "8 man", "9 man",
    "1 pin", "2 pin", "3 pin", "4 pin", "5 pin", "6 pin", "7 pin", "8 pin", "9 pin",
    "1 sou", "2 sou", "3 sou", "4 sou", "5 sou", "6 sou", "7 sou", "8 sou", "9 sou",
    "East", "South", "West", "North", "Haku", "Hatsu", "Chun"
]
remaining_rows_df = pd.DataFrame(reshaped_data[1:],index=index_labels, columns=remaining_rows_labels)


print(first_row_df)
print(remaining_rows_df)
