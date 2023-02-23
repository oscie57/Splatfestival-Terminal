import sys, os, json
from PySide6.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMessageBox, QHBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from download import download, fesdata, gamedata

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("Splatfestival Terminal")
        self.setFixedSize(450, 600)

        if "data" not in os.listdir('./'):
            self.download_files()

        self.fesdata = self.get_fesdata()

        self.paneltext1 = QLabel(f"{self.fesdata['Teams'][0]['Name']} vs {self.fesdata['Teams'][1]['Name']}", self)
        self.paneltext_startdate = QLabel(self.fesdata['TimeStart'], self)
        self.paneltext_enddate = QLabel(self.fesdata['TimeEnd'], self)

        panel = QImage(f"./data/Panel_{self.fesdata['FestivalId']}.png")

        panelpixmap = QPixmap.fromImage(panel)
        smaller_pixmap = panelpixmap.scaled(450, 450, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.imageLabel = QLabel()
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setPixmap(smaller_pixmap)

        self.stage1 = StageListing(f'./img/stages/{self.fesdata["Stages"][0]}.png', gamedata("stage", self.fesdata["Stages"][0]), 0.6)
        self.stage2 = StageListing(f'./img/stages/{self.fesdata["Stages"][1]}.png', gamedata("stage", self.fesdata["Stages"][1]), 0.6)
        self.stage3 = StageListing(f'./img/stages/{self.fesdata["Stages"][2]}.png', gamedata("stage", self.fesdata["Stages"][2]), 0.6)

        self.rulesinfo = DisplayRule(f'./img/rules/{self.fesdata["Rule"]}.png', gamedata("rule", self.fesdata["Rule"]), 2.0)

        self.button_update = QPushButton("Update Files", self)
        self.button_update.setFixedSize(200, 30)

        self.button_info = QPushButton("🛈", self)
        self.button_info.setFixedSize(30, 30)

        self.main_layout = QVBoxLayout(self)

        # define layouts 

        self.layout_middle_paneltext = QVBoxLayout(self)
        self.layout_middle_panel = QVBoxLayout(self)
        self.layout_middle_stages = QHBoxLayout(self)
        self.layout_middle_buttons = QHBoxLayout(self)

        self.layout_center_stages = QVBoxLayout(self)
        self.layout_center_rules = QVBoxLayout(self)

        self.layout_top_paneltext_top = QVBoxLayout(self)
        self.layout_top_paneltext_dates = QHBoxLayout(self)

        # add widgets to layouts

        self.layout_top_paneltext_top.addWidget(self.paneltext1, alignment=Qt.AlignCenter)

        self.layout_top_paneltext_dates.addWidget(self.paneltext_startdate)
        self.layout_top_paneltext_dates.addStretch(1)
        self.layout_top_paneltext_dates.addWidget(self.paneltext_enddate)

        self.layout_middle_panel.addWidget(self.imageLabel)

        self.layout_center_stages.setSpacing(0)
        self.layout_center_stages.addWidget(self.stage1)
        self.layout_center_stages.addWidget(self.stage2)
        self.layout_center_stages.addWidget(self.stage3)

        self.layout_center_rules.addWidget(self.rulesinfo, alignment=Qt.AlignCenter)

        self.layout_middle_buttons.addWidget(self.button_info, alignment=Qt.AlignRight | Qt.AlignBottom)
        self.layout_middle_buttons.addWidget(self.button_update, alignment=Qt.AlignRight | Qt.AlignBottom)

        # add layouts to outer layout

        self.main_layout.addLayout(self.layout_middle_paneltext)
        self.main_layout.addLayout(self.layout_middle_panel)
        self.main_layout.addLayout(self.layout_middle_stages)
        self.main_layout.addLayout(self.layout_middle_buttons)

        self.layout_middle_paneltext.addLayout(self.layout_top_paneltext_top)
        self.layout_middle_paneltext.addLayout(self.layout_top_paneltext_dates)

        self.layout_middle_stages.addLayout(self.layout_center_stages)
        self.layout_middle_stages.addLayout(self.layout_center_rules)

        # control buttons

        self.button_update.clicked.connect(self.download_files)
        self.button_info.clicked.connect(self.info_box)

    def info_box(self):
        """Show info box"""

        QMessageBox.information(self, "Info", "This program was made by oscie57.\nLayout inspired by ShadowDoggo's FesTWO Terminal.\nThis program is not affiliated with Nintendo or Splatfestival.\nGraphics from Nintendo and Splatfestival.\nPyQt6 support from Fashoomp#9015 (143878644169834496).")

    def download_files(self):
        
        if "data" in os.listdir("./"):
            os.system("rmdir /s /q data")
        
        download()
        fesdata()

        QMessageBox.information(self, "Downloaded Files", "Restart the application to view the\nlatest Splatfest information.")

    def get_fesdata(self):

        with open('./data/FesData.json', 'r') as f:
            fesdata = json.load(f)

        return fesdata

class StageListing(QWidget):

    def __init__(self, image, text, resize=1.0):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.setFixedWidth(225)
        self.layout.setContentsMargins(0, 2, 2, 2)

        self.stagename = QLabel(text.replace(" ", "\n"))
        
        panel = QPixmap(image)
        w, h = panel.size().width(), panel.size().height()
        scaled_img = panel.scaled(w * resize, h * resize, Qt.KeepAspectRatio)
        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(scaled_img)

        self.layout.addWidget(self.imageLabel)
        self.layout.addWidget(self.stagename)

class DisplayRule(QWidget):

    def __init__(self, image, text, resize = 1.0):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setFixedWidth(225)
        #self.layout.setContentsMargins(0, 2, 2, 2)

        self.ruletext = QLabel(text)

        image = QPixmap(image)
        w, h = image.size().width(), image.size().height()
        scaled_img = image.scaled(w * resize, h * resize, Qt.KeepAspectRatio)
        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(scaled_img)

        self.layout.addWidget(self.imageLabel, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.ruletext, alignment=Qt.AlignCenter)

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec())