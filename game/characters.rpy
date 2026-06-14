# ============================================================
# PULSE — characters.rpy
# Определения персонажей
# ============================================================

# Внутренний монолог Руслана (курсив, без имени)
define thought = Character(None, what_style="thought_style")

# Реплики вслух
define ruslan = Character("Руслан", color="#c8c8ff")
define sergey = Character("Серёга", color="#a8e6a8")
define kirill  = Character("Кирилл", color="#f0d080")
define teacher = Character("Преподаватель", color="#d0d0d0")
define mom     = Character("Мама", color="#f0a8a8")
define igor    = Character("Игорь", color="#a8c8f0")

# Стиль для мыслей — чуть меньше, курсив
style thought_style:
    italic True
    size 34
    color "#cccccc"
