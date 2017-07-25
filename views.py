from django.shortcuts import render, HttpResponse, get_object_or_404
from django.template import loader
from .models import Node, NodeDevice

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