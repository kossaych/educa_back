from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem
from numpy import array
import pickle
 
def verif_operation(ch)  :
    i=0
    while i <= len(ch) - 1 and ch[i] in ['M','D','C' ,'L' ,'X', 'V' ,'I' ,'+','-'] :
        i += 1
    return i > len(ch) - 1 and (ch.find('+') != -1 or ch.find('-') != -1) and ch.find('+') != 0 and ch.find('+') != len(ch)-1 and ch.find('-') != 0 and ch.find('-') != len(ch)-1 
def remplir_fichier_nombre(): 
    file_source = open("nombre.dat", "ab")
    rom = window.nb_rom.text()
    dec = window.nb_dec.text()
    if len(rom) == 0 and rom.isdigit() and dec.isdigit() == False :
        QtWidgets.QMessageBox.critical(window, "Erreur de saise nombre dec ou rom", QtWidgets.QMessageBox.Ok)
    pickle.dump({'rom' : rom,'dec' : dec}, file_source) 
    file_source.close()
    affichage_fichier_nombre()
    

def remplir_fichier_operation() : 
    file_source = open("operation.txt", "a")
    operation = window.operation.text()
    if len(operation) < 3   or not verif_operation(operation)  :
       
        QtWidgets.QMessageBox.critical(window, "Erreur de saise nombre dec ou rom", "Voulez-vous confirmer votre saise",
                                       QtWidgets.QMessageBox.Ok)
    else :
        file_source.write(operation + '=?'+'\n')
        
        file_source.close()
        afficher_operation()
        
def afficher_operation () :
    file_source = open("operation.txt", "r")  
    window.fichier_resultat.clear()
    data = file_source.readline()
    while data != '' :  
        window.fichier_operation.addItem(data) 
        data = file_source.readline()
    file_source.close()  
    
    
    
def affichage_fichier_nombre() :
    file_source = open("nombre.dat", "rb") 
    column = 0
    continuer = True
    while continuer :
        try  : 
                data = pickle.load(file_source)
                print(data)
                # initialiser le tableau
                window.fichier_nombre.setRowCount(2) 
                window.fichier_nombre.setVerticalHeaderLabels(['rom','dec'])  
                window.fichier_nombre.setColumnCount(column +  1)
                
                # remplir tableau
                window.fichier_nombre.setItem(0,column,QTableWidgetItem( str(data['rom'])))
                window.fichier_nombre.setItem(1,column,QTableWidgetItem( str(data['dec'])))
                column += 1
        except :
            continuer = False
         
    
    file_source.close()


def equivalent(chiffre_rom) : 
    file_source = open("nombre.dat", "rb") 
    column = 0
    continuer = True
    data = pickle.load(file_source)
    
    while continuer and chiffre_rom != data['rom'] :
         try  :
             data = pickle.load(file_source) 
         except :
            continuer = False
    file_source.close()
    print(data,chiffre_rom)
    if chiffre_rom == data['rom'] :
        print(int(data['dec']),'/////******')
        return int(data['dec'])
    
    
    
     
def convertir (ch):
    print(ch,'***')
    nb = 0
    
    if len(ch) > 1 :
        for i in range(len(ch)-1) :
            if equivalent(ch[i]) >= equivalent(ch[i+1]) :
                 
                    nb += equivalent(ch[i])
            else :
                 
                    nb -= equivalent(ch[i])
    return nb + equivalent(ch[-1])

   
   
   
def afficher_resultat () :
    file_source = open("operation.txt", "r")  
    window.fichier_resultat.clear()
    data = file_source.readline()
    while data != '' : 
        if data.find('+') != -1 : 
            pr_nombre = convertir(data[0:data.find('+')])
            de_nombre = convertir(data[data.find('+') + 1:data.find('=')])
            
            print(pr_nombre , de_nombre)
            window.fichier_resultat.addItem(data[:-2] + str(pr_nombre + de_nombre))
            
        else :
            pr_nombre = convertir(data[0:data.find('-')])
            de_nombre = convertir(data[data.find('-')+1:data.find('=')])
            print(pr_nombre-de_nombre) 
            window.fichier_resultat.addItem(data[:-2] +pr_nombre - de_nombre)

        data = file_source.readline()
    file_source.close()

 
application = QtWidgets.QApplication([])
window = uic.loadUi("rom.ui")
window.show()
# button
window.remplir.clicked.connect(remplir_fichier_nombre)
window.ajouter.clicked.connect(remplir_fichier_operation)
window.afficher.clicked.connect(afficher_resultat)



 
application.exec()

 