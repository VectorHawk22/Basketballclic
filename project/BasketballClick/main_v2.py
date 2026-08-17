#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Импорт анимаций
from animation.court1 import CourtSuccess
from animation.court2 import CourtFail

# Установка размера окна
Window.size = (600, 450)


# Простая игровая логика
class SimpleGame:
    def __init__(self):
        self.points = 0
        self.potion_active = False
        self.potion_time = 0
        self.load_game()
    
    def load_game(self):
        print("Загрузка игры...")
    
    def save_game(self):
        print("Сохранение игры...")
    
    def get_points(self):
        return self.points
    
    def try_add_point(self, clicks):
        if clicks >= 3:
            self.points += 1
            return True, None
        return False, None
    
    def activate_potion(self):
        if not self.potion_active:
            self.potion_active = True
            self.potion_time = 600
            return True
        return False
    
    def is_potion_active(self):
        return self.potion_active
    
    def get_potion_time_left(self):
        return self.potion_time


class AnimationContainer(Widget):
    """Контейнер для анимаций"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.court_success = None
        self.court_fail = None
        
        # Инициализация анимаций после создания виджета
        Clock.schedule_once(self.init_animations, 0.1)
    
    def init_animations(self, dt):
        """Инициализация анимаций"""
        self.court_success = CourtSuccess(self)
        self.court_fail = CourtFail(self)
        self.draw_court()
    
    def draw_court(self):
        """Отрисовка площадки"""
        if self.court_success:
            self.court_success.draw_court()
    
    def start_success_animation(self):
        """Запуск анимации успеха"""
        if self.court_success:
            self.court_success.start_animation()
    
    def start_fail_animation(self):
        """Запуск анимации неудачи"""
        if self.court_fail:
            self.court_fail.start_animation()


class ClickerGUI(BoxLayout):
    """Главный интерфейс кликера"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Инициализация игры
        self.game = SimpleGame()
        
        # Переменные для челленджа
        self.click_count = 0
        self.challenge_active = False
        
        # Создание интерфейса
        self.build_ui()
        
        # Обновление очков
        Clock.schedule_interval(self.update_points, 0.5)
    
    def build_ui(self):
        """Создание интерфейса"""
        self.clear_widgets()
        
        # Основной контейнер
        main_container = BoxLayout(orientation='horizontal', spacing=10, padding=10)
        
        # Левая часть
        left_panel = BoxLayout(orientation='vertical', size_hint_x=0.75, spacing=5)
        
        # Контейнер для анимации
        self.anim_container = AnimationContainer(size_hint_y=0.6)
        left_panel.add_widget(self.anim_container)
        
        # Информационная панель
        info_panel = BoxLayout(orientation='vertical', size_hint_y=0.4, spacing=5)
        
        self.result_label = Label(
            text="Нажми кнопку, чтобы начать!",
            font_size=16,
            size_hint_y=0.3,
            color=(0, 0, 0, 1)
        )
        info_panel.add_widget(self.result_label)
        
        # Кнопка и очки
        button_row = BoxLayout(size_hint_y=0.7, spacing=10, padding=[10, 5, 10, 5])
        
        self.click_button = Button(
            text="НАЧАТЬ ЧЕЛЛЕНДЖ!",
            font_size=18,
            background_color=(0.3, 0.7, 1, 1),
            size_hint_x=0.7
        )
        self.click_button.bind(on_press=self.on_button_press)
        button_row.add_widget(self.click_button)
        
        self.points_label = Label(
            text=f"Очки: {self.game.get_points()}",
            font_size=20,
            bold=True,
            size_hint_x=0.3
        )
        button_row.add_widget(self.points_label)
        
        info_panel.add_widget(button_row)
        left_panel.add_widget(info_panel)
        
        # Правая панель с кнопками
        right_panel = BoxLayout(
            orientation='vertical',
            size_hint_x=0.25,
            spacing=5,
            padding=[5, 5, 5, 5]
        )
        
        buttons = [
            ("Инвентарь", self.open_inventory, (1, 0.6, 0.6, 1)),
            ("Магазин", self.open_shop, (0.6, 1, 0.6, 1)),
            ("Авторы", self.open_authors, (1, 1, 0.6, 1)),
            ("Язык", self.change_language, (0.6, 0.8, 1, 1)),
            ("Настройки", self.open_settings, (0.8, 0.8, 0.8, 1))
        ]
        
        for text, command, color in buttons:
            btn = Button(
                text=text,
                font_size=11,
                bold=True,
                size_hint_y=0.18,
                background_color=color
            )
            btn.bind(on_press=command)
            right_panel.add_widget(btn)
        
        main_container.add_widget(left_panel)
        main_container.add_widget(right_panel)
        
        self.add_widget(main_container)
    
    def on_button_press(self, instance):
        """Обработка нажатия на главную кнопку"""
        if not self.challenge_active:
            # Начинаем челлендж
            self.challenge_active = True
            self.click_count = 0
            self.click_button.text = "КЛИКАЙ!!!"
            self.click_button.background_color = (1, 0, 0, 1)
            self.result_label.text = "Кликай быстрее! У тебя 1 секунда!"
            self.result_label.color = (1, 0, 0, 1)
            
            # Завершаем через 1 секунду
            Clock.schedule_once(self.end_challenge, 1.0)
        else:
            # Регистрируем клик во время челленджа
            self.click_count += 1
    
    def end_challenge(self, dt):
        """Завершение челленджа"""
        self.challenge_active = False
        self.click_button.text = "НАЧАТЬ ЧЕЛЛЕНДЖ!"
        self.click_button.background_color = (0.3, 0.7, 1, 1)
        
        # Проверяем результат
        success, _ = self.game.try_add_point(self.click_count)
        
        if success:
            self.result_label.text = f"🎯 Попал! +1 очко! ({self.click_count} кликов)"
            self.result_label.color = (0, 1, 0, 1)
            # Останавливаем предыдущие анимации и запускаем новую
            if hasattr(self.anim_container, 'court_fail') and self.anim_container.court_fail:
                self.anim_container.court_fail.stop()
            if hasattr(self.anim_container, 'court_success') and self.anim_container.court_success:
                self.anim_container.court_success.stop()
                # Небольшая задержка перед запуском новой анимации
                Clock.schedule_once(lambda x: self.anim_container.start_success_animation(), 0.1)
        else:
            self.result_label.text = f"❌ Промах! ({self.click_count} кликов)"
            self.result_label.color = (1, 0, 0, 1)
            if hasattr(self.anim_container, 'court_success') and self.anim_container.court_success:
                self.anim_container.court_success.stop()
            if hasattr(self.anim_container, 'court_fail') and self.anim_container.court_fail:
                self.anim_container.court_fail.stop()
                Clock.schedule_once(lambda x: self.anim_container.start_fail_animation(), 0.1)
        
        # Обновляем очки
        self.update_points(dt)
    
    def update_points(self, dt):
        """Обновление отображения очков"""
        points = self.game.get_points()
        self.points_label.text = f"Очки: {points}"
    
    def open_inventory(self, instance):
        self.result_label.text = "📦 Инвентарь"
        self.result_label.color = (0.5, 0, 0.5, 1)
    
    def open_shop(self, instance):
        self.result_label.text = "🏪 Магазин временно закрыт"
        self.result_label.color = (1, 0.5, 0, 1)
    
    def open_authors(self, instance):
        self.result_label.text = "👨‍💻 Авторы: thekosmoss, artman, amonpys"
        self.result_label.color = (0, 0, 1, 1)
    
    def change_language(self, instance):
        self.result_label.text = "🌍 Язык: Русский"
        self.result_label.color = (0, 0.5, 0.5, 1)
    
    def open_settings(self, instance):
        self.result_label.text = "⚙️ Настройки в разработке"
        self.result_label.color = (0.5, 0.5, 0.5, 1)


class ClickerApp(App):
    """Главное приложение"""
    
    def build(self):
        self.title = "Кликер - Basketball Click"
        return ClickerGUI()
    
    def on_stop(self):
        """Сохранение при закрытии"""
        if hasattr(self.root, 'game'):
            self.root.game.save_game()
            print("Игра сохранена!")


if __name__ == '__main__':
    print("Запуск приложения...")
    ClickerApp().run()