''' Создайте класс любых геометрических фигур, где на выход 
мы получаем характеристики фигуры. Каждый экземпляр должен
 иметь атрибуты, которые зависят от выбранной фигуры. 
 Например, для прямоугольника это будут аргументы x, y, width и height.'''

class GeometricFigure():
    def __init__(self,width, height ):
        self.x = width
        self.y = height

    def Parameters(self):
        return f"width = {self.x} height = {self.y}"

n = GeometricFigure(10, 20)
print(n.Parameters())