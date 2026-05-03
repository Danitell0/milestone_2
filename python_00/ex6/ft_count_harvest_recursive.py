def ft_count_harvest_recursive():
	days = int(input("Days until harvest: "))
	def print_day(x_day, total):
		if x_day > total:
			print("Harvest time!")
			return
		print(f"Day {x_day}")
		print_day(x_day + 1, total)
	print_day(1, days)
