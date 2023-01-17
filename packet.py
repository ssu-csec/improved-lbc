import core

def unpacking(data, info):
	
	data.global_meta = info.glob_list
	for del_index in del_list:
		del data.data[del_index]
	ins_index = info.ins_list.pop(0)
	data.data = data.data[:ins_index] + info.ins_list + data.data[ins_index:]

	
