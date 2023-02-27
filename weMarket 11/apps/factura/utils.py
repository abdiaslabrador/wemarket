import random
import string

def code_generator(size=7, chars=string.ascii_lowercase+string.digits): #string.ascii_lowercase+string.digits
	code_generated=''
	for _ in range(size):
		code_generated+=random.choice(chars)
	return code_generated

#investigar sobre permutaciones con repeticion
def code_created(instance, size=7): 
	code_generated = code_generator(size=size)
	Klass = instance.__class__
	exist = Klass.objects.filter(id_codigo_retiro=code_generated).exists()

	if exist:
		return code_created(size=size)

	return code_generated
