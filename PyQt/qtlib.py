import sys
QT_LIB = None
lib_order = ['PyQt5', 'PyQt4']
for lib in lib_order:
    if lib in sys.modules:
        QT_LIB = lib
        break

if QT_LIB is None:
    for lib in lib_order:
        try:
            __import__(lib)
            QT_LIB = lib
            break
        except ImportError:
            pass

if QT_LIB is None:
    raise ImportError("PyQt4 or PyQt5 could not be imported.")