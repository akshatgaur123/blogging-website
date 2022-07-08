def find_hash(comment,h):
	words=comment.split()
	i=0
	array=[]
	while i<len(words):
		x=words[i]
		y=x.split(h)
		if len(y)==1:
			pass
		else:
			j=1
			while j<len(y):
				if y[j]!='':
					array.append(y[j])
				j=j+1
		i=i+1
	return array


s='what are you #stupidity #insaniuty jcgh#ffjug#'

print(find_hash(s,'#'))


