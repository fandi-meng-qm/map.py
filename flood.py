import random
import numpy as np
from matplotlib import pyplot as plt


def randomRoom(M, room_num):
    height, width, d = M.shape
    min_size = 3
    max_size = 3
    # room_num = 10
    count = 0
    try_count = 0
    room = []
    while count < room_num:
        if try_count > 10000:
            raise Exception('洪水法失败，没能将所有房间放进去')
        r = random.randint(min_size, max_size)
        c = random.randint(min_size, max_size)
        left = random.randint(2, width - 3)
        top = random.randint(2, height - 3)
        f = True
        for i in range(top-1,top+r+2):
            for j in range(left-1,left+c+2):
                if i >= height-2 or j >= width-2:
                    f = False
                    break
                if M[i,j,5] == 1:
                    f = False
                    break
        if f:
            room.append([left,top,c,r])
            for i in range(top, top + r + 1):
                for j in range(left, left + c + 1):
                    if i >= height-2 or j >= width-2:
                        continue
                    M[i,j,:] = 1
            count += 1
        try_count += 1
    return room


def randomDoor(map,room_list):
    for it in room_list:
        door_num = random.randint(1,3)
        for _ in range(door_num):
            door_x,door_y = randomWall(it)
            if _ == 0:
                for i in range(it[3]+1):
                    map[it[1]+i, it[0], 5] = 3
                    map[it[1]+i, it[0]+it[2], 5] = 3
                for i in range(it[2]+1):
                    map[it[1], it[0]+i, 5] = 3
                    map[it[1]+it[3], it[0]+i, 5] = 3
            map[door_x,door_y,5] = 2


def randomWall(room):
    direction = random.randint(0,3)
    dir = [[0,1,-1,0],[1,0,0,-1],[1,0,0,room[3]],[0,1,room[2],0]]
    x_off = random.randint(1,room[2]-2)
    y_off = random.randint(1,room[3]-2)
    x = room[0] + x_off*dir[direction][0] #+ dir[direction][2]
    y = room[1] + y_off*dir[direction][1] #+ dir[direction][3]
    return y,x


def drawMap(M, image):
    rows, cols, deep = M.shape
    block = [[2,8,0,2],[0,2,2,8],[2,8,8,10],[8,10,2,8]]
    color = [0,0,230,140,50,50,50,50,50,50]
    for row in range(0, rows):
        for col in range(0, cols):
            unit = M[row, col]
            if unit[5] == 1:
                image[10 * row : 10 * row + 10, 10 * col:10 * col + 10] = 255
            else:
                image[10 * row + 2: 10 * row + 8, 10 * col + 2:10 * col + 8] = 255 - color[unit[5]]
            for i in range(4):
                if unit[i] == 1:
                    x1 = 10 * row + block[i][0]
                    x2 = 10 * row + block[i][1]
                    y1 = 10 * col + block[i][2]
                    y2 = 10 * col + block[i][3]
                    image[x1:x2,y1:y2] = 255 - color[unit[5]]
    plt.subplot(2,1,1)
    plt.imshow(image, interpolation='none', cmap ='gray')
    # plt.show()


def floodFill(M):
    h, w, d = M.shape
    area = 4
    area_list = []

    def findFree():
        for i1 in range(1,h-1):
            for j1 in range(1,w-1):
                if M[i1,j1,5] == 0:
                    return [i1,j1]
        return None

    def outRect(p):
        return p[0] < 1 or p[0] >= h-1 or p[1] < 1 or p[1] >= w-1

    direction = [[0, -1], [-1, 0], [0, 1], [1, 0]]
    corner = []
    while True:
        new_point = point = findFree()
        if point is None:
            break
        dir = random.randint(0, 3)
        while True:
            point = new_point
            M[point[0], point[1], 5] = area
            M[point[0], point[1], 4] = 1

            change = random.random()
            old_dir = dir
            if change > 0.9:
                tran = int((random.randint(-1,0)+0.5)*2)
                old_dir = dir
                dir = (dir + tran) % 4

            new_point = [point[0]+direction[dir][0], point[1]+direction[dir][1]]
            f = False
            if outRect(new_point):
                f = True
            elif M[new_point[0],new_point[1],4] == 1:
                f = True
            if f:
                for i in range(4):
                    ind = (old_dir + i) % 4
                    temp = [point[0]+direction[ind][0], point[1]+direction[ind][1]]
                    if outRect(temp):
                        continue
                    elif M[temp[0],temp[1],4] == 1:
                        continue
                    else:
                        new_point = temp
                        f = False
                        dir = ind
            if old_dir != dir and not f:
                corner.append(point)
            if not f:
                M[point[0],point[1],dir] = 1
                M[new_point[0],new_point[1],(dir+2)%4] = 1
            else:
                if len(corner):
                    new_point = corner.pop()
                else:
                    break
        area_list.append(area)
        area += 1
    return area_list


#打通区域,ls存放area的列表
def breakArea(map,ls):
    h,w,d = map.shape
    known = []
    direction = [[0,-1],[-1,0],[0,1],[1,0]]
    while len(ls) > 1:
        f = False
        for i in range(h):
            for j in range(w):
                if map[i,j,5] in ls and not map[i,j,5] in known:
                    ind = 0
                    for it in direction:
                        if map[i+it[0],j+it[1],5] in ls and map[i+it[0],j+it[1],5] != map[i,j,5]:
                            ls.remove(map[i+it[0],j+it[1],5])
                            map[i, j, ind] = 1
                            map[i+it[0], j+it[1], (ind + 2) % 4] = 1
                            map[map==map[i+it[0],j+it[1],5]] = map[i, j, 5]
                            known.append(map[i,j,5])
                            known.append(map[i+it[0],j+it[1],5])
                            f = True
                            break
                        ind += 1
                if f:
                    break
            if f:
                break


def convert(map):
    rows = map.shape[0]*2-3
    columns = map.shape[1]*2-3
    newmap = []
    for r in range(rows):
        _ = []
        for c in range(columns):
            _.append('W')
        newmap.append(_)
    for r in range(1, map.shape[0]-1):
        for c in range(1, map.shape[1]-1):
            row = 2*(r-1)+1
            col = 2*(c-1)+1
            if map[r,c,5] == 1:
                newmap[row][col] = 'R'
                newmap[row][col + 1] = 'R'
                newmap[row + 1][col] = 'R'
                newmap[row + 1][col + 1] = 'R'
            if map[r, c, 5] == 2:
                newmap[row][col] = 'D'
                if map[r,c+1,5] != 4:
                    newmap[row][col+1] = 'R'
                if map[r+1,c,5] != 4:
                    newmap[row+1][col] = 'R'
                if map[r, c + 1, 5] != 4 and map[r+1,c,5] != 4:
                    newmap[row + 1][col + 1] = 'R'
            if map[r, c, 5] == 3:
                newmap[row][col] = 'R'
                if map[r,c+1,5] != 4:
                    newmap[row][col+1] = 'R'
                if map[r+1,c,5] != 4:
                    newmap[row+1][col] = 'R'
                if map[r, c + 1, 5] != 4 and map[r+1,c,5] != 4:
                    newmap[row + 1][col + 1] = 'R'
            if map[r,c,5] >= 4:
                newmap[row][col] = 'C'
                if map[r,c,2] == 1:
                    newmap[row][col+1] = 'C'
                else:
                    newmap[row][col+1] = 'W'
                if map[r,c,3] == 1:
                    newmap[row+1][col] = 'C'
                else:
                    newmap[row+1][col] = 'W'
    for r in range(1, len(newmap)):
        for c in range(1, len(newmap[0])):
            if newmap[r][c] == 'D':
                newmap[r][c] = 'R'
                if newmap[r-1][c] == 'W':
                    newmap[r-1][c] = 'D'
                if newmap[r+1][c] == 'W':
                    newmap[r+1][c] = 'D'
                if newmap[r][c-1] == 'W':
                    newmap[r][c-1] = 'D'
                if newmap[r][c+1] == 'W':
                    newmap[r][c+1] = 'D'
            if newmap[r][c] == 'R':
                if newmap[r-1][c] == 'R' and newmap[r+1][c] == 'C':
                    newmap[r][c] = 'W'
                if newmap[r][c-1] == 'R' and newmap[r][c+1] == 'C':
                    newmap[r][c] = 'W'
                if newmap[r][c+1] != 'R' and newmap[r+1][c] == 'C':
                    newmap[r][c] = 'W'
    for r in range(1, len(newmap)):
        for c in range(1, len(newmap[0])):
            if newmap[r][c] == 'D':
                walls = 0
                if newmap[r-1][c] == 'W':
                    walls += 1
                if newmap[r+1][c] == 'W':
                    walls += 1
                if newmap[r][c+1] == 'W':
                    walls += 1
                if newmap[r][c-1] == 'W':
                    walls += 1
                if walls != 2:
                    newmap[r][c] = 'R'
            if newmap[r][c] == 'R':
                walls = 0
                if newmap[r-1][c] == 'W':
                    walls += 1
                if newmap[r+1][c] == 'W':
                    walls += 1
                if newmap[r][c+1] == 'W':
                    walls += 1
                if newmap[r][c-1] == 'W':
                    walls += 1
                if walls == 3:
                    newmap[r][c] = 'W'

    return newmap


def drawNewMap(map):
    image = np.zeros((len(map) * 10, len(map[0]) * 10), dtype=np.uint8)
    colors = {
        'W': 0,
        'C': 255,
        'R': 100,
        'D': 200
    }
    for row in range(0, len(map)):
        for col in range(0, len(map[0])):
            image[10 * row: 10 * row + 10, 10 * col:10 * col + 10] = colors[map[row][col]]
    plt.subplot(2, 1, 2)
    plt.imshow(image, interpolation='none', cmap='gray')


def generate(config):
    # rows = int(input('输⼊房间⾏数：'))
    # cols = int(input('输⼊房间列数：'))
    room_num = config['room_num'] + config['store_num']
    rows = int(np.sqrt(4*4*room_num))+5
    cols = int(np.sqrt(4*4*room_num)*4)+5
    map = np.zeros((rows,cols,6),np.int16)
    image = np.zeros((rows * 10, cols * 10), dtype=np.uint8)

    while True:
        try:
            room = randomRoom(map, room_num)
            break
        except Exception as e:
            print(e)
            pass
    randomDoor(map, room.copy())
    ls = floodFill(map)
    breakArea(map, ls)
    # print(map[:, :, 5])
    newmap = convert(map)
    # print(np.array(newmap))

    # drawMap(map, image)
    # drawNewMap(newmap)
    # plt.show()
    roomss = []
    for _ in range(len(room)):
        roomss.append([room[_][1]*2+1, room[_][0]*2+1])
    rooms = roomss[:config['room_num']]
    stores = roomss[config['room_num']:]
    return newmap, rooms, stores, len(newmap), len(newmap[0])


if __name__ == '__main__':
    generate({
        'room_num': 3,
        'store_num': 2
    })