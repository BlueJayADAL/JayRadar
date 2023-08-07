from networktables import NetworkTables


NetworkTables.initialize()

nt = NetworkTables.getTable("JayRadar")


def value_changed(table, key, value, isNew):
    print()
    print('Update to the JayRadar table found!')
    print(f'Key: {key}, Value: {value}, IsNew: {isNew}')
    print()


nt.addEntryListener(value_changed)

while True:
    pass
