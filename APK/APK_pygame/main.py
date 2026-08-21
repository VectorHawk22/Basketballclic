import os
import sys
import pygame

# Добавляем путь к текущей директории
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Импортируем главный GUI класс
from allgui_apk import AllGUI, main as gui_main


def main():
    """Главная точка входа в приложение"""
    print("🏀 Запуск Clicker Basketball...")
    
    # Инициализация Pygame
    pygame.init()
    
    # Запуск GUI
    gui_main()


if __name__ == "__main__":
    main()