

Run cmd.exe
Sleep, 2000 ; ожидаем полсекунды, чтобы командная строка успела прогрузиться
;Send, cd .. {Enter}

Sleep, 1000
Send, cd c:\Users\Jordan\Desktop\FridayAss {Enter}
Sleep, 1000 ; ожидаем полсекунды, чтобы команда успела выполниться
Send, git add . {Enter}
Sleep, 1000
Send, git commit -m "auto-commit" {Enter}
Sleep,2000

ExitApp