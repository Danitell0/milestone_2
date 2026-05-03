#include <stdio.h>

size_t	ft_strcspn(const char *s, const char *reject)
{
	int		i;
	int		j;
	size_t	len;

	i = 0;
	len = 0;
	while (s[i])
	{
		j = 0;
		while (reject[j])
		{
			if (s[i] == reject[j])
				return (len);
			j++;
		}
		len++;
		i++;
	}
	return (len);
}

int	main(void)
{
	printf("%zu\n", ft_strcspn("hello world", "eo"));
}
