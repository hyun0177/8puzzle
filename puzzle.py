import pygame
import cv2
import random
import numpy as np
import matplotlib.pyplot as plt
import pyautogui

pygame.init()

click_sound = pygame.mixer.Sound("Effect/aa.mp3")
over_sound = pygame.mixer.Sound("Effect/tt.mp3")
# 이미지 리스트 선언
images = {
    1: 'images/1.PNG', 2: 'images/2.PNG', 3: 'images/3.PNG',
    4: 'images/4.PNG', 5: 'images/5.PNG', 6: 'images/6.PNG',
    7: 'images/7.PNG', 8: 'images/8.PNG', 0: 'images/0.PNG'
}

# 목표 이미지 선언
imgList = [images[1], images[2], images[3], images[4], images[5], images[6], images[7], images[8], images[0]]

# 이미지를 랜덤하게 섞는 함수
def shuffle_image(image_list, shuffle_count):
    for _ in range(shuffle_count):
        empty_index = image_list.index(images[0])
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

# 이미지를 랜덤하게 섞음 (횟수는 사용자 정의)
shuffle_count = 3
start_image = random.sample(imgList, 9)
empty_cell = (start_image.index(images[0]) // 3, start_image.index(images[0]) % 3)
target = start_image.copy()
shuffle_image(target, shuffle_count)

# 그리드 생성
fig, axes = plt.subplots(3, 3, figsize=(5, 5))
plt.suptitle("Game Image")
# 서브플롯에 이미지 표시
for i in range(9):
    plt.subplot(3, 3, i + 1)
    plt.gca().axes.xaxis.set_visible(False)
    plt.gca().axes.yaxis.set_visible(False)
    plt.imshow(cv2.imread(start_image[i]))


def add_point(event):
    global empty_cell
    if event.button == 1:
        click_sound.play()
        fore = pyautogui.getActiveWindow()
        pos = pyautogui.position()
        x = pos.x - fore.left
        y = pos.y - fore.top
        print("Ŭ   : ", x, ", ", y)

        # 클릭한 위치에 해당하는 셀 좌표 계산
        clicked_cell = (int((y - 95) / 130), int((x - 75) / 130))

        # 클릭한 위치가 빈 칸 주변의 셀 중 하나인지 확인
        if abs(clicked_cell[0] - empty_cell[0]) + abs(clicked_cell[1] - empty_cell[1]) == 1:
            # 이미지 교환
            start_image[empty_cell[0] * 3 + empty_cell[1]], start_image[clicked_cell[0] * 3 + clicked_cell[1]] = \
                start_image[clicked_cell[0] * 3 + clicked_cell[1]], start_image[empty_cell[0] * 3 + empty_cell[1]]
            empty_cell = clicked_cell  # 빈 칸 좌표 업데이트

            # 서브플롯에 이미지 업데이트
            for i in range(9):
                axes[i // 3][i % 3].clear()
                axes[i // 3][i % 3].imshow(cv2.imread(start_image[i]))
                axes[i // 3][i % 3].axis('off')
            plt.draw()


            if start_image == target:
                plt.figtext(0.5, 0.90, "Game Clear!", fontsize=12, color='red', ha='center')
                plt.draw()
                plt.disconnect(cid)
                over_sound.play()

cid = plt.connect('button_press_event', add_point)

# 서브플롯 간 간격 조정
plt.subplots_adjust(wspace=0.01, hspace=0.02)

fig2 = plt.figure(figsize=(5, 5))
plt.suptitle("Target Image")
for i in range(9):
    plt.subplot(3, 3, i + 1)
    plt.gca().axes.xaxis.set_visible(False)
    plt.gca().axes.yaxis.set_visible(False)
    plt.imshow(cv2.imread(target[i]))

# 플롯 표시
plt.show()
