import threading
import time
import os
import msvcrt
import random as ra


hor = 12
ver = 22


# 오브젝트를 co에 추가하고 해당 오브젝트의 쓰레드를 실행시켜주는 기능
def starter(objects):
    global co
    co.extend(objects)
    for i in range(-len(objects), 0):
        co[i].start()


def location_list_maker(co, list_type):
    c = 1

    if list_type != 7:
        leng = 3
    else:
        leng = 4

    # 처음 블럭들의 상대적인 위치들을 이중 리스트로 모아주는 기능
    location_list = []
    for i in range(leng):
        sub_location_list = []
        for j in range(leng):
            for k in co:
                if k.rl == c and k.group == group:
                    sub_location_list.append(k)
                    break
            else:
                sub_location_list.append(0)
            c += 1
        location_list.append(sub_location_list)

    return location_list


class TetrisBlock:
    def __init__(self, delay):
        global co
        global group
        global latest_shape_type
        global next_num

        self.shape_type = next_num
        self.delay = delay
        group += 1

        # aaa
        #  a
        if self.shape_type == 1:
            starter([Block([4, -1], group, 4, self.shape_type), Block([5, -1], group, 5, self.shape_type),
                     Block([6, -1], group, 6, self.shape_type), Block([5, 0], group, 8, self.shape_type)])
        # a
        # aaa
        elif self.shape_type == 2:
            starter([Block([4, -1], group, 4, self.shape_type), Block([4, 0], group, 7, self.shape_type),
                     Block([5, 0], group, 8, self.shape_type), Block([6, 0], group, 9, self.shape_type)])
        #   a
        # aaa
        elif self.shape_type == 3:
            starter([Block([6, -1], group, 6, self.shape_type), Block([4, 0], group, 7, self.shape_type),
                     Block([5, 0], group, 8, self.shape_type), Block([6, 0], group, 9, self.shape_type)])
        #  aa
        # aa
        elif self.shape_type == 4:
            starter([Block([5, -1], group, 5, self.shape_type), Block([6, -1], group, 6, self.shape_type),
                     Block([4, 0], group, 7, self.shape_type), Block([5, 0], group, 8, self.shape_type)])
        # aa
        #  aa
        elif self.shape_type == 5:
            starter([Block([4, -1], group, 4, self.shape_type), Block([5, -1], group, 5, self.shape_type),
                     Block([5, 0], group, 8, self.shape_type), Block([6, 0], group, 9, self.shape_type)])
        # aa
        # aa
        elif self.shape_type == 6:
            starter([Block([4, -1], group, 4, self.shape_type), Block([5, -1], group, 5, self.shape_type),
                     Block([4, 0], group, 7, self.shape_type), Block([5, 0], group, 8, self.shape_type)])

        # aaaa(4x4칸)
        elif self.shape_type == 7:
            starter([Block([4, 0], group, 9, self.shape_type), Block([5, 0], group, 10, self.shape_type),
                     Block([6, 0], group, 11, self.shape_type), Block([7, 0], group, 12, self.shape_type)])

        latest_shape_type = self.shape_type

        Fall(group, self.delay).start()


class Block(threading.Thread):  # 각 테트리스 블럭을 이루는 작은 블럭
    def __init__(self, coord, block_group, relative_location, shape):
        threading.Thread.__init__(self)
        self.coord = coord
        # □■▤▥▨▧▩▣ ■◇◈▨▧▒▣
        if shape == 1:
            self.shape = "■"
        elif shape == 2:
            self.shape = "◇"
        elif shape == 3:
            self.shape = "◈"
        elif shape == 4:
            self.shape = "▨"
        elif shape == 5:
            self.shape = "▧"
        elif shape == 6:
            self.shape = "▒"
        elif shape == 7:
            self.shape = "▣"

        self.group = block_group  # 어떤 테트리스 블럭 그룹의 일부인지를 알려줌
        self.rl = relative_location  # relative location
        self.is_arrived = False  # 바닥 또는 블럭 위에 도착했는지의 여부


class Fall(threading.Thread):
    def __init__(self, block_group, delay):
        threading.Thread.__init__(self)
        self.group = block_group
        self.is_arrived = False  # 바닥 또는 블럭 위에 도착했는지의 여부
        self.is_stopped = False  # 최종적으로 움직임을 멈췄는지의 여부
        self.delay = delay  # 한 칸 내려올 때마다 멈추는 시간

    def run(self):
        global co
        global is_tetris_block_in_checking
        global is_tetris_block_stopped
        global one_to_seven
        global one_to_seven_iter
        global next_num

        time.sleep(0.5)

        try:
            while True:
                abc = {tuple(i.coord) for i in co if i.group != self.group}  # all blocks' coordinate with other group

                if len({(i.coord[0], i.coord[1] + 1) for i in co if i.group == self.group} &
                       (abc | {(i, ver - 1) for i in range(hor)})) >= 1:
                    self.is_arrived = True

                    if self.is_arrived:
                        is_tetris_block_in_checking = True
                        time.sleep(0.5)

                        if len({(i.coord[0], i.coord[1] + 1) for i in co if i.group == self.group} &
                               (abc | {(i, ver - 1) for i in range(hor)})) >= 1:
                            is_tetris_block_in_checking = False
                            is_tetris_block_stopped = True

                            if is_tetris_block_stopped:
                                try:
                                    next_num = one_to_seven_iter.__next__()
                                except StopIteration:
                                    ra.shuffle(one_to_seven)
                                    one_to_seven_iter = one_to_seven.__iter__()
                                    next_num = one_to_seven_iter.__next__()
                            break
                        else:
                            is_tetris_block_in_checking = False
                            self.is_arrived = False

                # 현재 내려오는 블럭들을 한 칸씩 내려주는 기능
                for i in co:
                    if i.group == self.group:
                        i.coord[1] += 1

                time.sleep(self.delay)
        except:
            pass


def move(input_action):  # 테트리스 블럭을 좌우로 이동시켜주는 기능
    global co
    global group
    global is_tetris_block_stopped
    global is_tetris_block_in_checking
    global latest_shape_type

    is_available = True
    direction = 0

    asb = sum([i.is_arrived for i in co if i.group == group])  # already stopped blocks of same(latest) group

    if asb == 0 or (asb >= 1 and is_tetris_block_in_checking):

        # 테트리스 블럭이 멈춘 경우가 아닌 경우
        if not is_tetris_block_stopped:
            cbsg = [i.coord for i in co if i.group != group]  # coords of blocks of not same(latest) group
            location_list = location_list_maker(co, latest_shape_type)

            # 왼쪽으로 이동하는 것을 원하는 경우
            if input_action == "a":
                for i in location_list:
                    for j in i:
                        if isinstance(j, Block):
                            if [j.coord[0] - 1, j.coord[1]] in cbsg or (
                                    j.coord[0] - 1 <= 0 or j.coord[0] - 1 >= hor - 1):
                                is_available = False
                                break
                        if not is_available:
                            break
            # 오른쪽으로 이동하는 것을 원하는 경우
            elif input_action == "d":
                for i in location_list:
                    for j in i:
                        if isinstance(j, Block):
                            if [j.coord[0] + 1, j.coord[1]] in cbsg or (
                                    j.coord[0] + 1 <= 0 or j.coord[0] + 1 >= hor - 1):
                                is_available = False
                                break
                        if not is_available:
                            break

            # 해당 방향으로 이동하는 것이 가능한 경우
            if is_available:
                if input_action == "a":
                    direction = 1
                elif input_action == "d":
                    direction = 2

            if direction in [1, 2]:
                ibsg = [i for i, j in enumerate(co) if j.group == group]  # indices of blocks of same(latest) group
                for i in ibsg:
                    if direction == 1:
                        co[i].coord[0] -= 1
                    elif direction == 2:
                        co[i].coord[0] += 1


# 현재 내려오고 있는 블럭들을 회전시켜주는 기능
def rotate():
    global co
    global group
    global latest_shape_type

    is_available = True
    cbsg = [i.coord for i in co if i.group != group]  # coords of blocks of not same(latest) group

    location_list = location_list_maker(co, latest_shape_type)

    if 1 <= latest_shape_type <= 5:

        # 테트리스 블럭이 회전을 할 수 있는 상태인지를 검사함
        for i in location_list:
            for j in i:
                if isinstance(j, Block):
                    if j.rl == 1:
                        if [j.coord[0] + 2, j.coord[1]] in cbsg or (j.coord[0] + 2 <= 0 or
                                                                     j.coord[0] + 2 >= hor - 1):
                            is_available = False
                    elif j.rl == 2:
                        if [j.coord[0] + 1, j.coord[1] + 1] in cbsg or (j.coord[0] + 1 <= 0 or
                                                                         j.coord[0] + 1 >= hor - 1 or
                                                                         j.coord[1] + 1 >= ver - 1):
                            is_available = False
                    elif j.rl == 3:
                        if [j.coord[0], j.coord[1] + 2] in cbsg or (j.coord[1] + 2 >= ver - 1):
                            is_available = False
                    elif j.rl == 4:
                        if [j.coord[0] + 1, j.coord[1] - 1] in cbsg or (j.coord[0] + 1 <= 0 or
                                                                         j.coord[0] + 1 >= hor - 1 or
                                                                         j.coord[1] - 1 >= ver - 1):
                            is_available = False
                    elif j.rl == 6:
                        if [j.coord[0] - 1, j.coord[1] + 1] in cbsg or (j.coord[0] - 1 <= 0 or
                                                                         j.coord[0] - 1 >= hor - 1 or
                                                                         j.coord[1] + 1 >= ver - 1):
                            is_available = False
                    elif j.rl == 7:
                        if [j.coord[0], j.coord[1] - 2] in cbsg or (j.coord[1] - 2 >= ver - 1):
                            is_available = False
                    elif j.rl == 8:
                        if [j.coord[0] - 1, j.coord[1] - 1] in cbsg or (j.coord[0] - 1 <= 0 or
                                                                         j.coord[0] - 1 >= hor - 1 or
                                                                         j.coord[1] - 1 >= ver - 1):
                            is_available = False
                    elif j.rl == 9:
                        if [j.coord[0] - 2, j.coord[1]] in cbsg or (j.coord[0] - 2 <= 0 or
                                                                     j.coord[0] - 2 >= ver - 1):
                            is_available = False

        # 회전이 가능한 경우 블럭들을 회전시켜 주는 기능
        if is_available:
            for i in location_list:
                for j in i:
                    if isinstance(j, Block):
                        if j.rl == 1:
                            j.coord[0] += 2
                        elif j.rl == 2:
                            j.coord[0] += 1
                            j.coord[1] += 1
                        elif j.rl == 3:
                            j.coord[1] += 2
                        elif j.rl == 4:
                            j.coord[0] += 1
                            j.coord[1] -= 1
                        elif j.rl == 6:
                            j.coord[0] -= 1
                            j.coord[1] += 1
                        elif j.rl == 7:
                            j.coord[1] -= 2
                        elif j.rl == 8:
                            j.coord[0] -= 1
                            j.coord[1] -= 1
                        elif j.rl == 9:
                            j.coord[0] -= 2

            # 블럭 위치가 바뀐 것을 location_list에 반영함
            location_list = [[i[0] for i in location_list][::-1], [i[1] for i in location_list][::-1],
                             [i[2] for i in location_list][::-1]]

            # 상대적 위치의 초기화
            c = 1
            for i in range(3):
                for j in range(3):
                    if isinstance(location_list[i][j], Block):
                        location_list[i][j].rl = c
                    c += 1
    elif latest_shape_type == 7:

        # 테트리스 블럭이 회전을 할 수 있는 상태인지를 검사함
        for i in location_list:
            for j in i:
                if isinstance(j, Block):
                    if j.rl == 2:
                        if [j.coord[0] + 2, j.coord[1]] in cbsg or (j.coord[0] + 2 <= 0 or
                                                                    j.coord[0] + 2 >= hor - 1 or
                                                                    j.coord[1] + 1 >= ver - 1):
                            is_available = False
                    elif j.rl == 3:
                        if [j.coord[0] + 1, j.coord[1] + 1] in cbsg or (j.coord[0] + 1 <= 0 or
                                                                        j.coord[0] + 1 >= hor - 1 or
                                                                        j.coord[1] + 2 >= ver - 1):
                            is_available = False
                    elif j.rl == 5:
                        if [j.coord[0], j.coord[1] + 2] in cbsg or (j.coord[0] + 2 <= 0 or
                                                                    j.coord[0] + 2 >= hor - 1 or
                                                                    j.coord[1] - 1 >= ver - 1):
                            is_available = False
                    elif j.rl == 6:
                        if [j.coord[0] + 1, j.coord[1] - 1] in cbsg or (j.coord[0] + 1 <= 0 or
                                                                        j.coord[0] + 1 >= hor - 1):
                            is_available = False
                    elif j.rl == 7:
                        if [j.coord[0] - 1, j.coord[1] + 1] in cbsg or (j.coord[1] + 1 >= ver - 1):
                            is_available = False
                    elif j.rl == 8:
                        if [j.coord[0], j.coord[1] - 2] in cbsg or (j.coord[0] - 1 <= 0 or
                                                                    j.coord[0] - 1 >= hor - 1 or
                                                                    j.coord[1] + 2 >= ver - 1):
                            is_available = False
                    elif j.rl == 9:
                        if [j.coord[0] - 1, j.coord[1] - 1] in cbsg or (j.coord[0] + 1 <= 0 or
                                                                        j.coord[0] + 1 >= hor - 1 or
                                                                        j.coord[1] - 2 >= ver - 1):
                            is_available = False
                    elif j.rl == 10:
                        if [j.coord[0] - 2, j.coord[1]] in cbsg or (j.coord[1] - 1 >= ver - 1):
                            is_available = False
                    elif j.rl == 11:
                        if [j.coord[0] - 1, j.coord[1] + 1] in cbsg or (j.coord[0] - 1 <= 0 or
                                                                        j.coord[0] - 1 >= hor - 1):
                            is_available = False
                    elif j.rl == 12:
                        if [j.coord[0], j.coord[1] - 2] in cbsg or (j.coord[0] - 2 <= 0 or
                                                                    j.coord[0] - 2 >= hor - 1 or
                                                                    j.coord[1] + 1 >= ver - 1):
                            is_available = False
                    elif j.rl == 14:
                        if [j.coord[0] - 1, j.coord[1] - 1] in cbsg or (j.coord[0] - 1 <= 0 or
                                                                        j.coord[0] - 1 >= hor - 1 or
                                                                        j.coord[1] - 2 >= ver - 1):
                            is_available = False
                    elif j.rl == 15:
                        if [j.coord[0] - 1, j.coord[1] - 1] in cbsg or (j.coord[0] - 2 <= 0 or
                                                                        j.coord[0] - 2 >= hor - 1 or
                                                                        j.coord[1] - 1 >= ver - 1):
                            is_available = False

        # 회전이 가능한 경우 블럭들을 회전시켜 주는 기능
        if is_available:
            for i in location_list:
                for j in i:
                    if isinstance(j, Block):
                        if j.rl == 2:
                            j.coord[0] += 2
                            j.coord[1] += 1
                        elif j.rl == 3:
                            j.coord[0] += 1
                            j.coord[1] += 2
                        elif j.rl == 5:
                            j.coord[0] += 2
                            j.coord[1] -= 1
                        elif j.rl == 6:
                            j.coord[0] += 1
                        elif j.rl == 7:
                            j.coord[1] += 1
                        elif j.rl == 8:
                            j.coord[0] -= 1
                            j.coord[1] += 2
                        elif j.rl == 9:
                            j.coord[0] += 1
                            j.coord[1] -= 2
                        elif j.rl == 10:
                            j.coord[1] -= 1
                        elif j.rl == 11:
                            j.coord[0] -= 1
                        elif j.rl == 12:
                            j.coord[0] -= 2
                            j.coord[1] += 1
                        elif j.rl == 14:
                            j.coord[0] -= 1
                            j.coord[1] -= 2
                        elif j.rl == 15:
                            j.coord[0] -= 2
                            j.coord[1] -= 1

            # 블럭 위치가 바뀐 것을 location_list에 반영함
            location_list = [[i[0] for i in location_list][::-1], [i[1] for i in location_list][::-1],
                             [i[2] for i in location_list][::-1], [i[3] for i in location_list][::-1]]

            # 상대적 위치의 초기화
            c = 1
            for i in range(4):
                for j in range(4):
                    if isinstance(location_list[i][j], Block):
                        location_list[i][j].rl = c
                    c += 1


def show(co, stage):  # 현재 판 상황 출력 위한 함수
    print("{0}".format("\n" * 3))
    print("{0:20s} Stage: {1} {0:9s} {2:>3d}".format(" ", int(stage), score))

    for j in range(0, ver):

        print("{0:20s}".format(""), end="")
        for i in range(0, hor):
            for k in co:
                if ([i, j] == k.coord) and (i not in [0, hor - 1]) and (j not in [0, ver - 1]):
                    print(k.shape, end="")
                    break
            else:
                if i == 0 and j == 0:
                    print("┌", end="")
                elif i == hor - 1 and j == 0:
                    print("┐", end="")
                elif i == 0 and j == ver - 1:
                    print("└", end="")
                elif i == hor - 1 and j == ver - 1:
                    print("┘", end="")
                elif i == 0 or i == hor - 1:
                    print("│", end="")
                elif j == 0 or j == ver - 1:
                    print("─", end="")
                else:
                    print("  ", end="")

        print()


def get_input(val):  # 거의 실시간으로 유저로부터 인풋을 받음
    global action
    global is_input_new

    while True:
        time.sleep(0.06)
        if msvcrt.kbhit():  # 유저가 키를 입력한 경우
            input_action = msvcrt.getch().decode("utf-8").lower()  # 엔터를 누르지 않아도 해당 값을 바로 input_action 이라는 변수에 할당함
            if input_action in ["a", "d", " "]:
                action = input_action
                is_input_new = True
        else:
            action = 0


def scored_checker(val):
    global co
    global is_tetris_block_in_checking
    global group
    global score

    while True:
        time.sleep(0.06)
        abc = [i.coord for i in co if i.group < group]  # all blocks' coordinate with not latest group

        # 테트리스 블럭이 최종 도착지를 검사하는 상태가 아닌 경우
        if not is_tetris_block_in_checking:
            for j in range(1, ver - 1):
                counter = 0
                for i in range(1, hor - 1):
                    if [i, j] in abc:
                        counter += 1
                if counter == 10:
                    scored_y_coord = j
                    break
            else:
                scored_y_coord = 0
        else:
            scored_y_coord = 0

        # 스코어가 난 경우 행의 블럭들을 모두 없애주는 기능
        if scored_y_coord != 0:
            ibd = []  # indices for blocks for deleting

            for index, j in enumerate(co):
                if j.coord[1] == scored_y_coord:
                    ibd.append(index)
            ibd.sort(reverse=True)

            # 필요 없어진 객체들(점수가 난 행의 블럭들)을 제거해 줌
            for i in ibd:
                del co[i]

            score += 10

            # 점수가 난 블럭들이 없어짐에 따라 아래로 한 칸 내려오게 될 블럭들의 인덱스, ibf: indices ofblocks for falling
            ibf = [i for i, j in enumerate(co) if j.group < group and j.coord[1] < scored_y_coord]
            for i in ibf:
                co[i].coord[1] += 1


def game_over_checker(val):
    global co
    global is_tetris_block_in_checking
    global group
    global is_game_over

    while True:
        time.sleep(0.06)
        abc = {tuple(i.coord) for i in co if i.group < group}  # all blocks' coordinate with not latest group

        if len(abc & {(i, 0) for i in range(hor)}):
            is_game_over = True
            break


def clear():
    global co
    global stage
    global score
    global group
    global is_tetris_block_in_checking
    global is_tetris_block_stopped

    is_tetris_block_in_checking = False
    stage += 1
    group += 1
    score = 0

    len_co = len(co)

    # 모든 블럭을 삭제해 줌
    for i in range(len_co - 1, -1, -1):
        del co[i]

    is_tetris_block_stopped = True


if __name__ == "__main__":
    co = list()
    input_thread = threading.Thread(target=get_input, args=(1,))
    score_checker_thread = threading.Thread(target=scored_checker, args=(1,))
    game_over_checker_thread = threading.Thread(target=game_over_checker, args=(1,))
    sleep_time = 0.1
    count = 0
    stage = 1
    action = 0
    is_input_new = False
    score = 40  # 점수
    latest_shape_type = 0  # 가장 최근에 내려보낸 테트리스 블럭의 모양의 종류
    group = 0
    is_tetris_block_stopped = True
    is_tetris_block_in_checking = False
    one_to_seven = list(range(1, 8))
    ra.shuffle(one_to_seven)
    one_to_seven_iter = one_to_seven.__iter__()
    next_num = one_to_seven_iter.__next__()
    is_game_over = False

    while True:
        os.system("cls")

        show(co, stage)  # 현재 게임 판의 상황을 보여줌

        if is_game_over:
            print("게임 오버 되었습니다!")
            break

        if stage == 9:
            print("게임에서 승리하셨습니다!!!")
            break

        print("이동: (a: 왼쪽, d: 오른쪽), 회전: space 키")

        # print("count:", count, "stage:", stage, "location list:", location_list)


        # print(stage, len(co)) # 디버깅용 print()
        time.sleep(sleep_time)

        if count == 0:  # 처음 인풋을 받기 시작하는 경우
            input_thread.start()
            score_checker_thread.start()
            game_over_checker_thread.start()

        if is_input_new:  # 액션을 새로 입력받은 경우
            if action in ["a", "d"]:  # 테트리스 블럭을 이동하는 경우
                move(action)
                is_input_new = False
            elif action == " ":  # 유저가 테트리스 블럭을 회전하는 경우
                rotate()

        if stage == 1:
            if is_tetris_block_stopped:
                TetrisBlock(0.3)
                is_tetris_block_stopped = False
            if score >= 50:
                clear()
        elif stage == 2:
            if is_tetris_block_stopped:
                TetrisBlock(0.25)
                is_tetris_block_stopped = False
            if score >= 50:
                clear()
        elif stage == 3:
            if is_tetris_block_stopped:
                TetrisBlock(0.2)
                is_tetris_block_stopped = False
            if score >= 50:
                clear()
        elif stage == 4:
            if is_tetris_block_stopped:
                TetrisBlock(0.15)
                is_tetris_block_stopped = False
            if score >= 50:
                clear()
        elif stage == 5:
            if is_tetris_block_stopped:
                TetrisBlock(0.1)
                is_tetris_block_stopped = False
            if score >= 50:
                clear()
        elif stage == 6:
            if is_tetris_block_stopped:
                TetrisBlock(0.075)
                is_tetris_block_stopped = False
            if score >= 50:
                clear()
        elif stage == 7:
            if is_tetris_block_stopped:
                TetrisBlock(0.05)
                is_tetris_block_stopped = False
            if score >= 50:
                clear()
        elif stage == 8:
            if is_tetris_block_stopped:
                TetrisBlock(0.03)
                is_tetris_block_stopped = False
            if score >= 50:
                clear()


        count += 1

