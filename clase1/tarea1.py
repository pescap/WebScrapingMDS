import requests
import time

def request_uf():
	#Retorna Uf diaria
	try:
		response = requests.get("https://mindicador.cl/api")
		uf = response.json()["uf"]["valor"]
		return uf
	except:
	# Trata de nuevo el 10 seg.
	time.sleep(10)
	return request_uf()
	