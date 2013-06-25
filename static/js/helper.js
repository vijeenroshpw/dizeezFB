function getOptionNames( model) {
	var cl = model.get('choice_list');
	return {'opt0':disnames[cl[0]-1],'opt1':disnames[cl[1]-1],'opt2':disnames[cl[2]-1],'opt3':disnames[cl[3]-1],'opt4':disnames[cl[4]-1]};
	}
	
