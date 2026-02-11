from pygame import *
import sounddevice as sd
import scipy.io.wavfile as wav

# === Налаштування ===
fs = 44100                      # Частота дискретизації для запису звуку (44.1 kГц – стандарт для аудіо)
recording = None                # Змінна, куди буде записуватись сирий аудіопотік
is_recording = False            # Прапорець: чи зараз триває запис
voice_file = "voice_record.wav" # Файл, куди буде зберегається записаний голос
minus_track = "MinusDuHast.mp3" # Мінусовка, яка буде грати під час запису

init()                                          # Ініціалізація всіх модулів pygame
mixer.init()                                    # Ініціалізація аудіомодуля pygame
mixer.music.set_volume(0.5)                     # Встановлення гучності мінусовки (0.0-1.0)

window_size = 1200, 600                         # Розмір вікна
window = display.set_mode(window_size)          # Створення вікна
clock = time.Clock()                            # Таймер для контролю FPS

font.init()                                                     # Ініціалізація шрифтів
font_big = font.SysFont("Arial", 32)                            # Великий шрифт для тексту кнопки

# Прямокутник кнопки (x, y, ширина, висота)
btn_rect = Rect(425, 250, 350, 80)
rect_color = 'white'                            # Початковий колір кнопки
btn_text = "Запис"                              # Початковий текст кнопки


def start_voice_record():
    """
    Почати запис голосу з мікрофона.
    sd.rec = асинхронний запис, який триває у фоновому режимі.
    Записуємо 15 секунд (fs * 15 семплів).
    """
    global recording
    recording = sd.rec(int(fs * 15), samplerate=fs, channels=1, dtype='int16')


def stop_voice_record():
    """
    Зупиняємо запис і зберігаємо результат у WAV-файл.
    """
    global recording
    sd.stop()                                   # Зупинив запис
    if recording is not None:
        wav.write(voice_file, fs, recording)    # Зберігаємо у файл


def play_song_and_voice_together():
    """
    Відтворюємо мінусовку та записаний голос одночасно.
    mixer.music – для MP3
    mixer.Sound – для WAV
    """
    mixer.music.load(minus_track)
    mixer.music.play()
    voice_sound = mixer.Sound(voice_file)
    voice_sound.play()


# === Основний цикл програми ===
while True:
    for e in event.get():
        if e.type == QUIT:
            quit()  # Закрити програми

        if e.type == MOUSEBUTTONDOWN:
            if btn_rect.collidepoint(e.pos):  # Якщо натиснули на кнопку
                if not is_recording:
                    # Починаємо запис
                    rect_color = 'red'                              # Кнопка стає червоною
                    btn_text = "Стоп та прослухати"                 # Текст змінюється
                    is_recording = True

                    mixer.music.load(minus_track)                   # Завантажуємо мінусовку
                    mixer.music.play()                              # Відтворюємо її
                    start_voice_record()                            # Починаємо запис голосу

                else:
                    # Зупиняємо запис і відтворюємо результат
                    rect_color = 'white'
                    btn_text = "Запис"
                    is_recording = False

                    stop_voice_record()                             # Зберігаємо запис
                    play_song_and_voice_together()                  # Відтворюємо мінус + голос

    # Оновлення графіки
    window.fill('grey')                                             # Фон
    draw.rect(window, rect_color, btn_rect)                         # Кнопка

    text_surface = font_big.render(btn_text, True, 'black')         # Текст кнопки
    window.blit(text_surface, (btn_rect.x + 20, btn_rect.y + 25))

    display.update()                                                # Оновлення екрану
    clock.tick(30)                                                  # 30 FPS
