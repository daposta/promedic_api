from .models import Responder


def generate_responder_serial():
	check_serial = Responder.objects.all().exists()
	serial = None
	if check_serial:
		serial = str(int(Responder.objects.latest('pk').serial_num)+1)
		if len(str(serial)) ==1:
			serial = '00' + str(serial)
		elif len(str(serial)) ==2:
			serial = '0' + str(serial)
		elif len(str(serial)) ==3:
			serial = str(serial)
		
	else:
		serial = "001"
	return serial


