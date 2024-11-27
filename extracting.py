import numpy as np
from scipy.sparse import csr_matrix
import pandas as pd

# 簡化文件路徑
file_path = '2009022011gm-00a9-0000-d7935c6d.npz'

# 載入 .npz 檔案
data = np.load(file_path)

# 檢查檔案中的鍵值
keys = data.files
print("Keys in the .npz file:", keys)

# 提取必要數據
indices = data['indices']
indptr = data['indptr']
shape = tuple(data['shape'])  # 確保 shape 是元組格式

# 詳細檢查 'format' 的內容
format_data = data['format']
print("Type of 'format':", type(format_data))
print("Content of 'format':", format_data)

# 解碼 'format' (嘗試不同方法)
if isinstance(format_data, np.ndarray):
    if format_data.size == 1:  # 如果是大小為 1 的陣列
        format = format_data.item().decode('utf-8')
    else:
        raise ValueError("Unexpected array structure in 'format'")
elif isinstance(format_data, (bytes, np.bytes_)):  # 如果直接是字節類型
    format = format_data.decode('utf-8')
else:
    raise ValueError("Unsupported data type in 'format'")

print("Decoded format:", format)

# 提取主數據
main_data = data['data']

print("Data format:", format)
print("Shape of the matrix:", shape)

# 檢查是否為 CSR 格式
if format == 'csr':
    # 使用 scipy 重建稀疏矩陣
    sparse_matrix = csr_matrix((main_data, indices, indptr), shape=shape)
    dense_matrix = sparse_matrix.toarray()  # 轉換為密集矩陣
    print("Dense matrix shape:", dense_matrix.shape)

    # 分離輸入 (X) 和輸出 (y)
    X = dense_matrix[:, :-1]  # 前 510 個元素
    y = dense_matrix[:, -1]   # 最後 1 個元素
    print("Input shape:", X.shape)
    print("Output shape:", y.shape)

    # 儲存數據為 CSV 格式
    df = pd.DataFrame(X)
    df['Output'] = y
    csv_path = 'processed_mahjong_data.csv'
    df.to_csv(csv_path, index=False)
    print(f"Processed data saved to {csv_path}")
else:
    print("Unknown format:", format)
