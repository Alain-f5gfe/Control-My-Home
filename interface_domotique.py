#!/home/f5gfe/tableau_de_bord/.venv/bin/python3
# -*- encoding: utf-8 -*-

''' 
#### Commande directe des objets de ma domotique dans une interface graphique. ###
Le but est d'avoir une interface de pilotage même si le serveur hébergeant Domoticz
est en panne
Attention: Il y a conflit entre cette interface et Domoticz si on les utilise
en parallèle. 
Il peut être nécessaire de lancer nmap afin de rafraîchir la table ARP du PC.

'''
import sys
from PySide6.QtWidgets import (
    QWidget, QLineEdit, QScrollArea, QMainWindow,
    QApplication, QVBoxLayout, QSpacerItem, QSizePolicy, QCompleter,
    QWidget, QLabel, QPushButton, QHBoxLayout)
from PySide6.QtCore import Qt
from pathlib import Path
import etat_sonoff
from etat_sonoff import sonoffIP, send_ordre_on, send_ordre_off

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.controls = QWidget()  # Controls main widget.
        self.controlsLayout = QVBoxLayout()   # Controls main layout.
        self.etat_actuel = 0
        self.modify_widgets()
        #la liste de noms des widgets isuues des clefs sont stockés dans une liste
        widget_names = []
        self.widgets = []
        
        # parcourir la liste en créant un nouveau OnOffWidget
        # pour chacun d'entre eux,déclencher la recherche de leur état l'ajouter au layout
        # + stocker sa référence dans la liste self.widgets
        for inter in etat_sonoff.sonoffIP:
            self.etat_actuel = (sonoffIP.get(inter)[1])
            item = OnOffWidget(inter)
            print(inter, item)
            self.controlsLayout.addWidget(item)
            self.widgets.append(item)
            print(self.widgets)
        
        
        # mise en page des éléments gestion de la taille des widgets
        spacer = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.controlsLayout.addItem(spacer)
        self.controls.setLayout(self.controlsLayout)
        
        # assenceur 
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.controls)

        # barre de recherche.
        self.searchbar = QLineEdit()
        self.searchbar.textChanged.connect(self.update_display)

        # Prédiction de texte de la barre de recherche
        self.completer = QCompleter(widget_names)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.searchbar.setCompleter(self.completer)

        # Ajouter la ligne recherche VBoxLayout (appliqué au widget principal
        # qui englobe l'ensemble de la fenêtre).
        main = QWidget()
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.searchbar)
        mainLayout.addWidget(self.scroll)

        main.setLayout(mainLayout)
        self.setCentralWidget(main)

        self.setGeometry(700, 100, 800, 700)
        self.setWindowTitle('Contrôle de la domotique')

    def update_display(self, text):
        '''
        rafraichi l'affichage. + comparer le texte nom des zones aux mots 
        de barre de recherche après conversion en minuscule
        '''
        for widget in self.widgets:
            if text.lower() in widget.name.lower():
                widget.show()
            else:
                widget.hide()

    def modify_widgets(self):
        css_file = Path.cwd() /"style.css"
        with open(css_file, "r") as f:
            self.setStyleSheet(f.read())
        
    def persit():
        ''' sauve l état des widgets '''
        print("liste widgets ", self.widgets)


class OnOffWidget(QWidget):
    '''
    creation d'un widget personalisé d'un bouton en mode bistable
    '''
    def __init__(self, name):
        super(OnOffWidget, self).__init__()

        self.is_on = 0
        print("le nom du widget ", name)
        self.name = name
        self.etat_actuel = (sonoffIP.get(self.name)[1])
        self.lbl = QLabel(self.name)
        self.btn_on = QPushButton("Marche")
        self.btn_on.setCheckable(True)
        self.btn_off = QPushButton("Arrêt ")
        self.btn_off.setCheckable(False)
        
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.lbl)
        self.hbox.addWidget(self.btn_on)
        self.hbox.addWidget(self.btn_off)

        # récupérer le non de la ligne ????
        
        self.btn_on.clicked.connect(self.on)
        self.btn_off.clicked.connect(self.off)
        self.setLayout(self.hbox)
        self.update_button_state()

    def show(self):
        """
        dans la recherche afficher ces widgets, et tous les widgets enfants.
        """
        for w in [self, self.lbl, self.btn_on, self.btn_off]:
            w.setVisible(True)

    def hide(self):
        """
        cacher ces widgets, et tous les widgets enfants.
        """
        for w in [self, self.lbl, self.btn_on, self.btn_off]:
            w.setVisible(False)

    def off(self):
        self.etat_actuel = 0
        send_ordre_off(self.name)
        self.update_button_state()
        print("etat_actuel après un clic off", self.etat_actuel)

    def on(self):
        self.etat_actuel = 1
        send_ordre_on(self.name)
        self.update_button_state()
        print("etat_actuel après un clic on", self.etat_actuel)

    def update_button_state(self):
        """
        Mettre à jour l'apparence des boutons de contrôle (On/Off)
        en fonction de l'état actuel.
        """
        if self.etat_actuel == 1:
            self.btn_on.setStyleSheet("background-color: #008000; color: #fff;")
            self.btn_off.setStyleSheet("background-color: none; color: none;")
        else:
            self.btn_on.setStyleSheet("background-color: none; color: none;")
            self.btn_off.setStyleSheet("background-color: #FF0000; color: #fff;")
            
    def persit(widgets):
        ''' sauve l état des widgets '''
        print(widgets)
        

app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec())

