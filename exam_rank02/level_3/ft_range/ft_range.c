int	*ft_range(int start, int end)
{
	int	i;
	int	*result;
	int	size;

	i = start;
	if (start > end)
		size = start - end + 1;
	else
		size = end - start + 1;
	result = (int *)malloc(size * sizeof(int));
	i = 0;
	if (start > end)
		while (start >= end)
			result[i++] = start--;
	else
		while (start <= end)
			result[i++] = start++;
	return (result);
}

