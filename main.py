from tkinter import *
from random import randint
import random
from game_gui import DeadlyHotelGUI


window = Tk()
window.title("选项")

room_size_horizontal_MIN = 1
room_size_horizontal_MAX = 3
room_size_vertical_MIN = 1
room_size_vertical_MAX = 3
room_size_vertical_variable = IntVar()
room_size_vertical_variable.set(room_size_vertical_MIN)
room_size_horizontal_variable = IntVar()
room_size_horizontal_variable.set(room_size_horizontal_MIN)


def room_size_random():
    room_size_horizontal_variable.set(randint(room_size_horizontal_MIN, room_size_horizontal_MAX))
    room_size_vertical_variable.set(randint(room_size_vertical_MIN, room_size_vertical_MAX))


Label(window, text="客房大小").grid(row=0, column=0, rowspan=2)
room_size_horizontal_scale = Scale(window, label='横', from_=room_size_horizontal_MIN, to=room_size_horizontal_MAX,
                                   tickinterval=1, orient=HORIZONTAL, variable=room_size_horizontal_variable)
room_size_horizontal_scale.grid(row=0, column=1)
room_size_vertical_scale = Scale(window, label='纵', from_=room_size_vertical_MIN, to=room_size_vertical_MAX,
                                 tickinterval=1, orient=HORIZONTAL, variable=room_size_vertical_variable)
room_size_vertical_scale.grid(row=1, column=1)
Button(window, text="随机", command=room_size_random).grid(row=0, column=2, rowspan=2)


store_size_horizontal_MIN = 3
store_size_horizontal_MAX = 5
store_size_vertical_MIN = 2
store_size_vertical_MAX = 4
store_size_vertical_variable = IntVar()
store_size_vertical_variable.set(store_size_vertical_MIN)
store_size_horizontal_variable = IntVar()
store_size_horizontal_variable.set(store_size_horizontal_MIN)


def store_size_random():
    store_size_horizontal_variable.set(randint(store_size_horizontal_MIN, store_size_horizontal_MAX))
    store_size_vertical_variable.set(randint(store_size_vertical_MIN, store_size_vertical_MAX))


Label(window, text="储物间大小").grid(row=0, column=3, rowspan=2)
store_size_horizontal_scale = Scale(window, label='横', from_=store_size_horizontal_MIN, to=store_size_horizontal_MAX,
                                    tickinterval=1, orient=HORIZONTAL, variable=store_size_horizontal_variable)
store_size_horizontal_scale.grid(row=0, column=4)
store_size_vertical_scale = Scale(window, label='纵', from_=store_size_vertical_MIN, to=store_size_vertical_MAX,
                                  tickinterval=1, orient=HORIZONTAL, variable=store_size_vertical_variable)
store_size_vertical_scale.grid(row=1, column=4)
Button(window, text="随机", command=store_size_random).grid(row=0, column=5, rowspan=2)


npc_num_MIN = 1
npc_num_MAX = 4
npc_num_variable = IntVar()
npc_num_variable.set(npc_num_MIN)


def npc_num_change(value):
    global room_num_MAX, room_num_MIN, room_num_variable, room_num_scale
    room_num_MIN = npc_num_variable.get() + victim_num_variable.get() + 1
    room_num_MAX = npc_num_variable.get() + victim_num_variable.get() + 3
    room_num_scale['from_'] = room_num_MIN
    room_num_scale['to'] = room_num_MAX
    room_num_variable.set(room_num_MIN)
    global store_num_MAX, store_num_MIN, store_num_variable, store_num_scale
    store_num_MIN = npc_num_variable.get() + 1
    store_num_MAX = npc_num_variable.get() + 3
    store_num_scale['from_'] = store_num_MIN
    store_num_scale['to'] = store_num_MAX
    store_num_variable.set(store_num_MIN)


def npc_num_random():
    value = randint(npc_num_MIN, npc_num_MAX)
    npc_num_variable.set(value)
    npc_num_change(value)


Label(window, text="NPC人数").grid(row=2, column=0)
Scale(window, label='', from_=npc_num_MIN, to=npc_num_MAX, variable=npc_num_variable, orient=HORIZONTAL, tickinterval=1,
      command=npc_num_change).grid(row=2, column=1)
Button(window, text="随机", command=npc_num_random).grid(row=2, column=2)


victim_num_MIN = 1
victim_num_MAX = 3
victim_num_variable = IntVar()
victim_num_variable.set(victim_num_MIN)


def victim_num_change(value):
    global room_num_MAX, room_num_MIN, room_num_variable, room_num_scale
    room_num_MIN = npc_num_variable.get() + int(value) + 1
    room_num_MAX = npc_num_variable.get() + int(value) + 3
    room_num_scale['from_'] = room_num_MIN
    room_num_scale['to'] = room_num_MAX
    room_num_variable.set(room_num_MIN)


def victim_num_random():
    value = randint(victim_num_MIN, victim_num_MAX)
    victim_num_variable.set(value)
    victim_num_change(value)


Label(window, text="受害者人数").grid(row=2, column=3)
Scale(window, label='', from_=victim_num_MIN, to=victim_num_MAX, variable=victim_num_variable, orient=HORIZONTAL,
      tickinterval=1, command=victim_num_change).grid(row=2, column=4)
Button(window, text="随机", command=victim_num_random).grid(row=2, column=5)


room_num_MIN = npc_num_variable.get() + victim_num_variable.get() + 1
room_num_MAX = npc_num_variable.get() + victim_num_variable.get() + 3
room_num_variable = IntVar()
room_num_variable.set(room_num_MIN)


def room_num_random():
    room_num_variable.set(randint(room_num_MIN, room_num_MAX))


Label(window, text="客房数量").grid(row=3, column=0)
room_num_scale = Scale(window, label='', from_=room_num_MIN, to=room_num_MAX, variable=room_num_variable,
                       orient=HORIZONTAL, tickinterval=1)
room_num_scale.grid(row=3, column=1)
Button(window, text="随机", command=room_num_random).grid(row=3, column=2)


store_num_MIN = npc_num_variable.get() + 1
store_num_MAX = npc_num_variable.get() + 3
store_num_variable = IntVar()
store_num_variable.set(store_num_MIN)


def store_num_random():
    store_num_variable.set(randint(store_num_MIN, store_num_MAX))


Label(window, text="储物间数量").grid(row=3, column=3)
store_num_scale = Scale(window, label='', from_=store_num_MIN, to=store_num_MAX, variable=store_num_variable,
                        orient=HORIZONTAL, tickinterval=1)
store_num_scale.grid(row=3, column=4)
Button(window, text="随机", command=store_num_random).grid(row=3, column=5)


turn_num_MIN = 20
turn_num_MAX = 50
turn_num_variable = IntVar()
turn_num_variable.set(turn_num_MIN)


def turn_num_random():
    turn_num_variable.set(randint(turn_num_MIN, turn_num_MAX))


Label(window, text="回合数").grid(row=4, column=0)
turn_num_scale = Scale(window, label='', from_=turn_num_MIN, to=turn_num_MAX, variable=turn_num_variable,
                       orient=HORIZONTAL, tickinterval=10)
turn_num_scale.grid(row=4, column=1)
Button(window, text="随机", command=turn_num_random).grid(row=4, column=2)


mode_variable = BooleanVar()
mode_variable.set(False)


def mode_random():
    mode_variable.set(random.choice([True, False]))


Label(window, text="游玩").grid(row=4, column=3)
frame = Frame(window)
Radiobutton(frame, text="AI", variable=mode_variable, value=True).pack(side=LEFT)
Radiobutton(frame, text="真人", variable=mode_variable, value=False).pack(side=LEFT)
frame.grid(row=4, column=4)
Button(window, text="随机", command=mode_random).grid(row=4, column=5)


ai_step_num_variable = IntVar()
ai_step_num_variable.set(500)

Label(window, text="AI模拟次数").grid(row=5, column=0)
Entry(window, textvariable=ai_step_num_variable, justify=RIGHT).grid(row=5, column=1)
Label(window, text="次").grid(row=5, column=2)


ai_delay_variable = IntVar()
ai_delay_variable.set(500)

Label(window, text="AI行动延迟").grid(row=5, column=3)
Entry(window, textvariable=ai_delay_variable, justify=RIGHT).grid(row=5, column=4)
Label(window, text="ms").grid(row=5, column=5)


def start_game():
    config = {
        'room_size': (room_size_horizontal_variable.get(), room_size_vertical_variable.get()),
        'store_size': (store_size_horizontal_variable.get(), store_size_vertical_variable.get()),
        'npc_num': npc_num_variable.get()+1,
        'victim_num': victim_num_variable.get(),
        'room_num': room_num_variable.get(),
        'store_num': store_num_variable.get(),
        'turn_num': turn_num_variable.get(),
        'mode': mode_variable.get(),
        'ai_step_num': ai_step_num_variable.get(),
        'ai_delay': ai_delay_variable.get(),
        'map': 'random'
    }
    global window
    window.destroy()
    gui = DeadlyHotelGUI(config)
    gui.init()
    gui.loop()
    gui.finish()


def start_game1():
    config = {
        'room_size': (room_size_horizontal_variable.get(), room_size_vertical_variable.get()),
        'store_size': (store_size_horizontal_variable.get(), store_size_vertical_variable.get()),
        'npc_num': npc_num_variable.get()+1,
        'victim_num': victim_num_variable.get(),
        'room_num': room_num_variable.get(),
        'store_num': store_num_variable.get(),
        'turn_num': turn_num_variable.get(),
        'mode': mode_variable.get(),
        'ai_step_num': ai_step_num_variable.get(),
        'ai_delay': ai_delay_variable.get(),
        'map': 'flood'
    }
    global window
    window.destroy()
    gui = DeadlyHotelGUI(config)
    gui.init()
    gui.loop()
    gui.finish()


Button(window, text='随机地图 进入游戏', command=start_game).grid(row=10, column=0, columnspan=3)
Button(window, text='洪水法 进入游戏', command=start_game1).grid(row=10, column=3, columnspan=3)

window.mainloop()

