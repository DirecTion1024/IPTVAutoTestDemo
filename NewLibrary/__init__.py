from myclass import MyClass
from robot.libraries.OperatingSystem import OperatingSystem

class NewLibrary(MyClass):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    def __init__(self, timeout=5, run_on_failure='Capture Page Screenshot'):
        MyClass.__init__(self, timeout, run_on_failure)