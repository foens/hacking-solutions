main()
{
	char* filename[64];
	char* buf[64];
	int var_ac = 0;
	...
	
	memset(filename, 0, 64);
	
	while(var_ac <= 62)
	{
		char current_char = getchar();
		if(current_char != '1' && current_char != '0')
		{
			break;
		} else if(current_char == '1')
		{
			int eax = var_ac;
			int edx = var_ac+7;
			if(eax < 0)
			{
				eax = edx;
			}
			eax /= 8;
			filename[?] = ?;
		}
		var_ac++;
	}
	
	fd = open(filename, 0);
	if(fd != 0)
	{
		while(1)
		{
			var_ac = _read(fd, buf, 64);
			if(var_ac == 0)
				break;
			write(1, buf, var_ac);
		}
		close(fd);
	}
}