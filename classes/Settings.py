import os 
import yaml
from progress.bar import IncrementalBar
import time

links = []
bar = IncrementalBar('Процесс', max = 150000)
for root,dirs,files in os.walk("c:/"):
    bar.next()
    for files in files:
        if files[-3:] == "lnk" or files[-3:] == "exe":
            links.append(os.path.join(root,files))
bar.finish()

def writeYaml(path):
    with open('./yaml/commands.yaml',"r+",encoding="utf-8") as file:
        body =  f"\ncom{time.time()}:\n" + "  keyword:\n"
        while True:
          print("Введите комманду или название программы (отправьте n если хотите завершить):")
          com = input("com^ ")
          if com == 'n':
              break
          body += f"  - {com}\n"

        
        song = input("Введите название мелодии:")
             
        body += f'  path: {path}\n' + f"  ahkFile: no\n  sound: {song}\n  action: start"
        file.seek(0,2)
        file.write(body)
    file.close()
        


while True:
    Name = input("\nВведи название программы: ")
    for i in range(len(links)):
        if Name.lower() in links[i].lower():
            print(f"[{i}] {links[i]}")

    index = int(input("\nВведите индекс строки. Либо число меньше 0.^ "))
    
    if index > -1:
      print(f"путь до программы = {links[index]}")
      writeYaml(links[index])
      
    yes = input("продолжить? (y/n)^ ")
    if yes == 'y':
        continue
    else:
        break