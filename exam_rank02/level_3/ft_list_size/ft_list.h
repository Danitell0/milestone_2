#IFNDEF FT_LIST_H
# DEFINE FT_LIST_H

typedef struct	s_list
{
	struct s_list	*next;
	void			*data;
}					t_list;

#ENDIF
