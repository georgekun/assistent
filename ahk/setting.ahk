Run cmd.exe
Sleep, 2000 ; ожидаем полсекунды, чтобы командная строка успела прогрузиться
;Send, cd .. {Enter}
Sleep, 1000
Send, python c:\Users\Jordan\Desktop\FridayAss\classes\Settings.py {Enter}
Sleep, 1000 ; ожидаем полсекунды, чтобы команда успела выполниться
ExitApp