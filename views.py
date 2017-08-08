from django.shortcuts import render, HttpResponse, get_object_or_404
from django.template import loader, Context
from .models import Node, NodeDevice, RadioMsg, ndDetail


# Create your views here.
def index(request):
  node_list = Node.objects.all()
  context = {
        'node_list': node_list,
    }
  return render(request, 'nodectl/index.html', context)
    
def node(request, node_id):
  node = get_object_or_404(Node, pk=node_id)
  node_devices = NodeDevice.objects.all().filter(node_id = node.id)

  return render(request, 'nodectl/node.html', {'node': node, 'nodedevices': node_devices})
  
def on_mqtt_message(client, userdata, msg):
  """This procedure is called each time a mqtt message is received"""
  mqttlist['1'] = msg.payload

def nodedevice(request, nodedevice_id):
  import paho.mqtt.client as mqtt

  mqttlist = []
  mclient = mqtt.Client(userdata = mqttlist)
  #mclient.on_connect = on_connect
  mclient.on_message = on_mqtt_message
  mclient.connect("127.0.0.1", 1883, 60)
  mclient.subscribe('house/toyota/toyotaswitch/1/I')
  mclient.loop(timeout=1.0, max_packets=1)
  mclient.disconnect()


  # get the nodedevice object
  nodedevice = get_object_or_404(NodeDevice, pk=nodedevice_id)
  c = Context({'nodedevice': nodedevice})
  
  # get any info details for the nd
  ndInfo = ndDetail.objects.filter(nd_id=nodedevice_id).filter(detail_type = 'I')
  c['ndInfo'] = ndInfo
  
  # get any param details for the nd
  ndParam = ndDetail.objects.filter(nd_id=nodedevice_id).filter(detail_type = 'P')
  c['ndParam'] = ndParam
  
  c['mqtt'] = mqttlist  
  
  # get last radio messages 
  sql = "SELECT * from radio_msg WHERE nodeID = {} AND deviceID = {} ORDER BY dt DESC \
      LIMIT 15".format(nodedevice.node_id.node, nodedevice.device_id.device_id)
  c['sql'] =sql
  radio_list = RadioMsg.objects.raw(sql)
  
  c['radiolist'] = radio_list
  return render(request, 'nodectl/nodedevice.html', c)