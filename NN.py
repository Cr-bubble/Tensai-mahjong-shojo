import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np

# 載入數據
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 資料預處理
x_train = ...
x_test = ...


# 定義模型
model = Sequential([
    Dense(64, activation='relu', input_shape=(34,)),  # 隱藏層 1
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


# 隨機生成範例數據 (用實際數據替代)
N = 1000  # 資料筆數
x_train = np.random.rand(N, 34)  # N x 34 的輸入
y_train = tf.keras.utils.to_categorical(
    np.random.randint(0, 34, size=(N,)), num_classes=34)  # One-hot 編碼輸出

# 訓練模型
model.fit(
    x_train, y_train,
    epochs=50,      # 訓練 20 回合
    batch_size=32,  # 每批數據大小
    validation_split=0.2  # 20% 用於驗證
)

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



def discard(hands_input):
    # 合併手牌與新進牌
    #hands[new] += 1
    hands = [0] * 34
    for tile in hands_input:
        hands[tile.type*9 + tile.index-1] += 1

    out = filter_prediction(hands_input, model.predict(hands))

    for i, tile in enumerate(hands_input):
        if(tile.type*9 + tile.index-1 == out):
            return i
    

# 測試
hands = [1, 0, 0, 0, 0, 0, 0, 0, 0,  2, 0, 0, 0, 0, 0, 0, 0, 1,  1, 0, 0, 0, 0, 0, 0, 0, 1,  1, 1, 1, 1, 1, 1, 1]
#new =   [0, 0, 0, 0, 0, 0, 0, 0, 0,  1, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0, 0, 0, 0, 0, 0]
new = 9
print(discard(hands, new))

def action(type, combination, hands):
    #type : chi, pong, kong
    #combination: 23吃4萬 or 24吃3萬

    decision = 0 

    return decision


