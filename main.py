import loginWindow
import database
import graphWindow

database.database_startup()
loginWin = loginWindow.LoginWindow()
if loginWin.logged_in:
    graphWindow.GraphWindow()
exit()
