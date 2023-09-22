import os
import re
import pathlib
import pyautogui
import pygetwindow
import time
import os.path
import shutil
import csv
from csv import writer
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from datetime import date

print("Caro usuário!\n\
Antes de iniciar o docking, execute os passos a seguir:\n\
1 - Usando o programa Biovia Discovery Studio, anote as coordenadas X, Y e Z da proteína\n\
2 - Usando o programa AutoDock Tools, anote as coordenadas X, Y e Z da caixa\n\
3 - Certifique-se de que os ligantes e as proteínas estejam no formato .pdbqt")

config = 'config.txt'
out = 'resultado.pdbqt'
log = 'dock/relatorio.txt'
auto_vina = str(os.getcwd())
caminhodock = f"{auto_vina}\\dock"

with open('ranking.csv', 'w+') as r:
    r.write('Alvo,Ligante,Afinidade (kcal/mol),rmsd l.b,rmsd u.b')

#Selecionando a pasta com os ligantes
print('\nSelecione a pasta de ligantes\n')
ligantesdir = filedialog.askdirectory() 
caminholig = f"{os.path.dirname(ligantesdir)}/{os.path.basename(ligantesdir)}"
ligantes = os.listdir(str(ligantesdir))

print('\nSelecione a proteína\n')
protdir = askopenfilename()           
caminhoprot = str(os.path.dirname(protdir))
prot = str(os.path.basename(protdir))

c_x = input("Insira a coordenada X da proteína ")
c_y = input("Insira a coordenada Y da proteína ")
c_z = input("Insira a coordenada Z da proteína ")
s_x = input("Insira a coordenada X da caixa ")
s_y = input("Insira a coordenada Y da caixa ")
s_z = input("Insira a coordenada Z da caixa ")

prottemp = f"{caminhodock}\\{prot}"
shutil.move(os.path.join(caminhoprot, prot), prottemp)

time.sleep(5)
pyautogui.hotkey('winleft', 's')
time.sleep(2)
pyautogui.write('cmd')
pyautogui.press('enter')
time.sleep(2)
#pyautogui.hotkey('winleft', 'up')

for f in ligantes:
    ligante = str(os.path.basename(f))
    ligtemp = f"{caminhodock}\\{ligante}"
    shutil.move(os.path.join(caminholig, ligante), ligtemp)
    time.sleep(5)

    with open('dock/config.txt', "w") as file:
        file.write(f'receptor = {prot} \nligand = {ligante} \n\nout = {out}\
         \n\ncenter_x = {c_x}\ncenter_y = {c_y}\ncenter_z = {c_z}\n\nsize_x = {s_x}\
         \nsize_y = {s_y}\nsize_z = {s_z}\n \nexhaustiveness = 24 \n\nnum_modes = 40\
          \n\nenergy_range = 20')
    time.sleep(5)
    
    pyautogui.write('cd/')
    pyautogui.press('enter')
    pyautogui.write('cd '+caminhodock)
    pyautogui.press('enter')
    pyautogui.write('vina.exe --config config.txt --log relatorio.txt')
    pyautogui.press('enter')
    time.sleep(5) 
    done = pyautogui.locateCenterOnScreen('concluido.png')
    while done==None:
        time.sleep(5)
        done = pyautogui.locateCenterOnScreen('concluido.png')
    print('docking com '+ligante+' concluído')

    time.sleep(5)
    lig = f"{caminholig}\\{ligante}"
    shutil.move(os.path.join(caminhodock, ligtemp), lig)
    time.sleep(5)

    def extrai_linha_txt(nome_arquivo: str, numero_linha: int):
        with open(file=nome_arquivo, mode='r', encoding='utf8') as fp:
            linhas = fp.read().splitlines()
        try:
            time.sleep(5)
            return linhas[numero_linha].split()
        except:
            time.sleep(10)
            return linhas[numero_linha].split()
    try:
        time.sleep(5)
        linha26 = extrai_linha_txt(nome_arquivo='dock/relatorio.txt', numero_linha=26)
    except:
        time.sleep(5)
        linha26 = extrai_linha_txt(nome_arquivo='dock/relatorio.txt', numero_linha=26)

    remover1 = linha26.pop(0)
    addprot = linha26.insert(0, prot)
    addlig = linha26.insert(1, ligante)
    linha26 = ','.join(linha26)
    
    time.sleep(5)
    with open('ranking.csv', 'a') as r:
        r.write('\n'+linha26)

prot = f"{caminhoprot}\\{prot}"
shutil.move(os.path.join(caminhodock, prottemp), prot)
pyautogui.write('exit')
pyautogui.press('enter')



