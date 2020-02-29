# -*- coding: utf-8 -*-
import locale
import math
import os
import random
import sys
import time

import pygame
# import pygame.movie
from moviepy.editor import *
from pygame.locals import *
from textBox import ask


# 获得测试图片
def get_test_images(file_dir):
    L=[]   
    for root, dirs, files in os.walk(file_dir):  
        for file in files:  
            if os.path.splitext(file)[1] == '.jpg':  
                L.append(os.path.join(os.path.splitext(file)[0]))  
    return random.sample(L, 20)  # 随机


# 打印文字到窗口
def print_text(font, x, y, text, color=(0,0,0)):
    imgText = font.render(text, True, color)
    screen = pygame.display.get_surface() #req'd when function moved into MyLibrary
    screen.blit(imgText, (x,y))


#定义一个按钮类
class Button(object):
    def __init__(self, upimage, downimage,position):
        self.imageUp = pygame.image.load(upimage).convert_alpha()
        self.imageDown = pygame.image.load(downimage).convert_alpha()
        self.position = position
        self.game_start = False
        
    def isOver(self):
        point_x,point_y = pygame.mouse.get_pos()
        x, y = self. position
        w, h = self.imageUp.get_size()

        in_x = x - w/2 < point_x < x + w/2
        in_y = y - h/2 < point_y < y + h/2
        return in_x and in_y

    def render(self):
        w, h = self.imageUp.get_size()
        x, y = self.position
        
        if self.isOver():
            screen.blit(self.imageDown, (x-w/2,y-h/2))
        else:
            screen.blit(self.imageUp, (x-w/2, y-h/2))
    def is_start(self):
        if self.isOver():
            b1,b2,b3 = pygame.mouse.get_pressed()
            if b1 == 1:
                self.game_start = True
                bg_sound.play_pause()
                btn_sound.play_sound()
                bg_sound.play_sound()


def replay_music():
    bg_sound.play_pause()
    bg_sound.play_sound()


#定义一个控制声音的类和初始音频的方法
def media_init():
    global hit_au, btn_au, bg_au, bullent_au
    pygame.mixer.init()
    hit_au = pygame.mixer.Sound("sounds/exlposion.wav")   # 输入正确
    btn_au = pygame.mixer.Sound("sounds/button.wav")      # 按钮
    bg_au = pygame.mixer.Sound("sounds/background.ogg")   # 背景
    bullent_au = pygame.mixer.Sound("sounds/bullet.wav")  # 输入错误


class Music():
    def __init__(self,sound):
        self.channel = None
        self.sound = sound     
    def play_sound(self):
        self.channel = pygame.mixer.find_channel(True)
        self.channel.set_volume(0.5)
        self.channel.play(self.sound)
    def play_pause(self):
        self.channel.set_volume(0.0)
        self.channel.play(self.sound)

if __name__ == "__main__":
    #主程序部分
    pygame.init()
    media_init()
    screen = pygame.display.set_mode((750, 460),0,32)
    pygame.display.set_caption("Guess Hero")
    font = pygame.font.Font(None, 22)
    font1 = pygame.font.Font(None, 40)
    framerate = pygame.time.Clock()
    upImageFilename = 'images/game_start_up.png'
    downImageFilename = 'images/game_start_down.png'
    
    #创建按钮对象
    button = Button(upImageFilename,downImageFilename, (360,420))
    interface = pygame.image.load("images/bg01.jpg")


    #定义一些变量
    test_images = get_test_images("heroImages")
    print(test_images)

    game_over = False
    you_win = False
    global bg_sound, hit_sound, btn_sound, bullent_sound
    bg_sound = Music(bg_au)
    hit_sound = Music(hit_au)
    btn_sound = Music(btn_au)
    bullent_sound = Music(bullent_au)

    game_pause = False
    current_time = 0
    start_time = 0
    music_time = 0
    score = 0
    replay_flag = True
    s = 1

    #循环
    bg_sound.play_sound()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            pygame.quit()
            sys.exit()
                
        # screen.blit(interface,(0,0))
        screen.blit(pygame.transform.scale(interface, (750, 460)), (0, 0))
        button.render()
        button.is_start()
        if button.game_start == True:
            if game_pause:
                #判断游戏是否通关
                if score >= 10:
                    you_win = True
                if you_win:
                    screen.fill((200, 200, 200))
                    print_text(font1, 270, 150, "YOU WIN THE GAME!",(240,20,20))
                    current_time =time.clock()-start_time
                    print_text(font1, 320, 250, "Your Score:",(120,224,22))
                    print_text(font1, 370, 290, str(score),(255,0,0))
                    pygame.display.update()
                    time.sleep(1)
                    clip = VideoFileClip('videos/pass.mp4')
                    clip.preview()
                    pygame.quit()
                    sys.exit()
                else:
                    screen.fill((200, 200, 200))
                    print_text(font1, 300, 150,"GAME OVER!",(240,20,20))
                    current_time = time.clock()-start_time
                    print_text(font1, 280, 250, "This Game Score:",(0,122,204))
                    print_text(font1, 370, 290, str(score),(255,0,0))
                    pygame.display.update()
                    time.sleep(2)
                    clip = VideoFileClip('videos/gameover.mp4')
                    clip.preview()
                    pygame.quit()
                    sys.exit()
                
            else:
                screen.fill((0, 0, 0))      
                print_text(font, 125, 20, "You have get Score:", (219,224,22))
                print_text(font1, 280, 15, str(score), (255,0,0))
                    
                hero_name = test_images.pop().lower()
                hero_image = "heroImages/" + hero_name + ".jpg"
                image = pygame.image.load(hero_image)
                image = pygame.transform.scale(image, (500, 375))
                screen.blit(image, (120, 48))
                pygame.display.update()

                input_name = ask(screen, "Name").strip()

                print(input_name)
                if input_name == hero_name:
                    score += 1
                    bullent_sound.play_sound()
                else:
                    hit_sound.play_sound()                
                    # game_pause = True

                if score >= 10 or not test_images:
                    game_pause = True
                    
                #循环播放背景音乐
                music_time = time.clock()
                if music_time > 150 and replay_flag:
                    replay_music()
                    replay_flag =False

        pygame.display.update()
