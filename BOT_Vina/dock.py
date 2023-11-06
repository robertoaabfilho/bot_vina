import os
import re
import pathlib
import pygetwindow
import datetime 
import time
import os.path
import shutil
import csv
from csv import writer
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from datetime import date

ranking = 'ranking.csv'
config = 'config.txt'
out = 'resultado.pdbqt'
caminhodock = str(os.getcwd())

with open(ranking, 'w+') as r:
    r.write('Alvo,Ligante,Afinidade (kcal/mol),rmsd l.b,rmsd u.b')

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

for f in ligantes:
	datarela = time.ctime(os.path.getmtime('relatorio.txt'))
    
	ligante = str(os.path.basename(f))
	ligtemp = f"{caminhodock}\\{ligante}"
	shutil.move(os.path.join(caminholig, ligante), ligtemp)
	time.sleep(5)

	with open(config, "w") as file:
		file.write(f'receptor = {prot} \nligand = {ligante} \n\nout = {out}\
		\n\ncenter_x = {c_x}\ncenter_y = {c_y}\ncenter_z = {c_z}\n\nsize_x = {s_x}\
        \nsize_y = {s_y}\nsize_z = {s_z}\n \nexhaustiveness = 24 \n\nnum_modes = 40\
        \n\nenergy_range = 20')

	time.sleep(5)

	os.system('vina.exe --config config.txt --log relatorio.txt')
	datarela2 = time.ctime(os.path.getmtime('relatorio.txt'))

	while datarela2==datarela:
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
	    linha26 = extrai_linha_txt(nome_arquivo='relatorio.txt', numero_linha=26)
	except:
	    time.sleep(5)
	    linha26 = extrai_linha_txt(nome_arquivo='relatorio.txt', numero_linha=26)

	remover1 = linha26.pop(0)
	addprot = linha26.insert(0, prot)
	addlig = linha26.insert(1, ligante)
	linha26 = ','.join(linha26)
    
	time.sleep(5)
	with open('ranking.csv', 'a') as r:
	    r.write('\n'+linha26)

	time.sleep(5)
	lig = f"{caminholig}\\{ligante}"
	shutil.move(os.path.join(caminhodock, ligtemp), lig)
	time.sleep(5)

	print('docking com '+ligante+' concluído')

prot = f"{caminhoprot}\\{prot}"
shutil.move(os.path.join(caminhodock, prottemp), prot)
os.system('exit')


