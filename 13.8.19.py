tickets = int(input("Введите количество билетов: "))
s = 0.0 #общая стоимость билетов
for i in range(tickets):
    age = int(input("Укажите возраст каждого посетителя: "))
    if age < 18:
        s += 0
    elif 18 <= age < 25:
        s += 990
    else: s += 1390
if tickets > 3:
    s *= 0.9
print("Сумма к оплате", s, "рублей")