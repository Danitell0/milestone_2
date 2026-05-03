#include <stdlib.h>
#include <stdio.h>

int	count_digits(int nbr)
{
	int	len;

	len = 0;
	if (nbr < 0)
		nbr = -nbr;
	else if (nbr == 0)
		return (1);
	while (nbr > 0)
	{
		nbr /= 10;
		len++;
	}
	return (len);
}

char	*ft_itoa(int nbr)
{
	char	*result;
	int		size;
	int		is_neg;

	is_neg = 0;
	size = count_digits(nbr);
	if (nbr < 0)
	{
		nbr = -nbr;
		size += 1;
		is_neg += 1;
	}
	result = (char *)malloc((size + 1) * sizeof(char));
	if (nbr == 0)
	{
		result[0] = '0';
		result[1] = '\0';
		return (result);
	}
	result[size] = '\0';
	while (nbr)
	{
		result[--size] = nbr % 10 + '0';
		nbr /= 10;
	}
	if (is_neg)
		result[0] = '-';
	return (result);
}

int	main(void)
{
	printf("%s\n", ft_itoa(0));
}
