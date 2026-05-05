#include <stdio.h>

int	ft_atoi_base(const char *str, int str_base)
{
	int	result;
	int	is_neg;
	int	i;

	result = 0;
	is_neg = 1;
	i = 0;
	if (str[i] == '-')
	{
		is_neg = -1;
		i++;
	}
	while (str[i])
	{
		if (str[i] >= '0' && str[i] <= '9')
			result = result * str_base + str[i] - '0';
		else if (str[i] >= 'A' && str[i] <= 'F')
			result = result * str_base + str[i] - 'A' + 10;
		else if (str[i] >= 'a' && str[i] <= 'f')
			result = result * str_base + str[i] - 'a' + 10;
		i++;
	}
	return (is_neg * result);
}

int	main(void)
{
	printf("%d\n", ft_atoi_base("-aa", 16));
}
