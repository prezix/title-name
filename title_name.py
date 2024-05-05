import subprocess
import chardet
from tkinter import Tk, Label, Button, Text, Scrollbar, END, Frame, StringVar, messagebox

# Функция для обнаружения кодировки и декодирования вывода консоли
def decode_console_output(output_bytes):
    detected_encoding = chardet.detect(output_bytes)['encoding']
    if detected_encoding:
        decoded_output = output_bytes.decode(detected_encoding, errors='replace')
        return decoded_output
    else:
        return None

# Функция для захвата и отображения вывода консоли
def capture_console_output(command):
    process = subprocess.Popen(["powershell", "-Command", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               shell=True)
    output, error = process.communicate()

    if output:
        decoded_output = decode_console_output(output)
        if decoded_output:
            return decoded_output
        else:
            return "Unable to decode output."
    if error:
        return error.decode('utf-8', errors='replace')

# Функция для обработки нажатия кнопки
def on_button_click(text_area):
    command = "Get-Process | Where-Object {$_.mainWindowTitle} | Format-Table Id, Name, mainWindowtitle -AutoSize"
    result = capture_console_output(command)
    text_area.insert(END, f"Console Output:\n{result}\n\n")

# Главная функция для запуска приложения
def main():
    window = Tk()
    window.title("Console Output Viewer")
    window.geometry("800x600")
    window.configure(bg="#282a36")  # Темный фон

    # Изменение шрифта на более темный
    default_font = ("Consolas", 12)
    window.option_add("*Font", default_font)

    label = Label(window, text="Running Command:", font=default_font, bg="#282a36", fg="#f8f8f2")
    label.pack(pady=20)

    button = Button(window, text="Execute Command", command=lambda: on_button_click(text_area), font=default_font, bg="#44475a", fg="#f8f8f2")
    button.pack(pady=10)

    text_area = Text(window, height=20, width=60, font=default_font, bg="#282a36", fg="#f8f8f2")
    text_area.pack(side="left", fill="both", expand=True)

    scrollbar = Scrollbar(window, command=text_area.yview, bg="#44475a")  # Исправлено
    scrollbar.pack(side="right", fill="y")

    text_area.config(yscrollcommand=scrollbar.set)

    window.mainloop()

if __name__ == "__main__":
    main()
