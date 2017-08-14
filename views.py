from django.shortcuts import render, HttpResponse, get_object_or_404
from django.template import loader, Context
from .models import Node, NodeDevice, RadioMsg, ndDetail
from .forms import NodeDeviceSetForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
  
global mqttlist

# Create your views here.

# ********************************************************************
def index(request):
  """ This provides the data for the initial index screen
  """
  node_list = Node.objects.all()
  context = {'node_list': node_list}
  return render(request, 'nodectl/index.html', context)

# ********************************************************************    
def node(request, node_id):
  node = get_object_or_404(Node, pk=node_id)
  node_devices = NodeDevice.objects.all().filter(node_id = node.id)
  cSql = "SELECT * from radio_msg WHERE nodeID = {} ORDER BY dt \
      DESC LIMIT 1".format(node.node)
  r = RadioMsg.objects.raw(cSql)
  if r[0] is not None:
    node.last_status = r[0].dt
    node.save()

  return render(request, 'nodectl/node.html', {'node': node, 'nodedevices': node_devices})
  
def on_mqtt_message(client, userdata, msg):
  """This procedure is called each time a mqtt message is received"""
  mqttlist.append(msg.payload)
  print('got a message')

# ********************************************************************
def on_mqtt_connect(client, userdata, flags, rc):
    """This procedure is called on connection to the mqtt broker"""
    client.subscribe("house/#")
    
  

def nodedevice(request, nodedevice_id):
  """
  """

  mqttlist = list()
  client = mqtt.Client()
  client.on_connect = on_mqtt_connect
  client.on_message = on_mqtt_message
  client.connect("127.0.0.1", 1883, 60)
  #client.subscribe("house/#")
  client.loop(timeout=1.0)

  # get the nodedevice object
  nodedevice = get_object_or_404(NodeDevice, pk=nodedevice_id)
  c = Context({'nodedevice': nodedevice})
  c['mqtt_topic'] = nodedevice.mqtt_topic()
  
  # get any info details for the nd
  ndInfo = ndDetail.objects.filter(nd_id=nodedevice_id).filter(detail_type = 'I')
  c['ndInfo'] = ndInfo
  
  # get any param details for the nd
  ndParam = ndDetail.objects.filter(nd_id=nodedevice_id).filter(detail_type = 'P')
  for p in ndParam:
    cSql = "SELECT * from radio_msg WHERE nodeID = {} AND deviceID = {} AND instance = {} \
        AND action = 'R' ORDER BY dt DESC LIMIT 1".format(nodedevice.node_id.node, \
        nodedevice.device_id.device_id, nodedevice.instance)
    r = RadioMsg.objects.raw(cSql)
    for r1 in r:
    #if r is not None:
      if p.detail_posn == 1:
        p.reported_value = r1.float_1
      elif p.detail_posn == 2:
        p.reported_value = r1.float_2
      break
    #p.save()
  
  
  c['ndParam'] = ndParam
  
  c['mqtt'] = mqttlist  
  
  # get last radio messages 
  sql = "SELECT * from radio_msg WHERE nodeID = {} AND deviceID = {} ORDER BY dt DESC \
      LIMIT 15".format(nodedevice.node_id.node, nodedevice.device_id.device_id)
  c['sql'] =sql
  radio_list = RadioMsg.objects.raw(sql)
  
  c['radiolist'] = radio_list
  client.disconnect()
  return render(request, 'nodectl/nodedevice.html', c)
  
# ********************************************************************
def nodedeviceset(request, ndDetail_id):
  ndParam = ndDetail.objects.get(id=ndDetail_id)
  jErrorMsg = ''
 
  client = mqtt.Client()
  #client.on_connect = on_mqtt_connect
  #client.on_message = on_mqtt_message
  client.connect("127.0.0.1", 1883, 60)

  if request.method == 'POST':
    form = NodeDeviceSetForm(request.POST, instance = ndParam)
  
    if form.is_valid():
      if form.cleaned_data['req_value'] < ndParam.min_value:
        jErrorMsg = "Parameter cannot be less than {}".format(ndParam.min_value)
      elif form.cleaned_data['req_value'] > ndParam.max_value:
        jErrorMsg = "Parameter cannot be more than {}".format(ndParam.max_value)
      else:
        form.save()
        topic = "{}/P".format(ndParam.nd_id.mqtt_topic())
        payload = json.dumps({ndParam.detail_text: form.cleaned_data['req_value']})
        print(ndParam.nd_id.mqtt_topic())
        publish.single(topic, payload)
        client.disconnect() 
        return HttpResponseRedirect(reverse('nodectl:nodedevice', \
          args=(ndParam.nd_id.id,)))
      form.req_value.error = jErrorMsg
  else:
    form = NodeDeviceSetForm()
 
  c = Context({'form': form})
  c['ndDetail'] = ndParam
  c['error_message'] = jErrorMsg
  
  c['explain'] = "{}  Minimum value is {}, max value is {}".format(ndParam.detail_descr,\
    ndParam.min_value, ndParam.max_value)
  client.disconnect() 
  return render(request, 'nodectl/nodedeviceset.html', c)

