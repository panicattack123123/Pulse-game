init -1 python:
    pass

define config.window_title = "PULSE"
define config.screen_width  = 1920
define config.screen_height = 1080

label start:
    $ quick_menu = False
    scene black
    pause 1.0
    jump level1

label scene_shaving_trigger:
    $ mg_shave_done = False
    $ mg_shave_zones = {
        "left_cheek":  {"x": 750,  "y": 450, "w": 160, "h": 220, "done": False},
        "right_cheek": {"x": 1010, "y": 450, "w": 160, "h": 220, "done": False},
        "chin":        {"x": 860,  "y": 680, "w": 200, "h": 150, "done": False},
        "mustache":    {"x": 870,  "y": 580, "w": 180, "h": 80,  "done": False}
    }
    call screen minigame_shave
    scene ruslan_shaved with dissolve
    "Готово. Теперь я выгляжу нормально."
    return

label endgame_credits:
    scene black with dissolve
    pause 2.0
    call screen support_resources
    return

screen support_resources():
    modal True
    add "#0d0d11"
    vbox:
        xalign 0.5 yalign 0.5
        spacing 35
        text "Если вы или ваши близкие столкнулись с тяжелым эмоциональным состоянием, тревогой или кризисной ситуацией, помните, что вы не одни и помощь всегда рядом." xalign 0.5 xsize 1100 text_align 0.5 color "#dddddd" size 26
        null height 15
        vbox:
            xalign 0.5
            spacing 12
            text "Единый телефон доверия (Всероссийский): 8 (800) 200-01-22" xalign 0.5 color "#ffffff" size 24 bold True
            text "Горячая линия психологической помощи: +7 (495) 051 (с мобильного)" xalign 0.5 color "#ffffff" size 24 bold True
            text "Горячая линия помощи при кризисных ситуациях: 8 (800) 333-44-34" xalign 0.5 color "#ffffff" size 24 bold True
        null height 15
        text "Вы также можете обратиться в местные кризисные центры, психоневрологические диспансеры (ПНД) или службы экстренной помощи по номеру 112." xalign 0.5 xsize 1000 text_align 0.5 color "#aaaaaa" size 20 italic True
        null height 30
        textbutton "Выйти в главное меню":
            xalign 0.5
            action Return()
            text_size 22
            text_color "#7777aa"
            text_hover_color "#ffffff"