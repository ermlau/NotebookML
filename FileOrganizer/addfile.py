import os
import shutil
import csv
import sys
import re

# prelevo i parametri
if len(sys.argv) == 1:
    print('specificare un nome file comprensivo di estensione')
    sys.exit(2)

# prendo il nome del file
nomefile = sys.argv[1]

# testo che il nome file sia nel formato valido nome.ext
validName = re.match('^[\w]{1,50}\.[\w]{1,20}$', nomefile)

if not validName:
    print(f'il nome file \'{nomefile}\' non è corretto, il formato accettato è nomefile.estensione')
    sys.exit(2)

# controllo che non mi sia stato specificato proprio il file di recap
if nomefile == 'recap.csv':
    print('non è possibile specificare il file recap.csv')
    sys.exit(2)

# faccio una verifica dell'esistenza del file
if not os.path.isfile('files/' + nomefile):
    print(f'file {nomefile} inesistente (il nome del file è case sensitive)')
    sys.exit(2)

# prelevo le informazioni del file
info = os.stat(f"files/{nomefile}")

# conservo i tipi di file per ogni tipo
TipoText = ['.doc', '.docx', '.txt', '.odt']
TipoImage = ['.jpg', '.png', '.jpeg']
TipoAudio = ['.mp3']

# funzione di trasformazione da estensione a tipo
def getTipo(extension):
    if extension in TipoText:
        return 'doc'
    if extension in TipoImage:
        return 'image'
    if extension in TipoAudio:
        return 'audio'
    return 'unknow'


# funzione di trasformazione da estensione a directory di destinazione
def getDirectory(extension):
    if extension in TipoText:
        return 'docs'
    if extension in TipoImage:
        return 'images'
    if extension in TipoAudio:
        return 'audio'
    return 'unknow'


# verifico che le directory di destinazione siano esistenti
if not os.path.isdir('files/audio'):
    os.mkdir('files/audio')
if not os.path.isdir('files/docs'):
    os.mkdir('files/docs')
if not os.path.isdir('files/images'):
    os.mkdir('files/images')

# verifico che il file csv sia esistente
# nel caso non lo fosse lo creo
if not os.path.isfile('files/recap.csv'):
    with open('files/recap.csv', 'w', newline='') as file:
        csv.writer(file).writerow(["name", "type", "size(B)"])


# controlli finiti ora effettuo le operazioni
#divido il nome del file in nome ed estensione
filename, file_extension = os.path.splitext(nomefile)
# derivo il tipo di file
tipoFile = getTipo(file_extension)
# controllo che sia un file conosciuto
if tipoFile == 'unknow':
    print(f"file {nomefile} di tipo sconosciuto")
    pass
else:
    # stampo i dettagli del file
    print(f'{filename} type:{tipoFile} size:{info.st_size}B')
    # sposto il file
    shutil.move('files/' + nomefile, 'files/' + getDirectory(file_extension) + '/' + nomefile)
    # scrivo sul file di recap lo spostamento del file
    with open('files/recap.csv', 'a', newline='') as file:
        csv.writer(file).writerow([filename, tipoFile, info.st_size])


