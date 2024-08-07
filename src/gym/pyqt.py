# importing libraries
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import *
from PyQt5 import QtTest
 
import sys
from random import randint
import time
    
class Window(QMainWindow):
 
    def __init__(self):
        super().__init__()
 
        # setting title
        self.setWindowTitle("Network Stimulation")
        
        # setting geometry
        self.setGeometry(100, 100, 560, 700)
        self.position_src_x = 25
        self.position_src_y = 25
        self.position_dest_x = 430
        self.position_dest_y = 25
        self.position_switch_x = 230
        self.position_switch_y = 130
        
        #Read the adjacenecy matrix
        self.readGraph()
        
        f = open("specifications.txt", "r")
        self.node_map = {}
        self.queue_map = {}
        self.latency_map = {} 
        
        line = f.readline()
        #Store the src, destination and switches in node_map dictionary with its position in matrix, node and color in an array
        while line.strip() != '----':
            node = line.split(',')
            if node[0] not in self.node_map.keys():
                src_node, latency_node = self.create_node(node[0],"orange")
                self.node_map[node[0]] = [self.mapping.index(node[0]), src_node, "orange"]
                self.latency_map[node[0]] = latency_node
            if node[1] not in self.node_map.keys():
                self.node_map[node[1]] = [self.mapping.index(node[1]),self.create_node(node[1], "Lightblue", False), "Lightblue"]
            line = f.readline().strip()
        line = f.readline()
        
        #Store the switches details in arrays
        while line.strip() != '----':
            s = line.split(',')
            switch_node, queue_node_arr = self.create_switch(s[0],int(s[1].strip()))
            self.node_map[s[0]] = [self.mapping.index(s[0]),switch_node,"grey"]
            self.queue_map[s[0]] = queue_node_arr
            line = f.readline().strip()
        f.close()
            
        self.time_node = QLabel(self)
        self.time_node.setGeometry(405, 700, 50, 30)
        self.time_node.setStyleSheet("QLabel"
                                 "{"
                                 "background : black;"
                                 "color : white;"
                                 "}")
        self.time_node.setAlignment(Qt.AlignCenter)
        self.time_node.setFont(QFont('Arial', 15))
        self.time_node.setText('0')
        # showing all the widgets
        self.show()
        self.show_packets()
 
    def readGraph(self):
        f = open("network.txt")
        self.mapping = []
        for i in f.readline().strip().split(','):
            self.mapping.append(i)
        self.num_nodes = len(self.mapping)
        line = f.readline()
        line = f.readline().strip()
        self.graph=[[0 for i in range(self.num_nodes)] for i in range(self.num_nodes)]
        while line.strip() != '----':
            s = line.split('->')
            self.graph[self.mapping.index(s[0])][self.mapping.index(s[1])] = s[2]
            line = f.readline().strip()
        f.close()

    
    def create_node(self, text, color, isSrc = True):
        # creating a label
        node = QLabel(self)
        latency = None
        # setting geometry to the label
        if isSrc:
            node.setGeometry(self.position_src_x, self.position_src_y, 50, 50)
        else:
            node.setGeometry(self.position_dest_x, self.position_dest_y, 50, 50)
        # creating label multi line
        node.setWordWrap(True)
        # setting style sheet to the label
        node.setStyleSheet("QLabel"
                                 "{"
                                 "border : 4px solid black;"
                                 "background : "+color+";"
                                 "}") 
        # setting alignment to the label
        node.setAlignment(Qt.AlignCenter)
        # setting font
        node.setFont(QFont('Arial', 15))
        #set text
        node.setText(text)
        if isSrc:
             # creating a label
            latency = QLabel(self)
            latency.setGeometry(self.position_src_x-20, self.position_src_y-20, 20, 20)
            # creating label multi line
            latency.setWordWrap(True)
            # setting style sheet to the label
            latency.setStyleSheet("QLabel"
                                 "{"
                                 "border : 4px solid black;"
                                 "background : white;"
                                 "min-height: 20px;"
                                 "min-width: 20px;"
                                 "}")
            latency.setFont(QFont('Arial', 10))
        #update y coordinates
        if isSrc:
            self.position_src_y += 200
            return node, latency
        else:
            self.position_dest_y += 200
            return node

    def create_switch(self, text, queue_length=0):
        # creating a label
        switch = QLabel(self)
        # setting geometry to the label
        switch.setGeometry(self.position_switch_x, self.position_switch_y, 50, 50)
        # creating label multi line
        switch.setWordWrap(True)
        # setting style sheet to the label
        switch.setStyleSheet("QLabel"
                                 "{"
                                 "border : 4px solid black;"
                                 "background :green;"
                                 "color: white;"
                                 "min-height: 20px;"
                                 "min-width: 20px;"
                                 "border-radius: 25px;"
                                 "}")
        #create queue
        q = []
        if queue_length > 0:
            #set geometry
            w = 25
            h = 25
            x = int(self.position_switch_x+25-(queue_length*12.5))
            y = int(self.position_switch_y+55)
            for i in range(queue_length):
                l = QLabel(self)
                l.setGeometry(x,y,w,h)
                l.setWordWrap(True)
                x += w
                l.setStyleSheet("QLabel"
                                 "{"
                                 "border : 2px solid black;"
                                 "background : light grey;"
                                 "text-align: center;"
                                 "}")
                l.setText('0')
                l.setFont(QFont('Arial', 8))
                q.append(l)
 
        # setting alignment to the label
        switch.setAlignment(Qt.AlignCenter)
        # setting font
        switch.setFont(QFont('Arial', 15))
        switch.setText(text)
        #Update f- coordinates
        self.position_switch_y += 200
        return switch, q
 
    def paintEvent(self, event):
        painter = QPainter(self)
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                if int(self.graph[i][j]) > 0:
                    n1 = self.node_map[self.mapping[i]][1]
                    n2 = self.node_map[self.mapping[j]][1]
                    painter.drawLine(n1.x()+25,n1.y()+25,n2.x()+25,n2.y()+25)

                 
    def show_packets(self):
        f = open("data.txt", "r")
        dic = f.readline().strip()
        pkt_dic = {}
        #timer to represent timestamps
        timer = 0
        latency_index = 0
        while(dic):
            #{S1:[[0,0,0,0,B1],UP], S2:[[0,A1],UP]}
            #Prepare dictionary
            #Real time data is expected innthe format
            items = dic[1:-1].split(', ')
            for i in items:
                switch = i.split(':')[0]
                value = i.split(':')[1][1:-1]
                status_lambda = value.split('],')[1]
                status = status_lambda.split(',')[0]
                lambda_val = status_lambda.split(',')[1]
                queue = []
                pkts = value.split('],')[0][1:]
                for i in pkts.split(','):
                    queue.append(i)
                pkt_dic[switch] = [queue, status, lambda_val]
            #iterate through dic items
            for s, q_arr in pkt_dic.items():
                #default color of switch to represent status
                color = "green"
                if q_arr[1] == "DOWN":
                    color = "red"
                #update stylesheet
                #required update to entire sheet, else border radius is overridden
                self.node_map[s][1].setStyleSheet("QLabel"
                                 "{"
                                 "border : 4px solid black;"
                                 "background : "+color+";"
                                 "color: white;"
                                 "min-height: 20px;"
                                 "min-width: 20px;"
                                 "border-radius: 25px;"
                                 "}")
                #Iterate through q nodes of switch 
                q = self.queue_map[s]
                q_len = len(q)
                for i in range(q_len):
                    src_node = str(q_arr[0][i])
                    #default color of node for 0
                    q_ncolor = "light grey"
                    if src_node != '0':
                        # update color with that of src node
                        if src_node[:2] in self.node_map.keys():
                            q_ncolor = self.node_map[src_node[:2]][2]
                        else:
                            q_ncolor = grey
                    #update text with src node + packet number    
                    q[i].setText(src_node)
                    q[i].setStyleSheet("QLabel"
                                 "{"
                                 "border : 2px solid black;"
                                 "background : "+q_ncolor+";"
                                 "}")

            lambda_vals = [0.5,0.6,0.7,0.8]
            for latency_node in self.latency_map.values():
                latency_node.setText(str(lambda_vals[latency_index]))
            #Increment the timer
            timer+=1
            if timer%5 == 0:
                #Increment the index
                latency_index += 1
                if latency_index == 3:
                    latency_index = 0
            #update time node with text of timer
            self.time_node.setText(str(timer))
            #wait for 2 seconds
            #remove for real time
            QtTest.QTest.qWait(2000)
            #read the next line
            #remove in real time
            dic = f.readline().strip()
            
        #set time node to 0
        self.time_node.setText('0')
        #show msg
        self.show_info_messagebox()
        
            
    def show_info_messagebox(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)      
        # setting Message box window title
        msg.setWindowTitle("Stimulation Complete")
      
        # declaring buttons on Message Box
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setText("All Packets Done!!")
        retval = msg.exec_()
        #exit the app if ok
        if retval == QMessageBox.Ok:
            sys.exit()
        
            
# create pyqt5 app
App = QApplication(sys.argv)
 
# create the instance of our Window
window = Window()
 
# start the app
exit(App.exec())
