# 判定AI
"""
killed
    [0, 6, weapon_code, x, y, turn]
meet
    [1, role1_code, role2_code, x, y, turn]
"""
import os
import pickle

files = os.listdir('records')
for file in files:
    with open('records/'+file, 'rb') as f:
        data = pickle.load(f)
        print(data)
