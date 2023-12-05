from decimal import Decimal, ROUND_HALF_UP

# Ваше исходное число
number = Decimal('3.141592623424')

# Округление до 10 знаков после запятой с использованием математического округления
rounded_number = number.quantize(Decimal('0.0000000001'), rounding=ROUND_HALF_UP)

formatted_result = "{:,.6f}".format(rounded_number)
formatted_result.replace(',', ' ').rstrip('0').rstrip('.')

print(isinstance(rounded_number, str))