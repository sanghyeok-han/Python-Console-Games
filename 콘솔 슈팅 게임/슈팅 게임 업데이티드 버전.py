import threading
import time
import os
import msvcrt
import random as ra

hor = 12
ver = 7


class User:
    def __init__(self):
        self.shape = "▷"
        self.coord = [2, 2]
        self.direction = 0
        self.hp = 3
        self.former_coord = self.coord[:]

    def move(self, direction):

        self.direction = direction
        self.former_coord = self.coord[:]  # 유저 우주선의 이동 직전 좌표

        # w,s,a,d는 각각 상,하,좌,우
        if self.direction == "w" and self.coord[1] != 1:
            self.coord[1] -= 1
        elif self.direction == "s" and self.coord[1] != ver - 2:
            self.coord[1] += 1
        elif self.direction == "a" and self.coord[0] != 1:
            self.coord[0] -= 1
        elif self.direction == "d" and self.coord[0] != hor - 2:
            self.coord[0] += 1


class Enemy:
    pass


class MovingEnemy(threading.Thread, Enemy):  # 움직이는 적

    def __init__(self, coord):
        threading.Thread.__init__(self)
        self.coord = coord
        self.shape = "■"
        self.hp = 3
        self.direction = 1  # 1: 왼쪽, 2: 오른쪽

    def run(self):
        time.sleep(0.2)
        while True:
            if self.coord[0] == 1:
                self.direction = 2
            elif self.coord[0] == hor - 2:
                self.direction = 1

            if self.direction == 1:  # 왼쪽으로 움직이는 경우
                self.coord[0] -= 1
            else:  # 오른쪽으로 움직이는 경우
                self.coord[0] += 1

            time.sleep(0.5)


class StrongMovingEnemy(threading.Thread, Enemy):  # 거꾸로 된 ㄹ자 모양으로 움직이는 적

    def __init__(self, coord):
        threading.Thread.__init__(self)
        self.coord = coord
        self.shape = "▣"
        self.hp = 6
        self.direction = 3  # 1,2,3,4: 상하좌우
        self.trend = 3  # 3: 왼쪽, 4: 오른쪽, # 전체적으로 움직이는 방향, 처음에는 왼쪽으로 움직임
        self.init_ycoord = coord[1]  # 생성시 처음 y 좌표

    def run(self):
        time.sleep(0.2)
        while True:
            if self.coord[0] == 1:
                self.trend = 4
            elif self.coord[0] == hor - 2:
                self.trend = 3

            if self.direction in [1, 2]:  # 바로 이전에 위쪽 또는 아래쪽으로 움직였던 경우
                self.direction = self.trend

            else:  # 바로 이전에 왼쪽 또는 오른쪽으로 움직였던 경우
                if self.coord[1] == self.init_ycoord:  # 현재 y 좌표가 생성시 처음 y 좌표와 같은 경우
                    self.direction = 2
                else:  # 현재 y 좌표가 생성시 처음 y 좌표와 다른 경우
                    self.direction = 1

            if self.direction == 1:  # 위쪽으로 움직이는 경우
                self.coord[1] -= 1
            elif self.direction == 2:  # 아래쪽으로 움직이는 경우
                self.coord[1] += 1
            elif self.direction == 3:  # 왼쪽으로 움직이는 경우
                self.coord[0] -= 1
            else:  # 오른쪽으로 움직이는 경우
                self.coord[0] += 1

            time.sleep(0.5)


class ShootingEnemy(Enemy):  # 제자리에서 슈팅하는 적
    def __init__(self, coord):
        self.coord = coord
        self.shape = "◆"
        self.hp = 3


class MovingShootingEnemy(threading.Thread, Enemy):  # 상하로 움직이며 슈팅하는 적
    def __init__(self, coord, moving_type):
        threading.Thread.__init__(self)
        self.coord = coord
        self.shape = "◈"
        self.hp = 6
        self.direction = 1  # 1,2: 상하
        self.init_ycoord = coord[1]  # 생성시 처음 y 좌표
        self.type = moving_type  # type가 1이면 먼저 위쪽으로 올라가고, 2이면 먼저 아래쪽으로 내려감

    def run(self):
        time.sleep(0.2)
        while True:
            if self.type == 1:  # 처음 생성시 위쪽으로 먼저 움직이는 타입인 경우
                if self.coord[1] == self.init_ycoord:  # 현재 y 좌표가 생성시 처음 y 좌표와 같은 경우 위쪽으로 움직이게 함
                    self.direction = 1
                else:  # 현재 y 좌표가 생성시 처음 y 좌표와 다른 경우 아래쪽으로 움직이게 함
                    self.direction = 2

            else:  # 처음 생성시 아래쪽으로 먼저 움직이는 타입인 경우
                if self.coord[1] == self.init_ycoord:  # 현재 y 좌표가 생성시 처음 y 좌표와 같은 경우 아래쪽으로 움직이게 함
                    self.direction = 2
                else:  # 현재 y 좌표가 생성시 처음 y 좌표와 다른 경우 위쪽으로 움직이게 함
                    self.direction = 1

            if self.direction == 1:  # 위쪽으로 움직이는 경우
                self.coord[1] -= 1
            else:  # 아래쪽으로 움직이는 경우
                self.coord[1] += 1

            time.sleep(0.5)


class TeleportingShootingEnemy(threading.Thread, Enemy):
    def __init__(self, coord):
        threading.Thread.__init__(self)
        self.coord = coord
        self.shape = "◇"
        self.hp = 3

    def run(self):
        while True:
            self.coord = [self.coord[0], ra.choice(range(1, ver - 1))]  # 해당 x 축의 랜덤한 y축 좌표로 순간 이동함
            time.sleep(0.5)


class HomingShootingEnemy(Enemy):  # 유도탄을 발사하는 적
    def __init__(self, coord):
        self.coord = coord
        self.shape = "◎"
        self.hp = 10


class BossTypeEnemy(Enemy):  # 보스 타입 적
    pass


class SemiBoss1(BossTypeEnemy):
    def __init__(self, coord):
        self.coord = coord
        self.shape = "☆"
        self.hp = 12


class SemiBoss2(threading.Thread, BossTypeEnemy):
    def __init__(self, coord):
        threading.Thread.__init__(self)
        self.coord = coord
        self.shape = "♠"
        self.hp = 15
        self.direction = 1  # 1,2: 상하
        self.init_ycoord = coord[1]  # 생성시 처음 y 좌표

    def run(self):
        time.sleep(0.5)
        while True:
            if self.coord[1] == self.init_ycoord - 1:  # 현재 y 좌표가 생성시 처음 y 좌표 한 칸 위쪽과 같은 경우 아래쪽으로 움직이게 함
                self.direction = 2
            elif self.coord[1] == self.init_ycoord + 1:  # 현재 y 좌표가 생성시 처음 y 좌표 한 칸 아래쪽과 같은 경우 위쪽으로 움직이게 함
                self.direction = 1

            if self.direction == 1:  # 위쪽으로 움직이는 경우
                self.coord[1] -= 1
            else:  # 아래쪽으로 움직이는 경우
                self.coord[1] += 1

            time.sleep(0.5)


class Boss(threading.Thread, BossTypeEnemy):
    def __init__(self, coord):
        threading.Thread.__init__(self)
        self.coord = coord
        self.shape = "★"
        self.hp = 60
        self.direction = 1  # 1,2: 상하
        self.init_ycoord = coord[1]  # 생성시 처음 y 좌표

    def run(self):
        time.sleep(0.6)
        while True:
            if self.coord[1] == self.init_ycoord - 1:  # 현재 y 좌표가 생성시 처음 y 좌표 한 칸 위쪽과 같은 경우 아래쪽으로 움직이게 함
                self.direction = 2
            elif self.coord[1] == self.init_ycoord + 1:  # 현재 y 좌표가 생성시 처음 y 좌표 한 칸 아래쪽과 같은 경우 위쪽으로 움직이게 함
                self.direction = 1

            if self.direction == 1:  # 위쪽으로 움직이는 경우
                self.coord[1] -= 1
            else:  # 아래쪽으로 움직이는 경우
                self.coord[1] += 1

            time.sleep(0.6)


class UserBullet(threading.Thread):  # 유저가 발사하는 총알
    def __init__(self, user):
        threading.Thread.__init__(self)
        self.shape = " -"
        self.coord = [user.coord[0] + 1, user.coord[1]]

    def run(self):
        time.sleep(0.1)
        while True:
            self.coord[0] += 1

            if self.coord[0] >= hor - 1:
                self.coord = [hor, ver]
                break

            time.sleep(0.3)


class EnemyBullet:
    pass


class NormalEnemyBullet(threading.Thread, EnemyBullet):  # 적이 발사하는 총알

    def __init__(self, coord):
        threading.Thread.__init__(self)
        self.shape = "←"
        self.coord = coord

    def run(self):
        time.sleep(0.1)
        while True:
            self.coord[0] -= 1

            if self.coord[0] == 0:
                self.coord = [hor, ver]
                break

            time.sleep(0.3)


class HomingEnemyBullet(threading.Thread, EnemyBullet):  # 적이 발사하는 유도탄

    def __init__(self, coord):
        threading.Thread.__init__(self)
        self.shape = "←"
        self.coord = coord

    def run(self):
        global co

        time.sleep(0.1)
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


def show(co, stage):  # 현재 판 상황 출력 위한 함수

    print("{0}".format("\n"*3))

    if stage < 10:
        print("{0:20s} Stage: {1} {2:>10s}".format(" ", int(stage), "♥" * co[0].hp))
    else:
        print("{0:20s} Stage: Final {1:>6s}".format(" ", "♥" * co[0].hp))

    for j in range(0, ver):

        print("{0:20s}".format(""), end="")

        for i in range(0, hor):
            for k in co:
                if [i, j] == k.coord:
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


# 0.08 0.14
# 0.07 0.12
# 0.06 0.10
def get_input(val):  # 거의 실시간으로 유저로부터 인풋을 받음
    global action
    global is_input_new

    while True:
        time.sleep(0.06)

        if msvcrt.kbhit():  # 유저가 키를 입력한 경우
            input_action = msvcrt.getch().decode("utf-8").lower()  # 엔터를 누르지 않아도 해당 값을 바로 input_action 이라는 변수에 할당함

            if input_action in ["w", "s", "a", "d", " "]:
                action = input_action
                is_input_new = True
        else:
            action = 0


co = [User()]   # Current objects
input_thread = threading.Thread(target=get_input, args=(1,))

action = 0
is_input_new = False
count = 0
stage = 1
attack_type = 0  # 보스의 공격 종류
attack_count = 0  # 보스가 같은 공격을 한 횟수
aac = 0  # attack available count, 보스가 다음 공격을 할 수 있는 count

while True:

    os.system("cls")

    show(co, stage)  # 현재 게임 판의 상황을 보여줌
    print("\n이동: (w: 위, s: 아래, a: 왼쪽, d: 오른쪽), 공격: space 키")

    if stage == 11:
        print("\n\n\n\n\n게임에서 승리하셨습니다!!!")
        break

    sleep_time = 0.1
    time.sleep(sleep_time)

    if count == 0:  # 처음 인풋을 받기 시작하는 경우
        input_thread.start()

    if is_input_new:  # 액션을 새로 입력받은 경우

        if action in ["w", "s", "a", "d"]:  # 유저가 우주선을 이동하는 경우
            co[0].move(action)
            is_input_new = False
        elif action == " ":  # 유저가 슈팅을 하는 경우
            co.append(UserBullet(co[0]))
            co[-1].start()

    # ShootingEnemy는 3초마다 총알을 발사함 (적의 총알 또한 객체로 관리함)
    ise = [i for i, j in enumerate(co) if isinstance(j, ShootingEnemy)]  # indices of shooting enemies
    if count % int(3 / sleep_time) == 0:
        if len(ise) >= 1:
            for i in ise:
                co.append(NormalEnemyBullet([co[i].coord[0] - 1, co[i].coord[1]]))
                co[-1].start()

    # MovingShootingEnemy, TeleportingShootingEnemy는 2초마다 총알을 발사함
    # indices of Moving or Teleporting Shooting enemies
    imtse = [i for i, j in enumerate(co) if isinstance(j, MovingShootingEnemy) or
             isinstance(j, TeleportingShootingEnemy)]
    if count % int(2 / sleep_time) == 0:
        if len(imtse) >= 1:
            for i in imtse:
                co.append(NormalEnemyBullet([co[i].coord[0] - 1, co[i].coord[1]]))
                co[-1].start()

    # HomingShootingEnemy는 7초마다 유도탄을 발사함
    ihse = [i for i, j in enumerate(co) if isinstance(j, HomingShootingEnemy)]  # indices of HomingShooting enemies
    if count % int(7 / sleep_time) == 0:
        if len(ihse) >= 1:
            for i in ihse:
                co.append(HomingEnemyBullet([co[i].coord[0] - 1, co[i].coord[1]]))
                co[-1].start()

    # Semiboss1은 1.5초마다 x, [y-1, y, y+1] 좌표에 총알을 발사함
    isb1 = [i for i, j in enumerate(co) if isinstance(j, SemiBoss1)]  # indices of semi boss
    if count % int(1.5 / sleep_time) == 0:
        if len(isb1) >= 1:
            for i in isb1:
                co.extend([NormalEnemyBullet([co[i].coord[0] - 1, co[i].coord[1] - 1]),
                           NormalEnemyBullet([co[i].coord[0] - 1, co[i].coord[1]]),
                           NormalEnemyBullet([co[i].coord[0] - 1, co[i].coord[1] + 1])])
                co[-3].start()
                co[-2].start()
                co[-1].start()

    # Semiboss2는 8초마다 x, [y-1, y+1] 좌표에 유도탄을 발사함
    isb2 = [i for i, j in enumerate(co) if isinstance(j, SemiBoss2)]  # indices of semi boss
    if count % int(8 / sleep_time) == 0:
        if len(isb2) >= 1:
            for i in isb2:
                co.extend([HomingEnemyBullet([co[i].coord[0], co[i].coord[1] - 1]),
                           HomingEnemyBullet([co[i].coord[0], co[i].coord[1] + 1])])
                co[-2].start()
                co[-1].start()

    # 보스는 두 가지 타입의 공격을 랜덤으로 섞어서 하다가 체력이 적을 때 마지막 타입의 공격을 함
    ifb = [i for i, j in enumerate(co) if isinstance(j, Boss)]  # index of final boss
    if len(ifb) == 1:

        # 보스의 체력이 20 이하이며, 진행중인 공격이 없는 경우 type 3 공격을 시작함
        if attack_type == 0 and co[ifb[0]].hp <= 20:
            if count == aac:
                attack_type = 3
        else:
            if aac == 0:  # 보스가 아직 공격하지 않은 경우
                attack_type = ra.choice([1, 2])
            else:
                if count == aac:
                    if attack_type == 0.9:  # 보스의 type 1 공격이 진행중인 경우
                        attack_type = 1
                    elif attack_type == 1.9:  # 보스의 type 2 공격이 진행중인 경우
                        attack_type = 2
                    elif attack_type == 2.9:  # 보스의 type 3 공격이 진행중인 경우
                        attack_type = 3
                    else:
                        attack_type = ra.choice([1, 2])

        if attack_type == 1:

            co.extend([NormalEnemyBullet([co[ifb[0]].coord[0] - 1, co[ifb[0]].coord[1] - 1]),
                       NormalEnemyBullet([co[ifb[0]].coord[0] - 1, co[ifb[0]].coord[1]]),
                       NormalEnemyBullet([co[ifb[0]].coord[0] - 1, co[ifb[0]].coord[1] + 1])])
            for i in range(-3, 0):
                co[i].start()

            attack_count += 1

            if attack_count == 1:  # 보스가 attack type1의 공격을 1회 한 경우
                attack_type = 0.9
                aac = count + int(0.7 / sleep_time)  # 공격 쿨타임 0.7초
            elif attack_count == 2:  # 보스가 attack type1의 공격을 2회 한 경우
                attack_type = 0
                aac = count + int(2 / sleep_time)  # 공격 쿨타임 2초
                attack_count = 0  # 보스가 attack type1의 공격을 연속으로 한 횟수를 초기화해 줌

        elif attack_type == 2:

            if attack_count == 0:
                co.extend([HomingEnemyBullet([co[ifb[0]].coord[0], co[ifb[0]].coord[1] - 1]),
                           HomingEnemyBullet([co[ifb[0]].coord[0], co[ifb[0]].coord[1] + 1])])
                co[-2].start()
                co[-1].start()
                attack_type = 1.9
                attack_count += 1
                aac = count + int(3 / sleep_time)  # 공격 쿨타임 3초
            elif attack_count == 1:  # 보스가 attack type2의 공격을 1회 한 경우
                co.extend([HomingEnemyBullet([co[ifb[0]].coord[0] - 1, co[ifb[0]].coord[1]])])
                co[-1].start()
                attack_type = 0
                attack_count = 0
                aac = count + int(8 / sleep_time)  # 공격 쿨타임 8초

        elif attack_type == 3:

            if attack_count == 0:
                co.extend([NormalEnemyBullet([9, 1]), NormalEnemyBullet([9, 3]), NormalEnemyBullet([9, 5])])
                for i in range(-3, 0):
                    co[i].start()
                attack_type = 2.9
                attack_count += 1
                aac = count + int(0.7 / sleep_time)  # 공격 쿨타임 0.7초

            elif attack_count == 1:  # 보스가 attack type3의 공격을 1회 한 경우
                co.extend([NormalEnemyBullet([9, 2]), NormalEnemyBullet([9, 4])])
                for i in range(-2, 0):
                    co[i].start()
                attack_type = 0
                attack_count = 0  # 보스가 attack type3의 공격을 연속으로 한 횟수를 초기화해 줌
                aac = count + int(1 / sleep_time)  # 공격 쿨타임 1초

    # 보스전에서 보스가 있을 때 텔레포트하는 적이 사라지면 해당 적을 6초 뒤에 다시 소환하는 기능
    if stage >= 10:

        ifb = [i for i, j in enumerate(co) if isinstance(j, Boss)]  # index of final boss
        # indices of TeleportingShootingEnemies witch x coord is 9
        itsbx9 = [i for i, j in enumerate(co) if isinstance(j, TeleportingShootingEnemy) and j.coord[0] == 9]
        # indices of TeleportingShootingEnemies witch x coord is 8
        itsbx8 = [i for i, j in enumerate(co) if isinstance(j, TeleportingShootingEnemy) and j.coord[0] == 8]

        if len(ifb) == 1:
            if count % int(6 / sleep_time) == 0:
                if co[ifb[0]].hp > 15:  # 보스의 현재 체력이 15 보다 많은 경우 TeleportingShootingEnemy 하나를 무한 리스폰함
                    if len(itsbx9) == 0:
                        co.extend([TeleportingShootingEnemy([9, 3])])
                        co[-1].start()
                # 보스의 현재 체력이 15 보다 적으며, type 3 공격을 시작한 이후로 TeleportingShootingEnemy 둘을 무한 리스폰함
                elif co[ifb[0]].hp <= 15 and attack_type in [0, 2.9, 3]:
                    if len(itsbx9) == 0:
                        co.extend([TeleportingShootingEnemy([9, 3])])
                        co[-1].start()
                    if len(itsbx8) == 0:
                        co.extend([TeleportingShootingEnemy([8, 3])])
                        co[-1].start()

    ie = [i for i, j in enumerate(co) if isinstance(j, Enemy)]  # indices of enemies
    ib = [i for i, j in enumerate(co) if isinstance(j, UserBullet) or isinstance(j, EnemyBullet)]  # indices of bullets

    ide = []  # indices of defeated enemies
    idbd = []  # indices of bullets witch will be deleted

    eo = []  # expired objects

    # 유저의 우주선이 적의 공격을 받았거나 적과 부딫힌 경우 적의 체력을 0으로 만들며 유저 우주선의 체력을 1 줄임
    # 단 준보스급 이상 적과 부딫힌 경우에는 유저 우주선의 체력만 1 줄이며 이전 좌표로 되돌려보냄
    if co[0].coord in [i.coord for i in co if (isinstance(i, EnemyBullet) or isinstance(i, Enemy))]:
        for i in range(1, len(co)):
            if co[0].coord == co[i].coord and (isinstance(co[i], EnemyBullet) or isinstance(co[i], Enemy) and not (
                    isinstance(co[i], BossTypeEnemy))):
                ide.append(i)
                co[0].hp -= 1
                break
            elif co[0].coord == co[i].coord and isinstance(co[i], BossTypeEnemy):
                co[0].hp -= 1
                co[0].coord = co[0].former_coord[:]
                break

    if co[0].hp <= 0:  # 유저 우주선의 체력이 0이 된 경우
        print("\n게임오버 되었습니다!")
        break

    for i in ie:  # 유저의 공격이 적을 맞춘 경우 해당 적의 체력을 1 줄이고 해당 적을 맞춘 총알을 특정함
        if co[i].coord in [j.coord for j in co if isinstance(j, UserBullet)]:  # 유저의 공격의 적을 맞춘 경우 적의 체력을 1 줄임
            co[i].hp -= 1

            for j in range(len(co)):  # 적을 맞춘 총알들의 좌표를 [hor, ver]로 옮김 (추후 객체 삭제 목적)
                if j != i and co[j].coord == co[i].coord:
                    co[j].coord = [hor, ver]

        if co[i].hp <= 0:  # 적의 체력이 0이 된 경우 해당 적들의 인덱스를 저장함 (추후 객체 삭제 목적)
            ide.append(i)

    # 보스의 체력이 0이 되면 남은 적을 모두 제거함
    if stage >= 10:
        ifb = [i for i, j in enumerate(co) if isinstance(j, Boss)]  # index of final boss
        # 보스가 쓰러진 경우
        if len(ifb) == 0:
            while len(ie) >= 1:
                ofn = ie.pop()  # one of final enemies
                if ofn not in ide:
                    ide.append(ofn)

    for i in ib:  # 판을 나가게 되는 등의 이유로 없앨 총알들을 좌표 hor, ver로 모아준 것들
        if co[i].coord == [hor, ver]:
            idbd.append(i)

    eo = ide + idbd
    # 기존에 지정해 준 삭제 대상들의 인덱스가 무효화되는 것을 방지하기 위해서 인덱스가 높은 순서대로 제거하기 위해 내림차순 정렬해줌
    eo.sort(reverse=True)

    # 필요 없어진 객체들(체력이 0인 적과 적을 맞춘 총알과 판의 경계를 지나는 총알)을 제거해 줌
    for i in eo:
        del co[i]

    if count == int(1/sleep_time):  # 처음 게임 시작 1초 후에 적을 2개 생성함
        co.extend([ShootingEnemy([9, 2]), ShootingEnemy([9, 4])])
        stage += 0.1

    ie = [i for i, j in enumerate(co) if isinstance(j, Enemy)]  # indices of enemies

    if stage >= 1.1 and len(ie) == 0:  # 현재 스테이지의 모든 적을 클리어한 경우
        time.sleep(0.3)
        # 스테이지가 끝난 다음 유저의 우주선을 제외한 나머지 객체를 모두 제거해줌
        for i in reversed(range(1, len(co))):
            del co[i]
            
        stage += 0.9
        stage = round(stage)

    if stage == 2:
        co.extend([ShootingEnemy([9, 1]), ShootingEnemy([9, 3]), ShootingEnemy([9, 5]), MovingEnemy([10, 2]),
                   MovingEnemy([10, 4])])
        for i in range(-2, 0):
            co[i].start()
        stage += 0.1

    if stage == 3:
        co.extend([ShootingEnemy([8, 2]), ShootingEnemy([8, 4]), ShootingEnemy([10, 1]), ShootingEnemy([10, 3]),
                   ShootingEnemy([10, 5])])
        stage += 0.1

    if stage == 4:
        co.extend([SemiBoss1([10, 3]), MovingEnemy([9, 1]), MovingEnemy([9, 5])])
        for i in range(-2, 0):
            co[i].start()
        stage += 0.1

    if stage == 5:
        co.extend([ShootingEnemy([7, 3]), ShootingEnemy([8, 3]), ShootingEnemy([9, 3]), ShootingEnemy([10, 3]),
                   StrongMovingEnemy([7, 1]), StrongMovingEnemy([7, 4]), MovingShootingEnemy([10, 1], 2),
                   MovingShootingEnemy([10, 5], 1)])
        for i in range(-4, 0):
            co[i].start()
        stage += 0.1

    if stage == 6:
        co.extend([ShootingEnemy([7, 1]), ShootingEnemy([7, 5]), ShootingEnemy([8, 1]), ShootingEnemy([8, 5]),
                   MovingEnemy([1, 3]), MovingEnemy([10, 3]), MovingShootingEnemy([10, 1], 2),
                   MovingShootingEnemy([10, 5], 1)])
        for i in range(-4, 0):
            co[i].start()
        stage += 0.1

    if stage == 7:
        co.extend([HomingShootingEnemy([10, 1]), StrongMovingEnemy([8, 1]), StrongMovingEnemy([9, 2]),
                   StrongMovingEnemy([10, 3])])
        for i in range(-3, 0):
            co[i].start()
        stage += 0.1

    if stage == 8:
        co.extend([SemiBoss2([9, 3]), MovingShootingEnemy([8, 2], 2), MovingShootingEnemy([8, 3], 2),
                   MovingEnemy([9, 1]), MovingEnemy([9, 5]), MovingEnemy([10, 1]), MovingEnemy([10, 5])])
        for i in range(-7, 0):
            co[i].start()
        stage += 0.1

    if stage == 9:
        co.extend([TeleportingShootingEnemy([9, 1]), TeleportingShootingEnemy([10, 5])])
        for i in range(-2, 0):
            co[i].start()
        stage += 0.1

    if stage == 10:
        co.extend([Boss([10, 3]), TeleportingShootingEnemy([9, 3])])
        for i in range(-2, 0):
            co[i].start()
        stage += 0.1

    count += 1
