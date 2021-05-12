import threading
import time
import os
import msvcrt
import itertools
import random as ra


hor = 11
ver = 15


def itc(iterable):  # 이터러블 객체의 길이를 확인해주는 함수, itc: iterable counter
    return sum(1 for i in iterable)


class User:
    def __init__(self):
        self.shape = "△"
        self.coord = [5, 12]
        self.direction = 0

    def move(self, direction):
        self.direction = direction

        # w,s,a,d는 각각 상,하,좌,우
        if self.direction == "w" and self.coord[1] != 1:
            self.coord[1] -= 1
        elif self.direction == "s" and self.coord[1] != ver - 2:
            self.coord[1] += 1
        elif self.direction == "a" and self.coord[0] != 1:
            self.coord[0] -= 1
        elif self.direction == "d" and self.coord[0] != hor - 2:
            self.coord[0] += 1


def get_input(val):  # 거의 실시간으로 유저로부터 인풋을 받음
    global action
    global is_input_new

    while True:
        time.sleep(0.06)
        if msvcrt.kbhit():  # 유저가 키를 입력한 경우
            input_action = msvcrt.getch().decode("utf-8").lower()  # 엔터를 누르지 않아도 해당 값을 바로 input_action 이라는 변수에 할당함
            if input_action in ["w", "s", "a", "d"]:
                action = input_action
                is_input_new = True
        else:
            action = 0


class Obstacle():

    # 파이참 권고로 __init__ 메소드 사용함
    def __init__(self):
        self.coord = None


class Arrow(threading.Thread, Obstacle):
    def __init__(self, coord, direction, stage = 10):  # direction의 경우 1: 상, 2: 하, 3: 좌, 4: 우, 5: 좌상, 6: 우상, 7: 좌하, 8: 우하
        threading.Thread.__init__(self)

        if direction == 1:
            self.shape = "↑"
        elif direction == 2:
            self.shape = "↓"
        elif direction == 3:
            self.shape = "←"
        elif direction == 4:
            self.shape = "→"
        elif direction == 5:
            self.shape = "↖"
        elif direction == 6:
            self.shape = "↗"
        elif direction == 7:
            self.shape = "↙"
        elif direction == 8:
            self.shape = "↘"

        self.coord = coord
        self.direction = direction
        self.stage = stage

    def run(self):

        if self.stage == 1:
            time.sleep(0.2)
        else:
            time.sleep(0.3)
        while True:
            if self.direction == 1:
                self.coord[1] -= 1
            elif self.direction == 2:
                self.coord[1] += 1
            elif self.direction == 3:
                self.coord[0] -= 1
            elif self.direction == 4:
                self.coord[0] += 1
            elif self.direction == 5:
                self.coord[0] -= 1
                self.coord[1] -= 1
            elif self.direction == 6:
                self.coord[0] += 1
                self.coord[1] -= 1
            elif self.direction == 7:
                self.coord[0] -= 1
                self.coord[1] += 1
            elif self.direction == 8:
                self.coord[0] += 1
                self.coord[1] += 1

            if self.stage == 1:
                time.sleep(0.2)
            else:
                time.sleep(0.3)
            # 각 화살 방향의 경우에서 판의 경계에 도달한 경우
            if self.direction == 1 and self.coord[1] <= 1:
                self.coord = [hor, ver]
                break
            elif self.direction == 2 and self.coord[1] >= ver - 2:
                self.coord = [hor, ver]
                break
            elif self.direction == 3 and self.coord[0] <= 1:
                self.coord = [hor, ver]
                break
            elif self.direction == 4 and self.coord[0] >= hor - 2:
                self.coord = [hor, ver]
                break
            elif self.direction == 5 and (self.coord[0] <= 1 or self.coord[1] <= 1):
                self.coord = [hor, ver]
                break
            elif self.direction == 6 and (self.coord[0] >= hor - 2 or self.coord[1] <= 1):
                self.coord = [hor, ver]
                break
            elif self.direction == 7 and (self.coord[0] <= 1 or self.coord[1] >= ver - 2):
                self.coord = [hor, ver]
                break
            elif self.direction == 8 and (self.coord[0] >= hor - 2 or self.coord[1] >= ver - 2):
                self.coord = [hor, ver]
                break


class HomingArrow(threading.Thread, Obstacle):  # 적이 발사하는 유도 화살

    def __init__(self, coord, shape):  # shape의 경우 1: ↑, 2: ↓, 3: ←, 4: →
        threading.Thread.__init__(self)

        if shape == 1:
            self.shape = "↑"
        elif shape == 2:
            self.shape = "↓"
        elif shape == 3:
            self.shape = "←"
        elif shape == 4:
            self.shape = "→"
        self.coord = coord

    def run(self):
        global co

        time.sleep(0.7)
        move_count = 0
        while True:
            ud = ((self.coord[0] - co[0].coord[0]) ** 2 + (
                        self.coord[1] - 1 - co[0].coord[1]) ** 2) ** 0.5  # up distance
            dd = ((self.coord[0] - co[0].coord[0]) ** 2 + (
                        self.coord[1] + 1 - co[0].coord[1]) ** 2) ** 0.5  # down distance
            ld = ((self.coord[0] - 1 - co[0].coord[0]) ** 2 + (
                        self.coord[1] - co[0].coord[1]) ** 2) ** 0.5  # left distance
            rd = ((self.coord[0] + 1 - co[0].coord[0]) ** 2 + (
                        self.coord[1] - co[0].coord[1]) ** 2) ** 0.5  # right distance

            if ud == min(ud, dd, ld, rd):  # 위쪽으로 이동하는 것이 최단거리인 경우
                self.shape = "↑"
                self.coord[1] -= 1
            elif dd == min(ud, dd, ld, rd):  # 아래쪽으로 이동하는 것이 최단거리인 경우
                self.shape = "↓"
                self.coord[1] += 1
            elif ld == min(ud, dd, ld, rd):  # 왼쪽으로 이동하는 것이 최단거리인 경우
                self.shape = "←"
                self.coord[0] -= 1
            else:  # 오른쪽으로 이동하는 것이 최단거리인 경우
                self.shape = "→"
                self.coord[0] += 1

            time.sleep(0.7)

            move_count += 1
            if move_count == 12:
                self.coord = [hor, ver]
                break


class ArrowShooter(threading.Thread, Obstacle):
    def __init__(self, coord, direction, shooter_type):  # shape의 경우 1: ■, 2:◆, 3: ★
        threading.Thread.__init__(self)
        self.coord = coord
        self.type = shooter_type
        self.direction = direction

        if self.type == 1:
            self.shape = "■"
        elif self.type == 2:
            self.shape = "◆"
        elif self.type == 3:
            self.shape = "★"

    def run(self):
        time.sleep(1)
        while True:
            if self.direction == 1:
                self.coord[1] -= 1
            elif self.direction == 2:
                self.coord[1] += 1
            elif self.direction == 3:
                self.coord[0] -= 1
            elif self.direction == 4:
                self.coord[0] += 1

            time.sleep(1)
            # 각 슈터 방향의 경우에서 판의 경계에 도달한 경우
            if self.direction == 1 and self.coord[1] <= 1:
                self.coord = [hor, ver]
                break
            elif self.direction == 2 and self.coord[1] >= ver - 2:
                self.coord = [hor, ver]
                break
            elif self.direction == 3 and self.coord[0] <= 1:
                self.coord = [hor, ver]
                break
            elif self.direction == 4 and self.coord[0] >= hor - 2:
                self.coord = [hor, ver]
                break


def spike_wall(x_coord, side):  # 총 27개의 Spike 객체를 생성함, side의 경우 1: 왼쪽 벽의 장애물, 2: 오른쪽 벽의 장애물
    global co

    if side == 1:
        for i in range(x_coord - 8, x_coord + 1):
            for j in range(-2, 1):
                if j == -2:
                    co.extend([Spike([i, j], 1)])
                elif j == -1:
                    co.extend([Spike([i, j], 3)])
                elif j == 0:
                    co.extend([Spike([i, j], 2)])

    elif side == 2:
        for i in range(x_coord, x_coord + 9):
            for j in range(-2, 1):
                if j == -2:
                    co.extend([Spike([i, j], 1)])
                elif j == -1:
                    co.extend([Spike([i, j], 3)])
                elif j == 0:
                    co.extend([Spike([i, j], 2)])


class Spike(threading.Thread, Obstacle):
    def __init__(self, coord, spike_type):
        threading.Thread.__init__(self)
        self.coord = coord

        if spike_type == 1:
            self.shape = "┴"
        elif spike_type == 2:
            self.shape = "┬"
        elif spike_type == 3:
            self.shape = "┼"

    def run(self):
        time.sleep(0.4)

        while True:
            self.coord[1] += 1
            time.sleep(0.4)
            # 가시가 경계에 도달한 경우
            if self.coord[1] == ver - 2:
                self.coord = [hor, ver]
                break


def show(co, stage, rest_time):  # 현재 판 상황 출력 위한 함수

    print("{0}".format("\n"*3))

    if stage < 7:
        print("{0:20s} Stage: {1}          {2}".format(" ", int(stage), rest_time))
    else:
        print("{0:20s} Final Stage       {1}".format(" ", rest_time))

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


co = [User()]   # Current objects
input_thread = threading.Thread(target=get_input, args=(1,))

sleep_time = 0.1
count = 0
stage = 1
action = 0
is_input_new = False
is_game_over = False
rest_time = 30

# None의 경우에는 파이참의 권고를 지키기 위한 변수 선언
s1_1_ori = range(4, 10, 2).__iter__()  # 4, 6, 8, s1_1_ori: stage 1.1의 object range iterable
s1_2_ori = range(9, 0, -2).__iter__()  # 9, 7, 5, 3
s1_3_ori = range(1, 10, 2).__iter__()  # 1, 3, 5, 7, 9
s1_4_ori = range(8, 1, -2).__iter__()  # 8, 6, 4, 2
s3_ori_x = itertools.cycle([7, 3])  # __next__()를 통해서 7과 3을 계속해서 반복해서 반환해주는 제너레이터를 생성함, 후에 x_coord로 이용함
s3_ori = itertools.cycle([1, 2])  # __next__()를 통해서 1과 2를 계속해서 반복해서 반환해주는 제너레이터를 생성함, 후에 side로 이용함
s4_1_ori_y = itertools.cycle([13, 1])  # 후에 y_coord로 이용함
s4_1_ori = itertools.cycle([1, 2])  # 상, 하 방향 후에 arrow_type로 이용함
s4_2_ori_x = itertools.cycle([9, 1])
s4_2_ori = itertools.cycle([3, 4])  # 좌, 우 방향
s4_3_ori_x = itertools.cycle([9, 1])
s4_3_ori = itertools.cycle([5, 8])  # 좌상, 우하 방향
s4_4_ori_x = itertools.cycle([9, 1])
s4_4_ori = itertools.cycle([7, 6])  # 좌하, 우상 방향
s4_5_ori_x = itertools.cycle([1, 9])  # 후에 x_coord로 이용함
s4_5_ori_y = itertools.cycle([13, 1])  # 후에 y_coord로 이용함
s4_5_ori = itertools.cycle([1, 4, 2, 3])  # 상, 우, 하, 좌 방향
s4_6_ori_x = itertools.cycle([1, 1, 9, 9])  # 후에 x_coord로 이용함
s4_6_ori = itertools.cycle([6, 8, 7, 5])
s4_7_ori_x = itertools.cycle([1, 1, 1, 9, 9, 9])  # 후에 x_coord로 이용함
s4_7_ori_y = itertools.cycle([13, 1])  # 후에 y_coord로 이용함
s4_7_ori = itertools.cycle([1, 6, 4, 8, 2, 7, 3, 5])

# for_debug = 0 # 디버깅용 변수

while True:
    os.system("cls")

    if count % int(1 / sleep_time) == 0:
        rest_time -= 1

    show(co, stage, rest_time)  # 현재 게임 판의 상황을 보여줌
    print("\n이동: (w: 위, s: 아래, a: 왼쪽, d: 오른쪽)")

    if stage == 8:
        print("\n\n게임에서 승리하셨습니다!!!")
        break

    # print(stage, len(co)) # 디버깅용 print()
    time.sleep(sleep_time)

    if count == 0:  # 처음 인풋을 받기 시작하는 경우
        input_thread.start()

    if is_input_new:  # 액션을 새로 입력받은 경우
        if action in ["w", "s", "a", "d"]:  # 유저가 우주선을 이동하는 경우
            co[0].move(action)
            is_input_new = False

    # 유저의 우주선이 장애물과 부딫히면 게임 오버시키는 기능
    if co[0].coord in [i.coord for i in co if (isinstance(i, Obstacle))]:
        for i in range(1, len(co)):
            is_game_over = True
            break

    # 게임오버 하는 경우, 디버깅 용도로 주석 처리 가능
    if is_game_over:
        print("\n게임오버 되었습니다!")
        break

    # arrow shooter가 일정 시간마다 화살을 발사하는 것을 구현함.
    ias = [index for index, j in enumerate(co) if isinstance(j, ArrowShooter)]  # indices of arrow shooters
    if len(ias) >= 1 and count % (3 / sleep_time) == 0:
        for i in ias:
            if co[i].type == 1:  # ■의 경우 상하좌우로 화살을 발사함
                co.extend([Arrow([co[i].coord[0] - 1, co[i].coord[1]], 3),
                           Arrow([co[i].coord[0] + 1, co[i].coord[1]], 4),
                           Arrow([co[i].coord[0], co[i].coord[1] + 1], 1),
                           Arrow([co[i].coord[0], co[i].coord[1] - 1], 2)])
                for j in range(-4, 0):
                    co[j].start()
            elif co[i].type == 2:  # ◆의 경우 모든 대각선 방향으로 화살을 발사함
                co.extend([Arrow([co[i].coord[0] - 1, co[i].coord[1] - 1], 5),
                           Arrow([co[i].coord[0] - 1, co[i].coord[1] + 1], 7),
                           Arrow([co[i].coord[0] + 1, co[i].coord[1] - 1], 6),
                           Arrow([co[i].coord[0] + 1, co[i].coord[1] + 1], 8)])
                for j in range(-4, 0):
                    co[j].start()
            elif co[i].type == 3:  # ★의 경우 주변 8 방향으로 화살을 발사함
                co.extend([Arrow([co[i].coord[0] - 1, co[i].coord[1]], 3),
                           Arrow([co[i].coord[0] + 1, co[i].coord[1]], 4),
                           Arrow([co[i].coord[0], co[i].coord[1] + 1], 1),
                           Arrow([co[i].coord[0], co[i].coord[1] - 1], 2),
                           Arrow([co[i].coord[0] - 1, co[i].coord[1] - 1], 5),
                           Arrow([co[i].coord[0] - 1, co[i].coord[1] + 1], 7),
                           Arrow([co[i].coord[0] + 1, co[i].coord[1] - 1], 6),
                           Arrow([co[i].coord[0] + 1, co[i].coord[1] + 1], 8)])
                for j in range(-8, 0):
                    co[j].start()

    ia = [i for i, j in enumerate(co) if isinstance(j, Obstacle)]  # indices of obstacles
    iabd = []  # indices of bullets witch will be deleted

    for i in ia:  # 판을 나가게 되는 등의 이유로 없앨 화살들을 좌표 hor, ver로 모아준 것들
        if co[i].coord == [hor, ver]:
            iabd.append(i)

    # 기존에 지정해 준 삭제 대상들의 인덱스가 무효화되는 것을 방지하기 위해서 인덱스가 높은 순서대로 제거하기 위해 내림차순 정렬해줌
    iabd.sort(reverse=True)

    # 필요 없어진 객체들(판의 경계를 지나는 화살 및 기타 장애물)을 제거해 줌
    for i in iabd:
        del co[i]

    if 1 <= stage < 2:
        if count == int(1 / sleep_time):  # 처음 게임 시작 1초 후에 화살(2)를 하나 생성함
            co.extend([Arrow([2, 1], 2, 1)])
            co[-1].start()
            stage += 0.1
            stage = round(stage, 1)

        elif stage == 1.1:
            # 처음 화살을 생성한 이후에 0.3초마다 화살(2)를 하나씩 총 4개 생성함
            if count % int(0.3 / sleep_time) == 0:
                # 이터러블을 복사하여 길이를 확인하여 길이가 1 이상이면 이터러블의 내용물을 하나 실행함
                s1_1_ori, s1_1_ori_c = itertools.tee(s1_1_ori)  # stage 1.1의 object range iterable, c: copied
                if itc(s1_1_ori_c) >= 1:
                    co.extend([Arrow([s1_1_ori.__next__(), 1], 2, 1)])
                    co[-1].start()
                # 이터러블의 내용물을 전부 사용한 경우
                else:
                    stage += 0.1
                    stage = round(stage, 1)
        elif stage == 1.2:
            # 스테이지 1.1이 끝난 이후에 0.3초마다 화살(2)를 하나씩 총 5개 생성함
            if rest_time <= 28:
                if count % int(0.3 / sleep_time) == 0:
                    # 이터러블을 복사하여 길이를 확인하여 길이가 1 이상이면 이터러블의 내용물을 하나 실행함
                    s1_2_ori, s1_2_ori_c = itertools.tee(s1_2_ori)
                    if itc(s1_2_ori_c) >= 1:
                        co.extend([Arrow([s1_2_ori.__next__(), 1], 2, 1)])
                        co[-1].start()
                    # 이터러블의 내용물을 전부 사용한 경우
                    else:
                        stage += 0.1
                        stage = round(stage, 1)
        elif stage == 1.3:
            # 스테이지 1.2이 끝난 이후에 0.4초마다 화살(2)를 하나씩 총 5개 생성함
            if rest_time <= 27:
                if count % int(0.3 / sleep_time) == 0:
                    # 이터러블을 복사하여 길이를 확인하여 길이가 1 이상이면 이터러블의 내용물을 하나 실행함
                    s1_3_ori, s1_3_ori_c = itertools.tee(s1_3_ori)
                    if itc(s1_3_ori_c) >= 1:
                        co.extend([Arrow([s1_3_ori.__next__(), 1], 2, 1)])
                        co[-1].start()
                    # 이터러블의 내용물을 전부 사용한 경우
                    else:
                        stage += 0.1
                        stage = round(stage, 1)
        elif stage == 1.4:
            # 스테이지 1.3이 끝난 이후에 0.4초마다 화살(2)를 하나씩 총 5개 생성함
            if rest_time <= 26:
                if count % int(0.3 / sleep_time) == 0:
                    # 이터러블을 복사하여 길이를 확인하여 길이가 1 이상이면 이터러블의 내용물을 하나 실행함
                    s1_4_ori, s1_4_ori_c = itertools.tee(s1_4_ori)
                    if itc(s1_4_ori_c) >= 1:
                        co.extend([Arrow([s1_4_ori.__next__(), 1], 2, 1)])
                        co[-1].start()
                    # 이터러블의 내용물을 전부 사용한 경우
                    elif len(co) == 1:
                        stage += 0.6
                        stage = round(stage, 1)
                        rest_time = 30

    elif 2 <= stage < 3:
        if 14 <= rest_time <= 28:  # 스테이지 2 시작 2초 후에 화살(2) 2개를 랜덤한 위치에 0.4초마다 지속적으로 생성함
            if count % int(0.4 / sleep_time) == 0:
                random_places = ra.sample(range(1, 10), 2)
                co.extend([Arrow([random_places[0], 1], 2), Arrow([random_places[1], 1], 2)])
                for i in range(-2, 0):
                    co[i].start()
                stage = round(stage, 1)
        # 제한 시간동안 살아남은 경우
        elif rest_time < 14 and len(co) == 1:
            stage += 1
            stage = round(stage, 1)
            rest_time = 30

    elif 3 <= stage < 4:
        if stage == 3:
            if 22 <= rest_time <= 28:
                if count % int(2 / sleep_time) == 0:
                    spike_wall(s3_ori_x.__next__(), s3_ori.__next__())
                    for i in range(-27, 0):
                        co[i].start()
            # 제한 시간동안 살아남은 경우
            elif rest_time < 22 and len(co) == 1:
                stage += 1
                stage = round(stage, 1)
                rest_time = 30

    # 상하, 좌우, 각 방향 대각선, 상하좌우, 전 방향 대각선, 전 방향 랜덤 화살
    elif 4 <= stage < 5:
        if stage == 4:
            # 상, 하 방향 화살
            if 26 <= rest_time <= 28:
                if count % int(0.2 / sleep_time) == 0:
                    co.extend([Arrow([ra.choice([i for i in range(1, 10)]), s4_1_ori_y.__next__()], s4_1_ori.__next__())])
                    co[-1].start()
            # 좌, 우 방향 화살
            elif 22 <= rest_time < 25:
                if count % int(0.2 / sleep_time) == 0:
                    co.extend([Arrow([s4_2_ori_x.__next__(), ra.choice([i for i in range(1, 14)])], s4_2_ori.__next__())])
                    co[-1].start()
            # 좌상, 우하 방향 화살
            elif 19 <= rest_time < 21:
                if count % int(0.2 / sleep_time) == 0:
                    co.extend([Arrow([s4_3_ori_x.__next__(), ra.choice([i for i in range(1, 14)])], s4_3_ori.__next__())])
                    co[-1].start()
            # 우상, 좌하 방향 화살
            elif 16 <= rest_time < 18:
                if count % int(0.2 / sleep_time) == 0:
                    co.extend([Arrow([s4_4_ori_x.__next__(), ra.choice([i for i in range(1, 14)])], s4_4_ori.__next__())])
                    co[-1].start()
            # 상, 우, 하, 좌 방향 화살
            elif 13 <= rest_time < 15:
                if count % int(0.2 / sleep_time) == 0:
                    s4_5_ori, s4_5_ori_c = itertools.tee(s4_5_ori)

                    if s4_5_ori_c.__next__() in [1, 2]:
                        co.extend([Arrow([ra.choice([i for i in range(1, 10)]),
                                          s4_5_ori_y.__next__()], s4_5_ori.__next__())])
                    else:
                        co.extend([Arrow([s4_5_ori_x.__next__(),
                                          ra.choice([i for i in range(1, 14)])], s4_5_ori.__next__())])
                    co[-1].start()
            # 우상, 우하, 좌하, 좌상 방향 화살
            elif 10 <= rest_time < 12:
                if count % int(0.2 / sleep_time) == 0:
                    co.extend([Arrow([s4_6_ori_x.__next__(),
                                      ra.choice([i for i in range(1, 14)])], s4_6_ori.__next__())])
                    co[-1].start()

            # 상, 우상, 우, 우하, 하, 좌하, 좌, 좌상 방향 화살
            elif 5 <= rest_time < 9:
                if count % int(0.2 / sleep_time) == 0:
                    s4_7_ori, s4_7_ori_c = itertools.tee(s4_7_ori)

                    if s4_7_ori_c.__next__() in [1, 2]:
                        co.extend([Arrow([ra.choice([i for i in range(1, 10)]),
                                          s4_7_ori_y.__next__()], s4_7_ori.__next__())])
                    else:
                        co.extend([Arrow([s4_7_ori_x.__next__(),
                                          ra.choice([i for i in range(1, 14)])], s4_7_ori.__next__())])
                    co[-1].start()
            elif rest_time < 5 and len(co) == 1:
                stage += 1
                stage = round(stage, 1)
                rest_time = 30

    elif 5 <= stage < 6:
        homing_arrows1 = [HomingArrow([1, 3], 4), HomingArrow([1, 6], 4), HomingArrow([1, 8], 4),
                          HomingArrow([1, 11], 4), HomingArrow([9, 3], 3), HomingArrow([9, 6], 3),
                          HomingArrow([9, 8], 3), HomingArrow([9, 11], 3), HomingArrow([2, 1], 2),
                          HomingArrow([5, 1], 2), HomingArrow([8, 1], 2), HomingArrow([2, 13], 1),
                          HomingArrow([5, 13], 1), HomingArrow([8, 13], 1)]
        homing_arrows2 = [HomingArrow([1, 1], 2), HomingArrow([9, 1], 2), HomingArrow([1, 13], 1),
                          HomingArrow([9, 13], 1)]
        if stage == 5:
            if rest_time <= 28:
                co.extend(homing_arrows1)
                for i in range(-len(homing_arrows1), 0):
                    co[i].start()
                stage += 0.1
                stage = round(stage, 1)
        elif stage == 5.1:
            if rest_time <= 26:
                co.extend(homing_arrows2)
                for i in range(-len(homing_arrows2), 0):
                    co[i].start()
                stage += 0.1
                stage = round(stage, 1)
        elif stage == 5.2:
            if rest_time <= 20 and len(co) == 1:
                stage += 0.8
                stage = round(stage, 1)
                rest_time = 30

    elif 6 <= stage < 7:
        if stage == 6:
            if rest_time <= 28:
                co.extend([ArrowShooter([1, 3], 4, 1), ArrowShooter([9, 3], 3, 1)])
                for i in range(-2, 0):
                    co[i].start()
                stage += 0.1
                stage = round(stage, 1)
        elif stage == 6.1:
            if 15 < rest_time <= 26:
                if count % int(4 / sleep_time) == 0:
                    co.extend([ArrowShooter([1, 1], 2, 2), ArrowShooter([9, 1], 2, 2), ArrowShooter([1, 13], 1, 2),
                               ArrowShooter([9, 13], 1, 2)])
                    for i in range(-4, 0):
                        co[i].start()
            elif rest_time <= 15 and len(co) == 1:
                stage += 0.9
                stage = round(stage, 1)
                rest_time = 30

    elif 7 <= stage < 8:
        if stage == 7:
            if rest_time <= 27:
                co.extend([ArrowShooter([3, 1], 2, 3), ArrowShooter([7, 13], 1, 3)])
                for i in range(-2, 0):
                    co[i].start()
                stage += 0.1
                stage = round(stage, 1)
        elif stage == 7.1:
            if rest_time <= 23:
                co.extend([ArrowShooter([1, 4], 4, 3), ArrowShooter([9, 10], 3, 3)])
                for i in range(-2, 0):
                    co[i].start()
                stage += 0.1
                stage = round(stage, 1)
        elif stage == 7.2:
            if rest_time <= 17:
                co.extend([ArrowShooter([1, 1], 2, 3), ArrowShooter([9, 1], 2, 3),
                           ArrowShooter([1, 13], 1, 3), ArrowShooter([9, 13], 1, 3)])
                for i in range(-4, 0):
                    co[i].start()
                stage += 0.1
                stage = round(stage, 1)
        elif stage == 7.3:
            if rest_time <= 13:
                co.extend([ArrowShooter([1, 1], 4, 3), ArrowShooter([9, 1], 3, 3),
                           ArrowShooter([1, 13], 4, 3), ArrowShooter([9, 13], 3, 3)])
                for i in range(-4, 0):
                    co[i].start()
                stage += 0.1
                stage = round(stage, 1)
        elif stage == 7.4:
            if rest_time <= 10 and len(co) == 1:
                stage += 0.6
                stage = round(stage, 1)

    count += 1
