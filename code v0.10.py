from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview import RecycleView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.config import ConfigParser
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.metrics import dp
from datetime import datetime
from kivy.uix.popup import Popup
import os
import ast
import time
from kivy.uix.checkbox import CheckBox

money = int(20)
# Builder.load_file('kivi.kv')

class Menu(Screen):
    def __init__(self, **kw):
        super(Menu, self).__init__(**kw)
        grid = GridLayout(cols = 2)
        grid.add_widget(Button(text='Список Квестов', on_press=lambda x: set_screen('list'),
                               background_normal = ('oldbook.jpg')))
        grid.add_widget(Button(text='Создать квест', on_press=lambda x: set_screen('add_task'),
                               background_normal = ('write.jpg')))
        grid.add_widget(Button(text='Магазин', on_press=lambda x: set_screen('shop'),
                               background_normal = ('shop.jpg')))
        grid.add_widget(Button(text='О персонаже', on_press=lambda x: set_screen('stat'),
                               background_normal = ('knight2.png')))
        self.add_widget(grid)


class ListComand(Screen):
    def __init__(self, **kw):
        super(ListComand, self).__init__(**kw)

    def on_enter(self):  # Будет вызвана в момент открытия экрана

        self.layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        back_button = Button(text='< Обратно, в главное меню',
                             on_press=lambda x: set_screen('menu'),
                             size_hint_y=None, height=dp(40))
        self.layout.add_widget(back_button)
        root = RecycleView(size_hint=(1, None), size=(Window.width,
                                                      Window.height))
        root.add_widget(self.layout)
        self.add_widget(root)

        dic_foods = ast.literal_eval(
            App.get_running_app().config.get('General', 'user_data'))

        for f, d in sorted(dic_foods.items(), key=lambda x: x[1]):
            global money
            fd = f.decode('u8') + ' ' + (datetime.fromtimestamp(d).strftime('%Y-%m-%d'))
            btn = Button(text=fd, size_hint_y=None, height=dp(40), on_press = self.marktask)
            self.check = CheckBox(active=False)  # Checkbox-ы, чтобы отмечать задания
            self.layout.add_widget(btn)
            self.layout.add_widget(self.check)

    def marktask(self, btn):
        global money
        if self.check.active == True:
            money += 10
    def on_leave(self):  # Будет вызвана в момент закрытия экрана

        self.layout.clear_widgets()  # очищаем список

class AddTask(Screen):

    def buttonClicked(self, btn1):
        if not self.txt1.text:
            return
        self.app = App.get_running_app()
        self.app.user_data = ast.literal_eval(
            self.app.config.get('General', 'user_data'))
        self.app.user_data[self.txt1.text.encode('u8')] = int(time.time())

        self.app.config.set('General', 'user_data', self.app.user_data)
        self.app.config.write()

        text = "Последний добавленный квест:  " + self.txt1.text
        self.result.text = text
        self.txt1.text = ''

    def __init__(self, **kw):
        super(AddTask, self).__init__(**kw)
        box = BoxLayout(orientation='vertical')
        back_button = Button(text='< Назад в главное меню', on_press=lambda x: set_screen('menu'), size_hint_y=None, height=dp(40))
        box.add_widget(back_button)
        self.txt1 = TextInput(text='', multiline=False, height=dp(40),
                              size_hint_y=None, hint_text="Название квеста")
        box.add_widget(self.txt1)
        btn1 = Button(text="Добавить квест", size_hint_y=None, height=dp(40))
        btn1.bind(on_press=self.buttonClicked)
        box.add_widget(btn1)
        self.result = Label(text='')
        box.add_widget(self.result)
        self.add_widget(box)


class Shop(Screen):

    def __init__(self, **kw):
        super(Shop, self).__init__(**kw)

        box = BoxLayout(orientation='vertical')
        back_button = Button(text='< Назад в главное меню', on_press=lambda x: set_screen('menu'),
                             size_hint_y=None, height=dp(40))
        box.add_widget(back_button)

        box2 = BoxLayout(orientation='horizontal')

        xbox = Button(text='2 часа в XBOX', on_press=self.money_count)
        box2.add_widget(xbox)
        ice = Button(text='Мороженное', on_press=self.money_count)
        box2.add_widget(ice)

        self.add_widget(box2)
        self.add_widget(box)

    def money_count(self, xbox):

        self.popda = Popup(title='Уведомление', content=Label(text='Вы купили предмет'), size_hint=(None, None),
                           size=(400, 400))
        self.popnet = Popup(title='Уведомление', content=Label( text='Недостаточно монет. Выполните несколько заданий, чтобы заработать монеты.'),
                            size_hint=(None, None), size=(400, 400))
        global money
        if money >= 10:
            self.popda.open()
            money -= 10
        else:
            self.popnet.open()

class Stats(Screen):
    def __init__(self, **kw):
        super(Stats, self).__init__(**kw)
        box2 = BoxLayout(orientation='vertical')
        back_button = Button(text='< Назад в главное меню', on_press=lambda x: set_screen('menu'),
                             size_hint_y=None, height=dp(40))
        box2.add_widget(back_button)

        box = GridLayout(cols=2)
        btn1 = Button(text="Мой кошелек", on_press = self.Money)
        box.add_widget(btn1)
        btn2 = Button(text="Опыт моего героя", on_press = self.Points)
        box.add_widget(btn2)
        self.add_widget(box)
        self.add_widget(box2)
    def Money(self, pop):
        global money
        pop = Popup(title='Уведомление', content=Label(text='У Вас на счету ' + str(money) + ' монет'), size_hint=(None, None), size=(400, 400))
        pop.open()

    def Points(self, pop): # Опыт - нафиг он нужен сейчас?!
        pop = Popup(title='Уведомление', content=Label(text='Ваш персонаж имеет ...'), size_hint=(None, None), size=(400, 400))
        pop.open()

def set_screen(name_screen):
    sm.current = name_screen

sm = ScreenManager()
sm.add_widget(Menu(name='menu'))
sm.add_widget(ListComand(name='list'))
sm.add_widget(AddTask(name='add_task'))
sm.add_widget(Shop(name='shop'))
sm.add_widget(Stats(name='stat'))

class MyApp(App):
    def __init__(self, **kvargs):
        super(MyApp, self).__init__(**kvargs)
        self.config = ConfigParser()

    def build_config(self, config):
        config.adddefaultsection('General')
        config.setdefault('General', 'user_data', '{}')

    def set_value_from_config(self):
        self.config.read(os.path.join(self.directory, '%(appname)s.ini'))
        self.user_data = ast.literal_eval(self.config.get(
            'General', 'user_data'))

    def get_application_config(self):
        return super(MyApp, self).get_application_config(
            '{}/%(appname)s.ini'.format(self.directory))

    def build(self):
        return sm

if __name__ == '__main__':
    MyApp().run()