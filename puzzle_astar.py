import pygame
import cv2
import random
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import heapq

pygame.init()

click_sound = pygame.mixer.Sound("Effect/aa.mp3")
over_sound = pygame.mixer.Sound("Effect/tt.mp3")

# 이미지 파일 로드
images = {
    1: 'images/1.PNG', 2: 'images/2.PNG', 3: 'images/3.PNG',
    4: 'images/4.PNG', 5: 'images/5.PNG', 6: 'images/6.PNG',
    7: 'images/7.PNG', 8: 'images/8.PNG', 0: 'images/0.PNG'
}

imgList = [images[1], images[2], images[3], images[4], images[5], images[6], images[7], images[8], images[0]]

# 이미지를 랜덤하게 섞는 함수
def shuffle_image(image_list, shuffle_count):
    for _ in range(shuffle_count):
        empty_index = image_list.index('images/0.PNG')
        empty_row, empty_col = empty_index // 3, empty_index % 3

        # 빈 칸의 상하좌우 인접한 셀 중에서 랜덤하게 선택
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)

        for dr, dc in directions:
            new_row, new_col = empty_row + dr, empty_col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_index = new_row * 3 + new_col
                image_list[empty_index], image_list[new_index] = image_list[new_index], image_list[empty_index]
                empty_row, empty_col = new_row, new_col
                break

# A* 알고리즘 구현
def heuristic(state, goal):
    distance = 0
    for i in range(9):
        if state[i] != 'images/0.PNG':
            goal_index = goal.index(state[i])
            distance += abs(i // 3 - goal_index // 3) + abs(i % 3 - goal_index % 3)
    return distance

def get_neighbors(state):
    empty_index = state.index('images/0.PNG')
    empty_row, empty_col = empty_index // 3, empty_index % 3
    neighbors = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for dr, dc in directions:
        new_row, new_col = empty_row + dr, empty_col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_index = new_row * 3 + new_col
            new_state = state.copy()
            new_state[empty_index], new_state[new_index] = new_state[new_index], new_state[empty_index]
            neighbors.append(new_state)
    return neighbors

def a_star(start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {tuple(start): 0}
    f_score = {tuple(start): heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while tuple(current) in came_from:
                path.append(current)
                current = came_from[tuple(current)]
            path.reverse()
            return path

        for neighbor in get_neighbors(current):
            tentative_g_score = g_score[tuple(current)] + 1

            if tuple(neighbor) not in g_score or tentative_g_score < g_score[tuple(neighbor)]:
                came_from[tuple(neighbor)] = current
                g_score[tuple(neighbor)] = tentative_g_score
                f_score[tuple(neighbor)] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[tuple(neighbor)], neighbor))

    return None

# 퍼즐 상태 시각화 함수 정의
def draw_image(axes, state):
    for i in range(9):
        axes[i // 3][i % 3].clear()
        axes[i // 3][i % 3].imshow(cv2.imread(state[i]))
        axes[i // 3][i % 3].axis('off')
    click_sound.play()
    plt.draw()
    plt.pause(1)  # 시각화를 업데이트하기 위한 잠시의 지연



shuffle_count = 50
start_image = random.sample(imgList, 9)
empty_cell = (start_image.index(images[0]) // 3, start_image.index(images[0]) % 3)
target = start_image.copy()
shuffle_image(target, shuffle_count)

# 시작 상태와 목표 상태 출력
fig, axes_start = plt.subplots(3, 3, figsize=(5, 5))
plt.suptitle("Game Image")

draw_image(axes_start, start_image)

fig2, axes_target = plt.subplots(3, 3, figsize=(5, 5))
plt.suptitle("Target Image")

draw_image(axes_target, target)

# A* 알고리즘을 사용하여 퍼즐을 풀어가며 각 단계마다 시각화
solution_path = a_star(start_image, target)

if solution_path:
    for state in solution_path:
        draw_image(axes_start, state)
    over_sound.play()
    plt.figure(1)
    plt.figtext(0.5, 0.90, "Game Clear!", fontsize=12, color='red', ha='center')
else:
    print("No solution found")

plt.show()  # 모든 figure를 화면에 표시