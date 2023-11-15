from hashlib import blake2b
import time 

def hash_string(string, digest_size=2):
	return blake2b(key=bytes(string, encoding='utf-8'), digest_size=digest_size).hexdigest()

def hash_output_name(image_path, format):
	return hash_string(str(int(time.time()))) +'.'+ format

def img_output_name(image_path, format,output_name=None):
	
	if output_name == None:
		return hash_output_name(image_path,format)
	else:
		if output_name.split('.')[-1] != format:
			return output_name +'.'+format

		return output_name