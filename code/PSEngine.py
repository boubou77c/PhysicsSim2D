
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor
class PhysiqueSimulator(QWidget):
    def __init__(self,main_window):
        super().__init__()
        self.main_window = main_window
        self.setFixedSize(1030,1000)

        # Spawn x pos
        self.x:float = 1.0
        # Spawn y pos
        self.y:float = 1.0

        # Initial speed x / y
        self.speed_x:float = 0.0
        self.speed_y = 0.0

        # Acceleration x / y
        self.ax = 0.0
        self.ay:float = 9.8

        # Delta time
        self.t:float = 0.10

        # New position
        self.positions:list = []

        # friction
        self.friction:float = 0.10
        #coef de restitution
        self.e:float = 0.8

        #Ball size
        self.radius:int = 7

    #Show information X / Y of the ball
    def show_information(self):
        self.main_window.xLabel.setText(f"X : {round(self.x,1)}")
        self.main_window.yLabel.setText(f"Y : {round(self.y,1)}")

    #Update the setting
    def set_simulation_params(self, dTime:float, friction:float, ispX:float, ispY:float,gravity:float,restitution:float):

        self.t = dTime
        self.friction = friction
        self.speed_x = ispX
        self.speed_y = ispY
        self.ay = gravity
        self.e = restitution


    #Update the position of the ball with the Newton law
    def update_pos(self):
        if(self.main_window.dragRB.isChecked() !=True):
            self.positions.clear()
        
        #z = z + accz * tmp
        self.x = self.x + self.speed_x * self.t
        self.y = self.y + self.speed_y * self.t

        # vf = vi + (acc * tmp).
        self.speed_x = self.speed_x + self.ax * self.t
        self.speed_y = self.speed_y + self.ay * self.t

        #if the system touch the ground
        if self.y >= 565:

            self.y = 550
            self.speed_y = -self.e * self.speed_y
            self.speed_x = self.speed_x * (1 - self.friction)


        #If the system touche the celling
        if self.y < 0:
            self.y =1
            self.speed_y = -self.speed_y * (1 - self.friction)

        #If the system touch the left wall
        if self.x <= self.radius:
            self.x = 1 + self.radius

            self.speed_x = -self.e * self.speed_x


        #If the system touch the right wall
        if self.x >= 1030 - self.radius:

            self.x = 1030 - self.radius
            self.speed_x = -self.e * self.speed_x



        #Add the new position
        self.positions.append((self.x, self.y))

        self.show_information()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QColor(255, 0, 0))
        painter.fillRect(self.rect(), QColor(255, 255, 255))
        try:
            #Draw the ball with its position
            for pos in self.positions:

                x = int(pos[0])
                y = int(pos[1])

                painter.drawEllipse(x, y, self.radius, self.radius)
        except OverflowError as e:
            self.positions.clear()
            print(e)
