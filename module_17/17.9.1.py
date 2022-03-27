array = [int(x) for x in input("Введите последовательность чисел через пробел: ").split()]

for i in range(len(array)):
    for j in range(len(array)-i-1):
        if array[j] > array[j+1]:
            array[j], array[j+1] = array[j+1], array[j]


def binary_search(array, element, left, right):
    if left > right:
        return False

    middle = (right + left) // 2
    if array[middle] == element:
        return middle
    elif element < array[middle]:
        return binary_search(array, element, left, middle - 1)
    else:
        return binary_search(array, element, middle + 1, right)


while True:
    try:
        element = int(input("Введите число, которое больше 0, но меньше 1000: "))
        if element < 0 or element > 999:
            raise Exception
        break
    except ValueError:
        print("Нужно ввести число!")
    except Exception:
        print("Неправильный диапазон, попробуйте ещё!")


array.append(element)
array.sort()
print(array)
x = binary_search(array, element, 0, len(array)) 
if x - 1 < 0:
    print(0)
else:
    print(x - 1)
