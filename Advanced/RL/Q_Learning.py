import sys

sys.path.append("../")
sys.path.append("../../")

from pprint import pprint
from Core.maze import Maze, INF

import random
import numpy as np

from helper import get_next_state, get_valid_actions
from policy import e_greedy
from reward import reward

N = M = 8
ACTIONS = [0, 1, 2, 3]
DISCOUNT = 0.8
LEARNING_RATE = 0.5
ACTION_MAPPER = {
        0: 'N',
        1: 'S',
        2: 'W',
        3: 'E'
    }

def load_maze():
    global maze 
    maze = Maze()
    maze.load(f"BinaryTree_{N}x{M}.maze")

def reset_q_table():
    """
    initialises/resets the q table
    """
    # setup the q table
    global q_table
    q_table = []

    for i in range(N):
        for j in range(M):
            temp = []
            for value in maze.grid[i][j].neighbors.values():
                if value == INF:
                    temp.append(-10000)
                else:
                    # temp.append(round(random.random(), 3))
                    temp.append(10)
            q_table.append(temp)

def print_q_table():
    for i in range(N*M):
        print(q_table[i], end="\t")
        if not (i+1) % N:
            print()

def visualise_q_table():
    for i in range(N*M):
        print(action_dict[np.argmax(q_table[i])], end="\t")
        if not (i+1) % N:
            print()

def get_path():
    i = N*M-2
    path = [i]
    visited = set()
    while i:
        temp = []
        for action, value in enumerate(q_table[i]):
            temp.append((value, action))
        temp.sort()
        for item in temp:
            try:
                new_state = get_next_state(maze, i, item[1])
        
                if new_state not in visited:
                    i = new_state
                    path.append(i)
                    break
            except:
                continue

    return path

def Q(state, action):
    return q_table[state][action]

def execute_episode():
    for state in range(N*M):
        action = e_greedy(
            state, 
            get_valid_actions(maze, state, ACTIONS), 
            Q, epsilon=0.1)
        R = reward(maze, state)
        next_state = get_next_state(maze, state, action)
        
        next_best = max(q_table[next_state])
        
        td_target = R + DISCOUNT * next_best
        td_diff = td_target - q_table[state][action]
        
        q_table[state][action] += LEARNING_RATE * td_diff        
        q_table[state][action] = round(q_table[state][action], 3)

if __name__ == "__main__":
    load_maze()
    reset_q_table()
    for _ in range(100):
        execute_episode()
    print_q_table()
    visualise_q_table()
    # print("PATH: ", get_path())