import database

database.databaseStartup()

boolvar, strvar = database.register('thomas', '1223334444')
print(boolvar, strvar)
boolvar, strvar = database.register('abdulla', '55555666666')
print(boolvar, strvar)


boolvar, strvar = database.register('thomas', '1223334444')
print(boolvar, strvar)
boolvar, strvar = database.register('thomas', '1')
print(boolvar, strvar)

