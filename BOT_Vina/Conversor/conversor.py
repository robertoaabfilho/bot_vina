# -*- coding: utf-8 -*-

import os
import re
import pathlib
import pyautogui
import shutil
import time
from tkinter import filedialog
from zipfile import ZipFile
from tkinter.filedialog import askopenfilename
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

print('\nSelecione a pasta "Downloads"\n')
downloaddir = filedialog.askdirectory()          
d = str(downloaddir)

print('\nSelecione a pasta de ligantes\n')
ligantesdir = filedialog.askdirectory()          
caminho = str(ligantesdir)                      
ligantes = os.listdir(caminho)

print('\nAcessando conversor online\n')

#Convertendo mol2 para pdbqt

navegador = webdriver.Chrome()
try:
	time.sleep(5)
	pyautogui.hotkey('winleft', 'up')
	navegador.get("https://htpsurflexdock.biocomp.uenf.br/convert_mol2_to_pdbqt/")
except:
	navegador.refresh()

for ligante in ligantes:
	time.sleep(3)
	botao1 = pyautogui.locateCenterOnScreen('figs/escolher.png', confidence=0.7)
	pyautogui.click(botao1)
	time.sleep(3)
	pyautogui.hotkey('ctrl', 'f')
	time.sleep(3)
	pyautogui.write(caminho)
	pyautogui.press('enter')
	time.sleep(1)
	nome = pyautogui.locateCenterOnScreen('figs/nome.png', confidence=0.7)
	pyautogui.click(nome)
	pyautogui.write(ligante)
	pyautogui.press('enter')
	time.sleep(2)
	botao2 = pyautogui.locateCenterOnScreen('figs/upload.png', confidence=0.7)
	pyautogui.click(botao2)
	time.sleep(2)
pyautogui.hotkey('ctrl', 'f4')

#Compilando

destino = str(os.getcwd())

arquivos = f"{destino}\\arquivos\\"
a = os.chdir(arquivos)
p = os.listdir(a)
try:
	for file in p:
		os.remove(file)
except:
	print("pasta vazia!")

down = os.chdir(d)
listd = os.listdir(down)
for f in listd:
	if "compound" in f:
		file2 = str(arquivos+'\\'+f)
		shutil.move(os.path.join(d, f), file2)
a = os.chdir(arquivos)
p = os.listdir(a)
for f in p:
	if 'compound' in f:
		with ZipFile(f, 'r') as zip:
			zip.extractall()
		os.remove(f)
