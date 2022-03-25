# IMPORTING LIBRARIES
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QEasingCurve, QPropertyAnimation, Qt
from PySide2 import *


# IMPORTING GUI FILE
from interface import *


# Main Window Class
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ##############################
        ##############################
        ######### Variables ##########
        ##############################
        ##############################
        gridWidth = 100
        gridHeight = 100
        gridFrames = 4
        gridFrameHeight = 100
        gridFrameWidth = 100
        statusPanelFrameHeight = 100
        statusPanelFrameWidth = 100

        ##############################
        ##############################

        ##############################
        #Removing Window Title Bar
        ##############################
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        ##############################
        # Setting Main Background To Transparent
        ##############################
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        ##############################
        # Shadow Effect Style
        ##############################
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(50)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 92, 157, 550))

        ##############################
        # Applying Shadow To Central Widget
        ##############################
        self.ui.centralwidget.setGraphicsEffect(self.shadow)


        ##############################
        # Setting Window Icon
        # This icon and title will not appear on our app main window
        # becasue we removed the title bar
        ##############################
        self.setWindowIcon(QIcon(":/icons/icons/camera.svg"))
        # Setting Window Title
        self.setWindowTitle("Modern UI")


        ##############################
        # Window Size grip to resize window
        ##############################
        #QSizeGrip(self.ui.size_grip)

        ##############################
        # Maximizing The Window
        ##############################
        self.MaximizeWindow()


        ##############################
        # Setting The Constraints
        ##############################
        self.SetConstraintsSpecs()


        ##############################
        # Minimizing The Window
        ##############################
        self.ui.minimize_window_button.clicked.connect(lambda: self.showMinimized())


        ##############################
        # Closing The Window
        ##############################
        self.ui.close_window_button.clicked.connect(lambda: self.close())

        ##############################
        # Restore / Maximize Window
        ##############################
        self.ui.restore_window_button.clicked.connect(lambda: self.restore_or_maximize_window())

        ##############################
        # Function to Move Window on Mouse Drag Event on the title Bar
        ##############################
        def moveWindow(e):
            # Detect if the window is normal size
            if self.isMaximized() == False:
                ## Moving Window only when the window is normal size
                ## Only Accepting the left Mouse Button
                if e.buttons() == Qt.LeftButton:
                    # Move Window
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()
            ###################################################
        #######################################################


        ##############################
        # Add CLick Event/Mouse Move Event/Drag event to the top header to move the window
        ##############################
        self.ui.body_header.mouseMoveEvent = moveWindow


        ##############################
        # Left Menu Toggle Button
        ##############################
        self.ui.open_close_side_bar_btn.clicked.connect(lambda: self.slideLeftMenu())


        ##############################
        # Right Status Menu Toggle Button
        ##############################
        self.ui.right_side_toggle_button_1.clicked.connect(lambda: self.slideRightMenu())


        ##############################
        # Right Side Menu Toggle Button 2
        ##############################
        self.ui.right_side_toggle_button_2.clicked.connect(lambda: self.enableAllCamerasGridView())


        ##############################
        # Calculating The Width and the Height of The Grid Frames
        ##############################



        ##############################
        # For Loop To Create A Grid Of GridFrames
        ##############################
        # Rows Loop
        for i in range(0, 2):
            # Columns Loop
            for j in range(0, 2):
                camera_frame_iter = self.createNewGridFrames(i, j)
                # Pushing to the camera List To Access Globally All Cameras
                camera_list.append(camera_frame_iter)
                # self.animateGridFrame(camera_frame_iter)


        ##############################
        # For Loop To Create A Grid Of GridFrames
        ##############################
        # Rows Loop
        count = len(camera_list) - 1
        while count > 0:
            self.createNewSideStatusPanelCameraFrames(count)
            count -= 1



        ##############################
        # Getting Click on the GridFrame
        ##############################

        # for camera in camera_list:
        #     widget = getattr(self.ui, camera)
        #     self.widget.mousePressEvent = self.GridFrameClicked

        self.ui.frame_00.mousePressEvent = self.GridFrameClicked

        # self.ui.camera_list[1].mousePressEvent = self.GridFrameClicked
        
        # self.ui.camera_list[2].mousePressEvent = self.GridFrameClicked
        
        # self.ui.camera_list[3].mousePressEvent = self.GridFrameClicked

        self.show()


# <============================================================================ Functions ======================================================> #

    ##############################
    # Centering The Window
    ##############################
    def CenterTheWindow(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



    ##############################
    # Setting The Grid Height and Width
    ##############################
    def SetConstraintsSpecs(self):
        self.gridWidth = self.ui.main_body_content_area.width()
        self.gridHeight = self.ui.main_body_content_area.height()
        print('Width : ' + str(self.gridWidth))
        print('Height : ' + str(self.gridHeight))


        # temp vars
        newGridWidth = self.gridWidth - 60      # Padding 30 on each side
        newGridHeight = self.gridHeight - 60      # Padding 30 on each side

        tempWidth = int(newGridWidth / 2)
        tempHeight = tempWidth
        while (True):
            if (round(tempWidth/tempHeight, 2) == 1.77):    # 16:9
                break
            tempHeight -= 1
        self.gridFrameWidth = tempWidth
        self.gridFrameHeight = tempHeight

    ##############################
    # Grid Frames Click Event
    ##############################
    def GridFrameClicked(self, event):
        # print(frameName.x() + " Clicked")
        if event.buttons() == QtCore.Qt.LeftButton:
            event.accept()
            gridLayout_width = self.ui.main_body_content_area.width()
            selected_camera_width = gridLayout_width - 410   # For Padding 100
            selected_camera_height = gridLayout_width - 50
            while (True):

                if (round(selected_camera_width/selected_camera_height, 2) == 1.77):
                    break
                selected_camera_height -= 1;
            print(selected_camera_width)
            print(selected_camera_height)
            self.ui.frame_00.setMinimumSize(QtCore.QSize(selected_camera_width, selected_camera_height))
            self.ui.frame_00.setMaximumSize(QtCore.QSize(selected_camera_width, selected_camera_height))

            # # Animating The Transition
            # self.animation = QPropertyAnimation(self.ui.frame_00, b"minimSize")
            # # Animating Minimum Size
            # self.animation.setDuration(2000)
            # self.animation.setStartValue(QtCore.QSize(self.ui.frame_00.width(), self.ui.frame_00.height()))    # Start Value is the current width
            # self.animation.setEndValue(QtCore.QSize(selected_camera_width, selected_camera_height))      # End value is the new width
            # self.animation.setEasingCurve(QEasingCurve.InOutCubic)
            # self.animation.start()

            self.ui.frame_01.hide()
            self.ui.frame_10.hide()
            self.ui.frame_11.hide()
            # Get screen left menu width
            width = self.ui.status_side_menu.width()

            # IF Minimized
            if width == 0:
                # Expand Menu
                newWidth = 350
                self.ui.right_side_toggle_button_1.setIcon(QIcon(u":/icons/icons/toggle-right.svg"))
            
                # Animating The Transition
                self.animation = QPropertyAnimation(self.ui.status_side_menu, b"minimumWidth")
                # Animating Minimum Width
                self.animation.setDuration(300)
                self.animation.setStartValue(width)     # Start Value is the current width
                self.animation.setEndValue(newWidth)    # End value is the new width
                self.animation.setEasingCurve(QEasingCurve.InOutQuart)
                self.animation.start()


    ##############################
    # Creating Grid Camera Frames
    ##############################
    def createNewGridFrames(self, rowNumber, colNumber):
        # Creating New Names For Frames Of The Grid
        newName = "frame_" + str(rowNumber) + str(colNumber)
        newLabelName = "label_" + str(rowNumber) + str(colNumber)
        newVerticalLayout_cameraFrameName = "verticalLayout_cameraFrame_" + str(rowNumber) + str(colNumber)

        #####################################################################################################
        # Grid Frame
        # self.camera_frame = QtWidgets.QFrame(self.ui.main_body_content_area)
        # # self.grid_frame = QtWidgets.QFrame(self.ui.scrollAreaWidgetContents)
        # # Using setObjectName() to set the names of the new frames
        # self.camera_frame.setObjectName(newName)
        # self.camera_frame.setMinimumSize(QtCore.QSize(640, 480))
        # self.camera_frame.setMaximumSize(QtCore.QSize(640, 480))
        # self.camera_frame.setStyleSheet("background-color: #000000;\n" "border: 2px solid #008080;\n" "border-radius: 10px;")
        # self.camera_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.camera_frame.setFrameShadow(QtWidgets.QFrame.Raised)


        self.camera_frame = QtWidgets.QFrame(self.ui.main_body_content_area)
        self.camera_frame.setMinimumSize(QtCore.QSize(self.gridFrameWidth - 100, self.gridFrameHeight - 100))
        self.camera_frame.setMaximumSize(QtCore.QSize(self.gridFrameWidth, self.gridFrameHeight))
        self.camera_frame.setStyleSheet("background-color: #008080; border-radius: 10px;")
        self.camera_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.camera_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.camera_frame.setObjectName(newName)
        # Creating new attribute to UI_MainWindow
        # Syntax : setattr(obj, var, val)
        # obj : Object whose which attribute is to be assigned
        # var : Object attribute which has to be assigned
        # val : value with which variable is to be assigned
        setattr(self.ui, newName, self.camera_frame)


        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.camera_frame)
        self.verticalLayout_16.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName(newVerticalLayout_cameraFrameName)
        # Creating new attribute to UI_MainWindow
        # Syntax : setattr(obj, var, val)
        # obj : Object whose which attribute is to be assigned
        # var : Object attribute which has to be assigned
        # val : value with which variable is to be assigned
        setattr(self.ui, newVerticalLayout_cameraFrameName, self.verticalLayout_16)


        self.camera_label = QtWidgets.QLabel(self.camera_frame)
        self.camera_label.setAutoFillBackground(False)
        self.camera_label.setText("")
        self.camera_label.setTextFormat(QtCore.Qt.AutoText)
        self.camera_label.setPixmap(QtGui.QPixmap("../../Pictures/jetson nano.png"))
        self.camera_label.setAlignment(QtCore.Qt.AlignCenter)
        self.camera_label.setObjectName(newLabelName)
        self.verticalLayout_16.addWidget(self.camera_label)
        # Creating new attribute to UI_MainWindow
        # Syntax : setattr(obj, var, val)
        # obj : Object whose which attribute is to be assigned
        # var : Object attribute which has to be assigned
        # val : value with which variable is to be assigned
        setattr(self.ui, newLabelName, self.camera_label)
        
        self.ui.gridLayout.addWidget(self.camera_frame, rowNumber, colNumber, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        return newName
        #####################################################################################################
        #####################################################################################################


    ##############################
    # Creating Side Status Panel Camera Frames
    ##############################
    def createNewSideStatusPanelCameraFrames(self, index):
        # Creating New Names For Frames Of The Grid
        newNameSidePanel = "side_frame_" + str(index)
        newLabelNameSidePanel = "side_label_" + str(index)
        newVerticalLayout_cameraFrameNameSidePanel = "side_verticalLayout_cameraFrame_" + str(index)

        self.side_camera_frame = QtWidgets.QFrame(self.ui.scrollAreaWidgetContents)
        self.side_camera_frame.setMinimumSize(QtCore.QSize(0, 140))
        self.side_camera_frame.setMaximumSize(QtCore.QSize(260, 150))
        self.side_camera_frame.setStyleSheet("background-color: #008080; border-radius: 10px;")
        self.side_camera_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.side_camera_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.side_camera_frame.setObjectName(newNameSidePanel)
        # Creating new attribute to UI_MainWindow
        # Syntax : setattr(obj, var, val)
        # obj : Object whose which attribute is to be assigned
        # var : Object attribute which has to be assigned
        # val : value with which variable is to be assigned
        setattr(self.ui, newNameSidePanel, self.side_camera_frame)


        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.side_camera_frame)
        self.verticalLayout_14.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_14.setSpacing(5)
        self.verticalLayout_14.setObjectName(newVerticalLayout_cameraFrameNameSidePanel)
        # Creating new attribute to UI_MainWindow
        # Syntax : setattr(obj, var, val)
        # obj : Object whose which attribute is to be assigned
        # var : Object attribute which has to be assigned
        # val : value with which variable is to be assigned
        setattr(self.ui, newVerticalLayout_cameraFrameNameSidePanel, self.verticalLayout_14)


        self.side_camera_label = QtWidgets.QLabel(self.side_camera_frame)
        self.side_camera_label.setStyleSheet("border-radius: 10px;")
        self.side_camera_label.setText("")
        self.side_camera_label.setPixmap(QtGui.QPixmap("../../Pictures/laptop.jpg"))
        self.side_camera_label.setObjectName(newLabelNameSidePanel)
        self.verticalLayout_14.addWidget(self.side_camera_label)
        # Creating new attribute to UI_MainWindow
        # Syntax : setattr(obj, var, val)
        # obj : Object whose which attribute is to be assigned
        # var : Object attribute which has to be assigned
        # val : value with which variable is to be assigned
        setattr(self.ui, newLabelNameSidePanel, self.side_camera_label)
        self.ui.verticalLayout_13.addWidget(self.side_camera_frame, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)



    #####################################################################################################
    #####################################################################################################


    ##############################
    # Animating The Grid Frame
    ##############################    
    def animateGridFrame(self, camera_frame):
        # Animating The Transition
        self.animation = QPropertyAnimation(camera_frame, b"minimumSize")
        # Animating Minimum Size
        self.animation.setDuration(2000)
        self.animation.setStartValue(QtCore.QSize(0, 0))    # Start Value is the current width
        self.animation.setEndValue(QtCore.QSize(640, 480))      # End value is the new width
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.start()


    ##############################
    # Slide Left Menu Function
    ##############################
    def slideLeftMenu(self):
        # Get cueent left menu width
        width = self.ui.slide_menu_container.width()

        # IF Minimized
        if width == 0:
            # Expand Menu
            newWidth = 250
            self.ui.open_close_side_bar_btn.setIcon(QIcon(u":/icons/icons/chevrons-left.svg"))
            self.SetConstraintsSpecs()

        # If Maximized
        else:
            # Restore Menu
            newWidth = 0
            self.ui.open_close_side_bar_btn.setIcon(QIcon(u":/icons/icons/menu.svg"))
            self.SetConstraintsSpecs()
        
        # Animating The Transition
        self.animation = QPropertyAnimation(self.ui.slide_menu_container, b"minimumWidth")
        # Animating Minimum Width
        self.animation.setDuration(250)
        self.animation.setStartValue(width)     # Start Value is the current width
        self.animation.setEndValue(newWidth)    # End value is the new width
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()
    ##############################


    ##############################
    # Slide Right Menu Function
    ##############################
    def slideRightMenu(self):
        # Get cueent left menu width
        width = self.ui.status_side_menu.width()

        # IF Minimized
        if width == 0:
            # Expand Menu
            newWidth = 350
            self.ui.right_side_toggle_button_1.setIcon(QIcon(u":/icons/icons/toggle-right.svg"))

        # If Maximized
        else:
            # Restore Menu
            newWidth = 0
            self.ui.right_side_toggle_button_1.setIcon(QIcon(u":/icons/icons/toggle-left.svg"))
        
        # Animating The Transition
        self.animation = QPropertyAnimation(self.ui.status_side_menu, b"minimumWidth")
        # Animating Minimum Width
        self.animation.setDuration(300)
        self.animation.setStartValue(width)     # Start Value is the current width
        self.animation.setEndValue(newWidth)    # End value is the new width
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()
    ##############################



    ##############################
    # Slide Right Menu Function
    ##############################
    def enableAllCamerasGridView(self):
        # Get cueent left menu width
        width = self.ui.status_side_menu.width()

        # IF Minimized
        if width == 0:
            # Expand Menu
            newWidth = 350
            self.ui.right_side_toggle_button_1.setIcon(QIcon(u":/icons/icons/toggle-right.svg"))

        # If Maximized
        else:
            # Restore Menu
            newWidth = 0
            self.ui.right_side_toggle_button_1.setIcon(QIcon(u":/icons/icons/toggle-left.svg"))
        
        # Animating The Transition
        self.animation = QPropertyAnimation(self.ui.status_side_menu, b"minimumWidth")
        # Animating Minimum Width
        self.animation.setDuration(300)
        self.animation.setStartValue(width)     # Start Value is the current width
        self.animation.setEndValue(newWidth)    # End value is the new width
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()
        
        self.ui.frame_00.show()
        self.ui.frame_01.show()
        self.ui.frame_10.show()
        self.ui.frame_11.show()
    ##############################

    
    ##############################
    # Update Restore Button icon or Maximizing or Minimizing Window
    ##############################
    def restore_or_maximize_window(self):
        # If Window Is Maximized
        if self.isMaximized():
            self.showNormal()
            # Change Icon
            self.ui.restore_window_button.setIcon(QIcon(":/icons/icons/maximize.svg"))

        else:
            self.showMaximized()
            # Changing Icon
            self.ui.restore_window_button.setIcon(QIcon(":/icons/icons/minimize-2.svg"))
    ##############################


    ##############################
    # Maximizing The Window
    ##############################
    def MaximizeWindow(self):
        self.showFullScreen()
    ##############################


    ##############################
    # Add Mouse Evenrs To The Window
    ##############################
    def mousePressEvent(self, event):
        # Get the current position of the mouse
        self.clickPosition = event.globalPos()
        # We will use this value to mobe the window
    ##############################


# Execute App
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    ## Screen Size Getting
    screen = app.primaryScreen()
    size = screen.size()
    global rect
    rect = screen.availableGeometry()
    print('Available: %d x %d' % (rect.width(), rect.height()))

    ## Camera List
    global camera_list
    camera_list = []

    window = MainWindow()


    sys.exit(app.exec_())