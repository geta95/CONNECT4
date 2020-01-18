# connect4

## アメリカの有名なおもちゃ
## 6x7マスで先に4マス並べたら勝ち
## 重力付き（マスは下から順に埋まっていく）
## CPUと対戦

import random
import numpy as np

# 行列の要素数
ROW_COUNT = 6
COLUMN_COUNT = 7

# オブジェクトの形の定義
OBJECT = {0: '●', 1: '×'}
PLAYER = {0: 'YOU', 1: 'CPU'}
EMPTY = '　'

# 経過ターン数の計測
TURN = 1

def get_key_from_value(d, val):
    # ValueからKeyを取り出す関数
    return [k for k, v in d.items() if v == val][0]

def decide_order():
    # 先行・後攻の決定：コイントス
    print('コイントスで先行・後攻を決定します。')
    print('表：' + PLAYER[0] + '、裏：' + PLAYER[1] + 'が先行になります。')
    print('ENTERキーを押してください。')
    ENTER = input()
    order = random.randint(0, 1)
    global the_turn
    if order == 0:
        print('表が出ました。先行は' + PLAYER[0] + 'です。')
        the_turn = PLAYER[0]
    else:
        print('裏が出ました。先行は' + PLAYER[1] + 'です。')
        the_turn = PLAYER[1]
    ENTER = input()

def output_field(board):
    # ボードをコマンドライン上に表示
    print('')
    print('+----' * COLUMN_COUNT + '+')
    print('| ' + '  | '.join([str(i) for i in range(1, COLUMN_COUNT + 1)]) + '  |')
    print('+----' * COLUMN_COUNT + '+')
    for r in range(ROW_COUNT):
        print('| ' + ' | '.join([str(board[r][c]) for c in range(COLUMN_COUNT)]) + ' |')

# プレイヤーの設定
def update_board(turn, board):
    # 列の選択後、空きを確認しボードを更新
    while True:
        print(turn + 'さん、1～' + str(COLUMN_COUNT) + '列の中から選択してください。')
        try:
            number = int(input())
        except ValueError:
            print('')
            print('数字を入力してください。')
            continue
        if (number == 0) or (number > COLUMN_COUNT):
            print('')
            print('Error: 1～' + str(COLUMN_COUNT) + 'までの数字を入力してください。')
            continue
        if board[0][number - 1] != EMPTY:
            print('')
            print('その列は選択できません。')
            continue
        for r in range(ROW_COUNT - 1, -1 ,-1):
            point = board[r][number - 1]
            if point == EMPTY:
                board[r][number - 1] = OBJECT[get_key_from_value(PLAYER, turn)]
                break
        break

# CPUの設定
## 基本的にはランダムに打つ
def cpu_choose_number():
    number = random.randint(1, COLUMN_COUNT)
    return number

def cpu_update_board(turn, board):
    # 列の選択後、空きを確認しボードを更新
    while True:
        if cpu_loose_condition1(board):
            number = the_number
            for r in range(ROW_COUNT - 1, -1 ,-1):
                point = board[r][number - 1]
                if point == EMPTY:
                    board[r][number - 1] = OBJECT[get_key_from_value(PLAYER, turn)]
                    break
            break


        elif cpu_loose_condition2(board):
            number = the_number
            for r in range(ROW_COUNT - 1, -1 ,-1):
                point = board[r][number - 1]
                if point == EMPTY:
                    board[r][number - 1] = OBJECT[get_key_from_value(PLAYER, turn)]
                    break
            break

        else:
            number = cpu_choose_number()
            if board[0][number - 1] != EMPTY:
                continue
            for r in range(ROW_COUNT - 1, -1 ,-1):
                point = board[r][number - 1]
                if point == EMPTY:
                    board[r][number - 1] = OBJECT[get_key_from_value(PLAYER, turn)]
                    break
            break

## 負けパターンを阻止する手は上に優先して打つ
def cpu_loose_condition1(board):
    global the_number
    # 2つ並んでおりかつその両隣及び更に両隣が開いている場合
    while True:
    ## 横方向のリーチ判定
        for r in range(ROW_COUNT):
            if r == ROW_COUNT - 1:
                if (board[r][1] == board[r][2] == OBJECT[0]) and (board[r][0] == board[r][3] == board[r][4] == EMPTY):
                    the_number = 4
                    return True
                    break
            elif (board[r][1] == board[r][2] == OBJECT[0]) and (board[r][0] == board[r][3] == board[r][4] == EMPTY) and (board[r + 1][0] != EMPTY) and (board[r + 1][3] != EMPTY) and (board[r + 1][4] != EMPTY):
                the_number = 4
                return True
                break
        for r in range(ROW_COUNT):
            if r == ROW_COUNT - 1:
                if (board[r][COLUMN_COUNT - 2] == board[r][COLUMN_COUNT - 3] == OBJECT[0]) and (board[r][COLUMN_COUNT - 1] == board[r][COLUMN_COUNT - 4] == board[r][COLUMN_COUNT - 5] == EMPTY):
                    the_number = COLUMN_COUNT - 3
                    return True
                    break
            elif (board[r][COLUMN_COUNT - 2] == board[r][COLUMN_COUNT - 3] == OBJECT[0]) and (board[r][COLUMN_COUNT - 1] == board[r][COLUMN_COUNT - 4] == board[r][COLUMN_COUNT - 5] == EMPTY) and (board[r + 1][COLUMN_COUNT - 1] != EMPTY) and (board[r + 1][COLUMN_COUNT - 4] != EMPTY) and (board[r + 1][COLUMN_COUNT - 5] != EMPTY):
                the_number = COLUMN_COUNT - 3
                return True
                break
        for c in range(2, COLUMN_COUNT - 2):
            for r in range(ROW_COUNT):
                if r == ROW_COUNT - 1:
                    if (board[r][c] == board[r][c + 1] == OBJECT[0]) and (board[r][c - 1] == board[r][c + 2] == EMPTY):
                        if (board[r][c - 2] == EMPTY):
                            the_number = c
                            return True
                            break
                        elif (board[r][c + 3] == EMPTY):
                            the_number = c + 3
                            return True
                            break
                elif (board[r][c] == board[r][c + 1] == OBJECT[0]) and (board[r][c - 1] == board[r][c + 2] == EMPTY) and (board[r + 1][c - 1] != EMPTY) and (board[r + 1][c + 2] != EMPTY):
                    if ((board[r][c - 2] == EMPTY) and (board[r + 1][c - 2] != EMPTY)):
                        the_number = c
                        return True
                        break
                    elif ((board[r][c + 2] == EMPTY) and (board[r + 1][c + 2] != EMPTY)):
                        the_number = c + 3
                        return True
                        break

    ## 縦方向のリーチ判定：必要なし

    ## 順斜め方向のリーチ判定
        for c in range(1, COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT - 1):
                if r == ROW_COUNT - 2:
                    if (board[r][c] == board[r - 1][c + 1] == OBJECT[0]) and (board[r + 1][c - 1] == board[r - 2][c + 2] == board[r - 3][c + 3] == EMPTY) and (board[r - 1][c + 2] != EMPTY) and (board[r - 2][c + 3] != EMPTY):
                        the_number = c + 3
                        return True
                        break
                elif (board[r][c] == board[r - 1][c + 1] == OBJECT[0]) and (board[r + 1][c - 1] == board[r - 2][c + 2] == board[r - 3][c + 3] == EMPTY) and (board[r + 2][c - 1] != EMPTY) and (board[r - 1][c + 2] != EMPTY) and (board[r - 2][c + 3] != EMPTY):
                    the_number = c + 3
                    return True
                    break
        for c in range(2, COLUMN_COUNT - 2):
            for r in range(2, ROW_COUNT - 2):
                if r == ROW_COUNT - 3:
                    if (board[r][c] == board[r - 1][c + 1] == OBJECT[0]) and (board[r + 2][c - 2] == board[r + 1][c - 1] == board[r - 2][c + 2] == EMPTY) and (board[r + 2][c - 1] != EMPTY) and (board[r - 1][c + 2] != EMPTY):
                        the_number = c
                        return True
                        break
                elif (board[r][c] == board[r - 1][c + 1] == OBJECT[0]) and (board[r + 2][c - 2] == board[r + 1][c - 1] == board[r - 2][c + 2] == EMPTY) and (board[r + 3][c - 2] != EMPTY) and (board[r + 2][c - 1] != EMPTY) and (board[r - 1][c + 2] != EMPTY):
                    the_number = c
                    return True
                    break

    ## 逆斜め方向のリーチ判定
        for c in range(1, COLUMN_COUNT - 3):
            for r in range(1, ROW_COUNT - 3):
                if r == ROW_COUNT - 4:
                    if (board[r][c] == board[r + 1][c + 1] == OBJECT[0]) and (board[r - 1][c - 1] == board[r + 2][c + 2] == board[r + 3][c + 3] == EMPTY) and (board[r][c - 1] != EMPTY) and (board[r + 3][c + 2] != EMPTY):
                        the_number = c + 3
                        return True
                        break
                elif (board[r][c] == board[r + 1][c + 1] == OBJECT[0]) and (board[r - 1][c - 1] == board[r + 2][c + 2] == board[r + 3][c + 3] == EMPTY) and (board[r][c - 1] != EMPTY) and (board[r + 3][c + 2] != EMPTY) and (board[r + 4][c + 3] != EMPTY):
                    the_number = c + 3
                    return True
                    break
        for c in range(2, COLUMN_COUNT - 2):
            for r in range(2, ROW_COUNT - 2):
                if r == ROW_COUNT - 3:
                    if (board[r][c] == board[r + 1][c + 1] == OBJECT[0]) and (board[r - 2][c - 2] == board[r - 1][c - 1] == board[r + 2][c + 2] == EMPTY) and (board[r - 1][c - 2] != EMPTY) and (board[r][c - 1] != EMPTY):
                        the_number = c
                        return True
                        break
                elif (board[r][c] == board[r + 1][c + 1] == OBJECT[0]) and (board[r - 2][c - 2] == board[r - 1][c - 1] == board[r + 2][c + 2] == EMPTY) and (board[r - 1][c - 2] != EMPTY) and (board[r][c - 1] != EMPTY) and (board[r + 3][c + 2] != EMPTY):
                    the_number = c
                    return True
                    break

        return None
        break

def cpu_loose_condition2(board):
    global the_number
    # 3つ並んでいる場合（1のスクリーニングのおかげで両隣がEMPTYの状態かつ3つ並んだ状態にはならないので片側だけ考えたらOK）
    ## 横方向のリーチ判定
    while True:
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                # 右側が空いている場合
                if r == ROW_COUNT - 1:
                    if (board[r][c] == board[r][c + 1] == board[r][c + 2] == OBJECT[0]) and (board[r][c + 3] == EMPTY):
                        the_number = c + 4
                        return True
                        break
                elif (board[r][c] == board[r][c + 1] == board[r][c + 2] == OBJECT[0]) and (board[r][c + 3] == EMPTY) and (board[r + 1][c + 3] != EMPTY):
                    the_number = c + 4
                    return True
                    break
        for c in range(1, COLUMN_COUNT - 2):
            for r in range(ROW_COUNT):
                # 左側が空いている場合
                if r == ROW_COUNT - 1:
                    if (board[r][c] == board[r][c + 1] == board[r][c + 2] == OBJECT[0]) and (board[r][c - 1] == EMPTY):
                        the_number = c
                        return True
                        break
                elif (board[r][c] == board[r][c + 1] == board[r][c + 2] == OBJECT[0]) and (board[r][c - 1] == EMPTY) and (board[r + 1][c - 1] != EMPTY):
                    the_number = c
                    return True
                    break

        ## 縦方向のリーチ判定
        for c in range(COLUMN_COUNT):
            for r in range(1, ROW_COUNT - 2):
                if (board[r][c] == board[r + 1][c] == board[r + 2][c] == OBJECT[0]) and (board[r - 1][c] == EMPTY):
                    the_number = c + 1
                    return True
                    break

        ## 順斜め方向のリーチ判定
        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                # 右側が空いている場合
                if (board[r][c] == board[r - 1][c + 1] == board[r - 2][c + 2] == OBJECT[0]) and (board[r - 3][c + 3] == EMPTY) and (board[r - 2][c + 3] != EMPTY):
                    the_number = c + 4
                    return True
                    break
        for c in range(1, COLUMN_COUNT - 2):
            for r in range(2, ROW_COUNT - 1):
                # 左側が空いている場合
                if r == ROW_COUNT - 2:
                    if (board[r][c] == board[r - 1][c + 1] == board[r - 2][c + 2] == OBJECT[0]) and (board[r + 1][c - 1] == EMPTY):
                        the_number = c
                        return True
                        break
                elif (board[r][c] == board[r - 1][c + 1] == board[r - 2][c + 2] == OBJECT[0]) and (board[r + 1][c - 1] == EMPTY) and (board[r + 2][c - 1] != EMPTY):
                    the_number = c
                    return True
                    break

        ## 逆斜め方向のリーチ判定
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                # 右側が空いている場合
                if r == ROW_COUNT - 4:
                    if (board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] == OBJECT[0]) and (board[r + 3][c + 3] == EMPTY):
                        the_number = c + 4
                        return True
                        break
                elif (board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] == OBJECT[0]) and (board[r + 3][c + 3] == EMPTY) and (board[r + 4][c + 3] != EMPTY):
                    the_number = c + 4
                    return True
                    break
        for c in range(1, COLUMN_COUNT - 2):
            for r in range(1, ROW_COUNT - 2):
                # 左側が空いている場合
                if (board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] == OBJECT[0]) and (board[r - 1][c - 1] == EMPTY) and (board[r][c - 1] != EMPTY):
                    the_number = c
                    return True
                    break

        return None
        break

def change_order():
    # ターンの変更
    global the_turn
    if the_turn == PLAYER[0]:
        the_turn = PLAYER[1]
    else:
        the_turn = PLAYER[0]

# 勝利判定
def victory_condition(turn, board):
    # 横方向の勝利判定
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == OBJECT[get_key_from_value(PLAYER, turn)] and board[r][c + 1] == OBJECT[get_key_from_value(PLAYER, turn)] and board[r][c + 2] == OBJECT[get_key_from_value(PLAYER, turn)] and board[r][c + 3] == OBJECT[get_key_from_value(PLAYER, turn)]:
                return True

    # 縦方向の勝利判定
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == OBJECT[get_key_from_value(PLAYER, turn)] and board[r + 1][c] == OBJECT[get_key_from_value(PLAYER, turn)] and board[r + 2][c] == OBJECT[get_key_from_value(PLAYER, turn)] and board[r + 3][c] == OBJECT[get_key_from_value(PLAYER, turn)]:
                return True

    # 順斜め方向の勝利判定
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == OBJECT[get_key_from_value(PLAYER, turn)] and board[r + 1][c + 1] == OBJECT[get_key_from_value(PLAYER, turn)] and board[r + 2][c + 2] == OBJECT[get_key_from_value(PLAYER, turn)] and board[r + 3][c + 3] == OBJECT[get_key_from_value(PLAYER, turn)]:
                return True

    # 逆斜め向の勝利判定
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == OBJECT[get_key_from_value(PLAYER, turn)] and board[r - 1][c + 1] == OBJECT[get_key_from_value(PLAYER, turn)] and board[r - 2][c + 2] == OBJECT[get_key_from_value(PLAYER, turn)] and board[r - 3][c + 3] == OBJECT[get_key_from_value(PLAYER, turn)]:
                return True

# ゲーム開始
# 新しいボードの定義
new_board = np.full((ROW_COUNT, COLUMN_COUNT), EMPTY)
# 更新用ボードの定義
the_board = new_board

# Opening
print('')
print('Welcome to CONNECT 4!')
print('')
decide_order()
if the_turn == PLAYER[0]:
    output_field(the_board)

while True:
    if the_turn == PLAYER[0]:
        print('')
        print('＜' + str(TURN) + 'ターン目＞')
        update_board(the_turn, the_board)
        if victory_condition(the_turn, the_board):
            break
        TURN += 1
        change_order()

    elif the_turn == PLAYER[1]:
        print('')
        cpu_update_board(the_turn, the_board)
        output_field(the_board)
        if victory_condition(the_turn, the_board):
            break
        change_order()

# Ending
print('')
output_field(the_board)
print('')
print('ゲーム終了。' + the_turn + 'の勝利！')
print('（総ターン数：' + str(TURN) + 'ターン）')
ENTER = input()
