import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
import os




# 定義模型
if 0:
    model = load_model('NN_v1')
else:
    # 載入數據
    folder_path = 'dataset_extracted'

    # 創建一個空的 DataFrame，準備存放所有合併的數據
    all_data = pd.DataFrame()

    dataframes = []

    for file in os.listdir(folder_path):
        if file.endswith('.csv'):
            file_path = os.path.join(folder_path, file)
            data = pd.read_csv(file_path)
            dataframes.append(data)  # 將每個 DataFrame 添加到列表中

    # 一次性合併所有 DataFrame
    all_data = pd.concat(dataframes, ignore_index=True)


    # 資料預處理
    x_train = all_data.iloc[:, 68:102].values  # 使用 iloc 获取特定列的值
    y_train = all_data.iloc[:, -1].values  # 获取最后一列作为标签

    # 将标签转为 One-Hot 编码
    y_train_one_hot = tf.keras.utils.to_categorical(y_train)
    model = Sequential([
        Dense(512, activation='relu', input_shape=(34,)),  # 隱藏層 1
        Dense(256, activation='relu'),                   # 隱藏層 2
        Dense(128, activation='relu'),                   # 隱藏層 2
        Dense(64, activation='relu'),                   # 隱藏層 3
        Dense(34, activation='softmax')                 # 輸出層
    ])



    # 編譯模型
    model.compile(
        optimizer='adam',              # 選擇 Adam 優化器
        loss='categorical_crossentropy', # 適用於多分類問題
        metrics=['accuracy']
    )

    # 訓練模型
    model.fit(
        x_train, y_train_one_hot,
        epochs=50,      # 訓練 20 回合
        batch_size=32,  # 每批數據大小
        validation_split=0.2  # 20% 用於驗證
    )

    model.save('NN_v2')

def filter_prediction(input_tiles, prediction):
    """
    过滤预测结果，确保输出的牌在玩家手牌内。
    
    Args:
        input_tiles (np.array): 玩家手牌 (长度为34的向量)
        prediction (np.array): 模型的输出 (长度为34的概率向量)
    
    Returns:
        int: 经过过滤后的输出牌索引
    """
    legal_tiles = np.where(input_tiles > 0)[0]  # 找到手牌中合法牌的索引
    filtered_prediction = np.zeros_like(prediction)
    filtered_prediction[legal_tiles] = prediction[legal_tiles]
    
    return np.argmax(filtered_prediction)



import numpy as np

def discard(hands_input):
    # 初始化手牌
    hands = np.zeros(34)  # 假设有 34 种牌

    # 根据 hands_input 中的牌来填充 hands 数组
    for tile in hands_input:
        hands[tile['type'] * 9 + tile['index'] - 1] += 1

    # 让模型预测
    hands = hands.reshape(1, 34)  # 使其成为符合模型要求的形状
    out = model.predict(hands)

    # 找到模型预测出的弃牌
    discard_index = np.argmax(out)

    # 找到并返回对应的弃牌
    for i, tile in enumerate(hands_input):
        if tile['type'] * 9 + tile['index'] - 1 == discard_index:
            return i

    

# 測試
hands = [1, 0, 0, 0, 0, 0, 0, 0, 0,  3, 0, 0, 0, 0, 0, 0, 0, 1,  1, 0, 0, 0, 0, 0, 0, 0, 1,  1, 1, 1, 1, 1, 1, 1]
#new =   [0, 0, 0, 0, 0, 0, 0, 0, 0,  1, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0, 0, 0, 0, 0, 0]
new = 9

hands_input = [
    {'dora': False, 'type': 0, 'index': 1},
    {'dora': False, 'type': 0, 'index': 2},
    {'dora': False, 'type': 0, 'index': 3},
    {'dora': False, 'type': 1, 'index': 4},
    {'dora': False, 'type': 1, 'index': 5},
    {'dora': False, 'type': 1, 'index': 6},
    {'dora': False, 'type': 1, 'index': 7},
    {'dora': False, 'type': 1, 'index': 8},
    {'dora': False, 'type': 1, 'index': 9},
    {'dora': False, 'type': 2, 'index': 0},
    {'dora': False, 'type': 3, 'index': 1},
    {'dora': False, 'type': 3, 'index': 2},
    {'dora': False, 'type': 3, 'index': 3},
    {'dora': False, 'type': 3, 'index': 3}
]
print(discard(hands_input))

def action(type, combination, hands):
    #type : chi, pong, kong
    #combination: 23吃4萬 or 24吃3萬

    decision = 0 

    return decision


