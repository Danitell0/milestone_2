#ifndef FLOOD_FILL_H
# define FLOOD_FILL_H

typedef struct	s_point
{
	int		x;
	int		y;
}			t_point;

void	fill(char **area, t_point size, t_point vec, char target);
void	flood_fill(char **area, t_point size, t_point begin);

#endif
