# ============================================================
# PULSE — minigames.rpy
# Скрипты, экраны и логика всех мини-игр проекта
# ============================================================

# ============================================================
# 1. МИНИ-ИГРА: БУДИЛЬНИК
# ============================================================
label minigame_alarm_run:
    $ mg_alarm_progress = 0.0
    $ mg_alarm_done = False
    call screen minigame_alarm
    scene black with dissolve
    return

screen minigame_alarm():
    modal True
    add "#0a0a0a"

    if not mg_alarm_done and mg_alarm_progress > 0.0:
        timer 0.1 action SetVariable("mg_alarm_progress", max(mg_alarm_progress - 0.015, 0.0)) repeat True

    frame:
        xalign 0.5 ypos 80 background None
        vbox:
            spacing 8
            text "Воля" xalign 0.5 color "#aaaaaa" size 20
            bar:
                value AnimatedValue(mg_alarm_progress, 1.0, 0.15)
                xsize 400 ysize 22
                left_bar Frame("#6666cc", 4, 4)
                right_bar Frame("#333355", 4, 4)

    if not mg_alarm_done:
        imagebutton:
            xalign 0.5 yalign 0.5
            idle "images/alarm_idle.png"
            hover "images/alarm_hover.png"
            action [
                SetVariable("mg_alarm_progress", min(mg_alarm_progress + 0.11, 1.0)),
                If(mg_alarm_progress >= 0.99, true=SetVariable("mg_alarm_done", True), false=NullAction())
            ]
    else:
        timer 0.6 action Return()


# ============================================================
# 2. МИНИ-ИГРА: СВОБОДНОЕ БРИТЬЁ
# ============================================================
init python:
    import pygame
    import os

    class FreeShaveDisplayable(renpy.Displayable):
        def __init__(self, **kwargs):
            super(FreeShaveDisplayable, self).__init__(**kwargs)
            
            bg_beard_path = os.path.join(config.gamedir, "images/5.png")
            bg_clean_path = os.path.join(config.gamedir, "images/6.png")
            
            self.surf_beard = pygame.image.load(bg_beard_path).convert_alpha()
            self.surf_clean = pygame.image.load(bg_clean_path).convert_alpha()
            
            self.mask_surface = pygame.Surface((1920, 1080), pygame.SRCALPHA)
            self.mask_surface.fill((255, 255, 255, 255))
            
            self.is_shaving = False
            self.shaved_pixels = 0
            self.total_target_pixels = 350 

        def render(self, width, height, st, at):
            render = renpy.Render(1920, 1080)
            combined_surface = pygame.Surface((1920, 1080), pygame.SRCALPHA)
            
            combined_surface.blit(self.surf_clean, (0, 0))
            
            temp_beard = self.surf_beard.copy()
            temp_beard.blit(self.mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            combined_surface.blit(temp_beard, (0, 0))
            
            pygame_render = renpy.Render(1920, 1080)
            pygame_render.blit(combined_surface, (0, 0))
            
            render.blit(pygame_render, (0, 0))
            return render

        def event(self, ev, x, y, st):
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                self.is_shaving = True
            elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                self.is_shaving = False
                
            if (ev.type == pygame.MOUSEMOTION or self.is_shaving) and self.is_shaving:
                pygame.draw.circle(self.mask_surface, (0, 0, 0, 0), (int(x), int(y)), 55)
                self.shaved_pixels += 1
                renpy.redraw(self, 0)
                
                if self.shaved_pixels > self.total_target_pixels:
                    renpy.timeout(0.01)
                    return "shaved"
            return None

screen minigame_shave():
    modal True
    add FreeShaveDisplayable()
    text "Зажмите левую кнопку мыши и побрейте лицо" xalign 0.5 yalign 0.94 color "#ffffff" size 24 italic True


# ============================================================
# 3. МИНИ-ИГРА: КОНСПЕКТ (ФИКСАЦИЯ И ВЫРАВНИВАНИЕ)
# ============================================================
init python:
    import math

    # Координаты выровнены по центру тетрадного листа
    NOTE_PATH = [
        (380, 680), (520, 480), (670, 630), (820, 510), 
        (970, 680), (1120, 460), (1270, 630), (1420, 480), 
        (1570, 650), (1700, 480)
    ]
    NOTE_TOLERANCE = 80.0

    def get_target_y(current_x):
        if current_x <= NOTE_PATH[0][0]:
            return NOTE_PATH[0][1]
        if current_x >= NOTE_PATH[-1][0]:
            return NOTE_PATH[-1][1]
            
        for i in range(len(NOTE_PATH) - 1):
            p1 = NOTE_PATH[i]
            p2 = NOTE_PATH[i+1]
            if p1[0] <= current_x <= p2[0]:
                t = float(current_x - p1[0]) / float(p2[0] - p1[0])
                return p1[1] + (p2[1] - p1[1]) * t
        return NOTE_PATH[0][1]

    class NoteGameDisplayable(renpy.Displayable):
        def __init__(self, **kwargs):
            super(NoteGameDisplayable, self).__init__(**kwargs)
            self.is_dragging = False

        def render(self, width, height, st, at):
            render = renpy.Render(1920, 1080)
            draw_surf = pygame.Surface((1920, 1080), pygame.SRCALPHA)
            
            for i in range(len(NOTE_PATH) - 1):
                pygame.draw.line(draw_surf, (220, 220, 240, 180), NOTE_PATH[i], NOTE_PATH[i+1], 6)
            
            start_x = NOTE_PATH[0][0]
            end_x = NOTE_PATH[-1][0]
            dot_x = int(start_x + store.mg_note_progress * (end_x - start_x))
            dot_y = int(get_target_y(dot_x))
            
            dot_color = (46, 204, 113, 255) if self.is_dragging else (231, 76, 60, 255)
            pygame.draw.circle(draw_surf, dot_color, (dot_x, dot_y), 16)
                
            pygame_render = renpy.Render(1920, 1080)
            pygame_render.blit(draw_surf, (0, 0))
            render.blit(pygame_render, (0, 0))
            return render

        def event(self, ev, x, y, st):
            start_x = NOTE_PATH[0][0]
            end_x = NOTE_PATH[-1][0]
            
            current_dot_x = start_x + store.mg_note_progress * (end_x - start_x)
            current_dot_y = get_target_y(current_dot_x)

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if math.hypot(x - current_dot_x, y - current_dot_y) < NOTE_TOLERANCE:
                    self.is_dragging = True
                    renpy.redraw(self, 0)
            
            elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                self.is_dragging = False
                renpy.redraw(self, 0)

            if ev.type == pygame.MOUSEMOTION and self.is_dragging and not store.mg_note_breathing and not store.mg_note_done:
                calculated_progress = float(x - start_x) / float(end_x - start_x)
                calculated_progress = max(0.0, min(1.0, calculated_progress))
                
                if calculated_progress >= store.mg_note_progress and (calculated_progress - store.mg_note_progress) < 0.04:
                    target_y = get_target_y(x)
                    distance_y = abs(y - target_y)
                    
                    if distance_y < NOTE_TOLERANCE:
                        store.mg_note_progress = calculated_progress
                        renpy.redraw(self, 0)
                        
                        if store.mg_note_progress >= 0.99:
                            store.mg_note_done = True
                            return "note_complete"
                    else:
                        if store.mg_note_progress > 0.02:
                            self.is_dragging = False
                            store.mg_note_errors += 1
                            store.mg_note_breathing = True
                            renpy.redraw(self, 0)
                            return "note_error"
            return None

default mg_note_progress = 0.0
default mg_note_errors = 0
default mg_note_done = False
default mg_note_breathing = False

label minigame_note_run:
    $ mg_note_progress = 0.0
    $ mg_note_errors = 0
    $ mg_note_done = False
    $ mg_note_breathing = False
    call screen minigame_note
    return

screen minigame_note():
    modal True
    
    # ИСПРАВЛЕНО: Строки фона и затемнения полностью закрыты кавычками
    add "images/notebook_bg.jpg" blur 12.0
    add "#00000022"

    add NoteGameDisplayable()

    vbox:
        xalign 0.5 ypos 45
        text "Зажмите ЛКМ на точке и ведите конспект по линии" xalign 0.5 color "#ffffff" size 24 drop_shadow (2, 2)

    if mg_note_breathing:
        add "#000000cc"
        text "Руслан отвлёкся и потерял мысль..." xalign 0.5 yalign 0.45 color "#ffffff" size 26
        text "Верните курсор к красной точке, зажмите ЛКМ и продолжайте" xalign 0.5 yalign 0.53 color "#aaaaaa" size 20 italic True
        timer 1.0 action SetVariable("mg_note_breathing", False)

    text "Ошибки: [mg_note_errors]" xpos 60 ypos 45 color "#ff5555" size 22 drop_shadow (1, 1)

    if mg_note_done:
        timer 0.5 action Return()