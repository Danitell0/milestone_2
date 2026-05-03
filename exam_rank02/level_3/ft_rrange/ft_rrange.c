#include <stdio.h>
#include <stdlib.h>

int	*ft_rrange(int start, int end)
{
	int	i;
	int	size;
	int *result;

	i = 0;
	if (start <= end)
	{
		size = end - start + 1;
		result = (int *)malloc(size * sizeof(int));
		while (i < size)
			result[i++] = end--;
	}
	else if (start > end)
	{
		size = start - end + 1;
		result = (int *)malloc(size * sizeof(int));
		while (i < size)
			result[i++] = end++;
	}
	return (result);
}

int	main(void)
{
	int	*arr;
	int	i;

	i = 0;
	arr = ft_rrange(3, -1);
	while (i < 5)
	{
		printf("%i\n", arr[i]);
		i++;
	}
}
