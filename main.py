import loginWindow
import database
import graphWindow

database.databaseStartup()
loginWin = loginWindow.LoginWindow()
if loginWin.logged_in:
    graphWindow.GraphWindow()
exit()
