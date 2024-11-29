# 國士無雙所需的牌索引（幺九牌 + 字牌）
kokushi_indices = [0, 8, 9, 17, 18, 26, 27, 28, 29, 30, 31, 32, 33]

def determine(hands, new):
    # 合併手牌與新進牌
    hands[new] += 1

    out = -1 #index of the drawed tile

    #change here to other algorithms
    #-------
    # 檢查是否滿足國士無雙條件
    # needed_tiles = [i for i in kokushi_indices if hands[i] > 0]  # 已有的幺九和字牌
    # num_pairs = sum(hands[i] >= 2 for i in kokushi_indices)  # 檢查有幾個對子

    # if len(needed_tiles) == len(kokushi_indices) and num_pairs >= 1:
    #     return -1 #lon
    # else:
    # 棄掉非國士無雙相關的牌
    drawed = 0
    for i in range(len(hands)):
        if(drawed):
            break
        if i not in kokushi_indices:
            if(hands[i] > 0):
                hands[i] = max(0, hands[i] - 1)
                out = i
                drawed = 1
    
    #棄掉大於3張的國士無雙牌
    if(not drawed):
        for i in kokushi_indices:
            if(drawed):
                break
            if(hands[i] > 2):
                hands[i] = max(0, hands[i] - 1)
                out = i
                drawed = 1

    #棄掉大於2張的國士無雙牌
    if(not drawed):
        for i in kokushi_indices:
            if(drawed):
                break
            if(hands[i] >= 2):
                hands[i] = max(0, hands[i] - 1)
                out = i
                drawed = 1
    #print("棄排後的手牌：", temp_hands)
    #-------

    return out
    

# 測試
hands = [1, 0, 0, 0, 0, 0, 0, 0, 0,  2, 0, 0, 0, 0, 0, 0, 0, 1,  1, 0, 0, 0, 0, 0, 0, 0, 1,  1, 1, 1, 1, 1, 1, 1]
#new =   [0, 0, 0, 0, 0, 0, 0, 0, 0,  1, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0, 0, 0, 0, 0, 0]
new = 9
print(determine(hands, new))
