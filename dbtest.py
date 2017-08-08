
from models import Node, NodeDevice, RadioMsg


nodedevice = get_object_or_404(NodeDevice, pk=8)
radio_list = RadioMsg.objects.raw('SELECT * FROM radio_msg WHERE nodeID = 4 AND deviceID = 32 LIMIT 5')
for r in radio_List:
  print r.dt

