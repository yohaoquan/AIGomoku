from graphics import *

GRID_WIDTH = 40

COLUMN_COUNT = 15
ROW_COUNT = 15

pruneCount = 0  # count of pruned subtrees during negativeMax()
search_count = 0   # possible movement searched

aiSteps = []  # list of stones of AI
playerSteps = []  # list of stones of Player
allSteps = []  # all stones on the board

allPointsOnBoard = []  # all possible points on board
next_point = [0, 0]  # AI's next move

ratio = 1  # Aggressiveness, 0 < ratio < 2. The bigger the more aggressive
DEPTH = 2  # heuristic search depth. 2 is enough for demonstration proposes.

# Scores for different shapes achieved on the board
shape_score = [(20, (0, 0, 1, 0, 0, 0)),
               (20, (0, 0, 0, 1, 0, 0)),
               (120, (0, 1, 0, 1, 0, 0)),
               (120, (0, 0, 1, 0, 1, 0)),
               (120, (0, 0, 1, 1, 0, 0)),
               (720, (1, 1, 1, 0, 1)),
               (720, (1, 0, 1, 1, 1)),
               (720, (1, 1, 0, 1, 1)),
               (720, (0, 1, 1, 1, 1)),
               (720, (1, 1, 1, 1, 0)),
               (720, (0, 1, 0, 1, 1, 0)),
               (720, (0, 1, 1, 0, 1, 0)),
               (720, (0, 0, 1, 1, 1, 0)),
               (720, (0, 1, 1, 1, 0, 0)),
               (4320, (0, 1, 1, 1, 1, 0)),
               (50000, (1, 1, 1, 1, 1))]


def ai():
    global pruneCount
    pruneCount = 0
    global search_count
    search_count = 0
    negative_max(True, DEPTH, -99999999, 99999999)
    print("Pruned: " + str(pruneCount))
    print("Searched: " + str(search_count) + " possible movements.")
    return next_point[0], next_point[1]


# Search
def negative_max(is_ai, depth, alpha, beta):
    # base case: actually checking the score when the depth is 0 and when one side is winning under current movement.
    if game_win(aiSteps) or game_win(playerSteps) or depth == 0:
        return evaluation(is_ai)

    blank_list = list(set(allPointsOnBoard).difference(set(allSteps)))  # getting all empty points on the board.
    order(blank_list)   # reorder the list of searching to maximize the performance.
    # loop through all possible points of movement
    for next_step in blank_list:

        global search_count
        search_count += 1

        # skip if no stones is placed nearby.
        if not has_neighbor(next_step):
            continue

        if is_ai:
            aiSteps.append(next_step)
        else:
            playerSteps.append(next_step)
        allSteps.append(next_step)

        value = -negative_max(not is_ai, depth - 1, -beta, -alpha)
        if is_ai:
            aiSteps.remove(next_step)
        else:
            playerSteps.remove(next_step)
        allSteps.remove(next_step)

        if value > alpha:

            print(str(value) + "alpha:" + str(alpha) + "beta:" + str(beta))
            print(allSteps)
            if depth == DEPTH:
                next_point[0] = next_step[0]
                next_point[1] = next_step[1]
            # alpha + beta pruning point
            if value >= beta:
                global pruneCount
                pruneCount += 1
                return beta
            alpha = value

    return alpha


# from experience, points that are close to Player's last step have highest possibilities of being the best step for AI.
def order(blank_list):
    last_pt = allSteps[-1]
    for _ in blank_list:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if (last_pt[0] + i, last_pt[1] + j) in blank_list:
                    blank_list.remove((last_pt[0] + i, last_pt[1] + j))
                    blank_list.insert(0, (last_pt[0] + i, last_pt[1] + j))


def has_neighbor(point):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if (point[0] + i, point[1]+j) in allSteps:
                return True
    return False


# evaluation
def evaluation(is_ai):

    if is_ai:
        my_list = aiSteps
        enemy_list = playerSteps
    else:
        my_list = playerSteps
        enemy_list = aiSteps

    # evaluating scores if AI
    score_all_arr = []
    my_score = 0
    for pt in my_list:
        m = pt[0]
        n = pt[1]
        my_score += cal_score(m, n, 0, 1, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, 1, 0, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, 1, 1, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, -1, 1, enemy_list, my_list, score_all_arr)

    #  算敌人的得分， 并减去
    score_all_arr_player = []
    enemy_score = 0
    for pt in enemy_list:
        m = pt[0]
        n = pt[1]
        enemy_score += cal_score(m, n, 0, 1, my_list, enemy_list, score_all_arr_player)
        enemy_score += cal_score(m, n, 1, 0, my_list, enemy_list, score_all_arr_player)
        enemy_score += cal_score(m, n, 1, 1, my_list, enemy_list, score_all_arr_player)
        enemy_score += cal_score(m, n, -1, 1, my_list, enemy_list, score_all_arr_player)

    total_score = my_score - enemy_score*ratio*0.1

    return total_score


# evaluating on provided direction.
def cal_score(m, n, x_direction, y_direction, enemy_list, my_list, score_all_arr):
    add_score = 0  # additional score
    # only the highest score on each direction is recorded
    max_score_shape = (0, None)

    # if a shape is already discovered before on this direction, skip
    for item in score_all_arr:
        for pt in item[1]:
            if m == pt[0] and n == pt[1] and x_direction == item[2][0] and y_direction == item[2][1]:
                return 0

    # loop through left and right of the  move
    for offset in range(-5, 1):
        positions = []
        for i in range(0, 6):
            if (m + (i + offset) * x_direction, n + (i + offset) * y_direction) in enemy_list:
                positions.append(2)
            elif (m + (i + offset) * x_direction, n + (i + offset) * y_direction) in my_list:
                positions.append(1)
            else:
                positions.append(0)
        tmp_shape5 = (positions[0], positions[1], positions[2], positions[3], positions[4])
        tmp_shape6 = (positions[0], positions[1], positions[2], positions[3], positions[4], positions[5])

        for (score, shape) in shape_score:
            if tmp_shape5 == shape or tmp_shape6 == shape:
                if score > max_score_shape[0]:
                    max_score_shape = (score, ((m + (0+offset) * x_direction, n + (0 + offset) * y_direction),
                                               (m + (1+offset) * x_direction, n + (1 + offset) * y_direction),
                                               (m + (2+offset) * x_direction, n + (2 + offset) * y_direction),
                                               (m + (3+offset) * x_direction, n + (3 + offset) * y_direction),
                                               (m + (4+offset) * x_direction, n + (4 + offset) * y_direction)), (x_direction, y_direction))

    # if two shapes each on different directions can be made, add them up.
    if max_score_shape[1] is not None:
        for item in score_all_arr:
            for pt1 in item[1]:
                for pt2 in max_score_shape[1]:
                    if pt1 == pt2 and max_score_shape[0] > 10 and item[0] > 10:
                        add_score += item[0] + max_score_shape[0]

        score_all_arr.append(max_score_shape)

    return add_score + max_score_shape[0]


def game_win(steps):
    for m in range(COLUMN_COUNT):
        for n in range(ROW_COUNT):

            if n < ROW_COUNT - 4 and (m, n) in steps and (m, n + 1) in steps and (m, n + 2) in steps and (
                    m, n + 3) in steps and (m, n + 4) in steps:
                return True
            elif m < ROW_COUNT - 4 and (m, n) in steps and (m + 1, n) in steps and (m + 2, n) in steps and (
                        m + 3, n) in steps and (m + 4, n) in steps:
                return True
            elif m < ROW_COUNT - 4 and n < ROW_COUNT - 4 and (m, n) in steps and (m + 1, n + 1) in steps and (
                        m + 2, n + 2) in steps and (m + 3, n + 3) in steps and (m + 4, n + 4) in steps:
                return True
            elif m < ROW_COUNT - 4 and n > 3 and (m, n) in steps and (m + 1, n - 1) in steps and (
                        m + 2, n - 2) in steps and (m + 3, n - 3) in steps and (m + 4, n - 4) in steps:
                return True
    return False


def gomokuWindow():
    window = GraphWin("AI Gomoku", GRID_WIDTH * COLUMN_COUNT, GRID_WIDTH * ROW_COUNT)
    window.setBackground("white")
    i1 = 0

    while i1 <= GRID_WIDTH * COLUMN_COUNT:
        l = Line(Point(i1, 0), Point(i1, GRID_WIDTH * COLUMN_COUNT))
        l.draw(window)
        i1 = i1 + GRID_WIDTH
    i2 = 0

    while i2 <= GRID_WIDTH * ROW_COUNT:
        l = Line(Point(0, i2), Point(GRID_WIDTH * ROW_COUNT, i2))
        l.draw(window)
        i2 = i2 + GRID_WIDTH
    return window


if __name__ == '__main__':

    win = gomokuWindow()

    for i in range(COLUMN_COUNT + 1):
        for j in range(ROW_COUNT + 1):
            allPointsOnBoard.append((i, j))

    change = 0
    g = 0
    m = 0
    n = 0

    lastPiece = None
    while g == 0:
        if change % 2 == 1:
            if lastPiece is not None:
                lastPiece.setFill('white')
            pos = ai()
            if pos in allSteps:
                message = Text(Point(200, 200), "Spot unavailable." + str(pos[0]) + "," + str(pos[1]))
                message.draw(win)
                g = 1

            aiSteps.append(pos)
            allSteps.append(pos)

            piece = Circle(Point(GRID_WIDTH * pos[0], GRID_WIDTH * pos[1]), 16)
            piece.setFill('yellow')
            lastPiece = piece
            piece.draw(win)

            if game_win(aiSteps):
                message = Text(Point(200, 200), "AI win.")
                message.draw(win)
                g = 1
            change = change + 1

        else:
            p2 = win.getMouse()
            if not ((round((p2.getX()) / GRID_WIDTH), round((p2.getY()) / GRID_WIDTH)) in allSteps):

                a2 = round((p2.getX()) / GRID_WIDTH)
                b2 = round((p2.getY()) / GRID_WIDTH)
                playerSteps.append((a2, b2))
                allSteps.append((a2, b2))

                piece = Circle(Point(GRID_WIDTH * a2, GRID_WIDTH * b2), 16)
                piece.setFill('black')
                piece.draw(win)
                if game_win(playerSteps):
                    message = Text(Point(200, 200), "User win.")
                    message.draw(win)
                    g = 1

                change = change + 1

    message = Text(Point(200, 120), "Click anywhere to quit.")
    message.draw(win)
    win.getMouse()
    win.close()

