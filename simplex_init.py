#!/usr/bin/python
#-*- coding: utf-8 -*-
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from simplex_po import *


class FrowBoxWindow(Gtk.Window):
    # Grid possui multiplas linhas e colunas
    def __init__(self):
        # variáveis para o simplex
        self.if_solucionar = False
        self.num_restricao = 0
        self.num_var_ini = 0
        self.tipo = 'max'
        self.funcao_objetivo = ''
        self.matriz = []
        # # # # # # # # # # # # # # # # # # # 3 # 

        Gtk.Window.__init__(self, title="Simplex")
        self.set_border_width(12)
        self.set_default_size(400, 200)
        # Scroll
        self.scroll = Gtk.ScrolledWindow(hexpand=True, vexpand=True)
        self.scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.box_sr = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=10)
        #self.scroll.set_default_size(400, 200)
        # Horizontal / 2 vertical
        self.box_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=10)
        self.box_superior = Gtk.Box(spacing=30)
        self.box_inferior = Gtk.Box(spacing=30)

        # Vertical
        self.box1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
        # Função objetivo
        self.box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
        
        # # # # # # # # # # # # # # # # 1 1aixa # # # # # # # # # # # # # # # # # # 
        button_esq_1 = Gtk.RadioButton.new_with_label_from_widget(None, "Maximizar")
        button_esq_1.connect("toggled", self.on_button_toggled, "1")
        self.box1.pack_start(button_esq_1, False, False, 0) 
        
        button_esq_2 = Gtk.RadioButton.new_from_widget(button_esq_1)
        button_esq_2.set_label("Minimizar")
        button_esq_2.connect("toggled", self.on_button_toggled, "2")
        self.box1.pack_start(button_esq_2, False, False, 0)

         # Número de variaveis
        self.box1.pack_start(Gtk.Label(""), False, False, 0)
        label_esq_0 = Gtk.Label("Número de variáveis:")
        self.box1.pack_start(label_esq_0, False, False, 0)

        adjustment_esq_1 = Gtk.Adjustment(0, 0, 1000, 1, 10, 0)
        self.spinbutton_esq_1 = Gtk.SpinButton()
        self.spinbutton_esq_1.set_adjustment(adjustment_esq_1)
        self.box1.pack_start(self.spinbutton_esq_1, False, False, 0)
        self.spinbutton_esq_1.connect("notify::active", self.on_click_me_clicked)
        self.box1.pack_start(Gtk.Label(""), False, False, 0)

        # Número de restrições
        label_esq_1 = Gtk.Label("Número de restrições:")
        self.box1.pack_start(label_esq_1, False, False, 0)

        adjustment_esq_2 = Gtk.Adjustment(0, 0, 1000, 1, 10, 0)
        self.spinbutton_esq_2 = Gtk.SpinButton()
        self.spinbutton_esq_2.set_adjustment(adjustment_esq_2)
        self.box1.pack_start(self.spinbutton_esq_2, False, False, 0)
        self.spinbutton_esq_2.connect("notify::active", self.on_click_me_clicked)

        button_esq_3 = Gtk.Button.new_with_label("Restrições")
        button_esq_3.connect("clicked", self.on_click_me_clicked,'restricao')
        self.box1.pack_start(button_esq_3, False, True, 0)


        self.box1.pack_start(Gtk.Label(""), False, False, 0)
        button_esq_4 = Gtk.Button.new_with_label("Solucionar",)
        button_esq_4.connect("clicked", self.on_click_me_clicked,'solucionar')
        self.box1.pack_start(button_esq_4, False, True, 0)
        # # # # # # # # # # # # # # # # 1 caixa # # # # # # # # # # # # # # # # # # 
        
        # # # # # # # # # # # # # # # # 2 caixa # # # # # # # # # # # # # # # # # # 
        # Linha 1
        self.grid1 = Gtk.Grid()
        self.label_ini1 = Gtk.Label("  Função objetivo:    ")
        self.grid1.add(self.label_ini1)

        self.entry1 = Gtk.Entry()
        self.entry1.set_text("1x_1 + 0x_2 = 0")
        self.grid1.add(self.entry1)
        self.box2.add(self.grid1)

        # Linha 2
        self.box_restricao =  Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
        self.grid2 = Gtk.Grid()
        label_ini2 = Gtk.Label("  Restrição:                ")
        self.grid2.add(label_ini2)
        self.entry2 = [] # Lista de text_edit para restrições
        self.box2.add(self.box_restricao)
        # # # # # # # # # # # # # # # # 2 caixa # # # # # # # # # # # # # # # # # #
        self.box_superior.add(self.box1)
        self.box_superior.add(self.box2)
        self.box_main.add(self.box_superior)
        self.box_main.add(self.box_inferior)

        self.scroll.add(self.box_main)
        #self.box_sr.add(self.scroll)pack_start
        self.box_sr.pack_start(self.scroll,True,True,0)
        self.add(self.box_sr)

    def on_button_toggled(self, button, name):
        if button.get_active():
            state = "on"
            if name == '1':
                self.tipo = 'max'
            else:
                self.tipo = 'min'
                
        else:
            state = "off"
            print("Button", name, "was turned", state)
        
        print("Button", name, "  Tipo:", self.tipo)
        
    def on_click_me_clicked(self, button, name):
        print self.spinbutton_esq_2.get_value() , "   Button: ", name

        if name == 'restricao':
            if ((self.spinbutton_esq_2.get_value() != 0.0) and (int(self.spinbutton_esq_2.get_value() != self.num_restricao))):
                print self.spinbutton_esq_2.get_value() , "   Button: ", name , "              OK"
                self.num_restricao = int(self.spinbutton_esq_2.get_value())
                # # # # # # # # # # # # # # # # 2 caixa # # # # # # # # # # # # # # # # # # 
                # remover tabela de restrições 
                self.box_restricao.destroy()
                self.box_restricao =  Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)

                self.box_restricao.pack_start(self.grid2, False, True, 0)
                
                self.entry2 = []

                for i in range(int(self.spinbutton_esq_2.get_value())):
                    self.entry2.append(Gtk.Entry())
                    self.entry2[i].set_text('1x_1 + 1x_2 <= 1')
                    self.box_restricao.pack_start(self.entry2[i], False, True, 0)
                # # # # # # # # # # # # # # # # 2 caixa # # # # # # # # # # # # # # # # # #
                self.box2.pack_start(self.box_restricao, False, True, 0)
                self.box_superior.show_all()

                #self.box.add(self.box2)

        elif name == 'solucionar':
            self.num_var_ini = int(self.spinbutton_esq_1.get_value())
            if ((self.num_var_ini != 0) and (self.num_restricao != 0)):
                if (self.if_solucionar):
                    self.box_inferior.destroy()
                self.box_inferior = Gtk.Box(spacing=30)
                box_inferior = Gtk.Box(spacing=30)
                self.funcao_objetivo = self.entry1.get_text()

                for i in range(self.num_restricao):
                    self.matriz.append(self.entry2[i].get_text())
                
                print " Num_var_inicial: ", self.num_var_ini,"   Num_restricao: ", self.num_restricao
                print " Tipo: ", self.tipo, "    Função objetivo: ", self.funcao_objetivo
                print " Matriz de restrições:  ", self.matriz

                objetivo = (self.tipo, self.funcao_objetivo)

                obje = Simplex(self.num_var_ini, self.matriz, objetivo)
                #obje.tipo
                #obje.base
                #obje.matriz
                
                grid = Gtk.Grid()
                label_solu = Gtk.Label('Solução: ')
                print "Solucao"
                grid.add(label_solu)
                box_inferior.pack_start(grid, False, True, 0)


                box_matriz = Gtk.Box(spacing=10)
                box_coluna = []
                label_matriz = []
                cont = 0

                box_coluna.append(Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=5))
                box_coluna[0].add(Gtk.Label(str(obje.topo[0])))
                for j in range(len(obje.base)):
                    box_coluna[0].add(Gtk.Label(obje.base[j]))
                box_matriz.add(box_coluna[0])

                for i in range(obje.num_var_ini+obje.num_var_s+1): 
                    box_coluna.append(Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=5))
                    box_coluna[i+1].add(Gtk.Label(str(obje.topo[i+1])))
                    for j in range(len(obje.base)):
                        label_matriz.append(Gtk.Label(str(obje.matriz[j][i])))
                        box_coluna[i+1].add(label_matriz[cont])
                        cont += 1
                    box_matriz.add(box_coluna[i+1])
                
                box_inferior.pack_start(box_matriz, False, True, 0)
               
                self.box_inferior.pack_start(box_inferior, False, True, 0)
                self.box_main.pack_start(self.box_inferior, False, True, 0)
                self.box_inferior.show_all()
                self.box_main.show_all()
                self.if_solucionar = True
                
                self.matriz = []
                #self.box1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)

#settings = Gtk.Settings.get_default()
#settings.set_property("gtk-application-prefer-dark-theme", True)
win = FrowBoxWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
#Gtk.rc_parse('/elementary/gtk-3.0/gtkrc')
#Gtk.rc_parse('~/.themes/Ant/gtk-2.0/gtkrc')
Gtk.main()
