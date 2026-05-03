#include "flood_fill.h"

void	fill(char **area, t_point size, t_point vec, char target)
{
	if (vec.y < 0 ||  vec.y >= size.y || vec.x < 0 || vec.x >= size.x
		|| area[vec.y][vec.x] != target)
		return ;
	area[vec.y][vec.x] = 'F';
	fill(area, size, (t_point){vec.x - 1, vec.y}, target);
	fill(area, size, (t_point){vec.x + 1, vec.y}, target);
	fill(area, size, (t_point){vec.x, vec.y - 1}, target);
	fill(area, size, (t_point){vec.x, vec.y + 1}, target);
}

void	flood_fill(char **area, t_point size, t_point begin)
{
	char	target;

	target = area[begin.y][begin.x];
	fill(area, size, begin, target);
}
