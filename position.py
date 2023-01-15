# position on the map
class Position:
    __x = 0
    __y = 0

    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def get_coordinate(self):
        return self.__x, self.__y

    def __str__(self):
        return 'x=%d y=%d' % (self.__x, self.__y)

    def __eq__(self, other):
        return self.__x == other.__x and self.__y == other.__y

    def __hash__(self):
        return hash((self.__x, self.__y))



