import importlib
import os

from goods.libs.html import Html


class Application:
    @staticmethod
    def init(moduleName,className,methodName):
        projectName = os.path.basename(os.getcwd())
        module = projectName+"."+"modules"+"."+moduleName+"."+"controller."+className
        try:
            controller = importlib.import_module(module)
        except Exception :
            return Html.render("/404.html")
        try:
            classInstance = getattr(controller, className)
        except Exception :
            return Html.render("/404.html")
        try:
            funcName = getattr(classInstance(), methodName)
            return funcName()
        except Exception :
            return Html.render("/404.html")
