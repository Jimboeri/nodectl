from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Class_type(models.Model):
  descr        = models.CharField(max_length=200)

  def __str__(self):
    return self.descr


class Node(models.Model):
  descr        = models.CharField(max_length=200)
  first_active = models.DateTimeField('Date first seen active')
  last_active  = models.DateTimeField('Date and time of last activity')
  node         = models.IntegerField()
  mqtt_topic   = models.CharField(max_length=100)
  last_status  = models.CharField(max_length=200)

  def __str__(self):
    return self.descr

  
class Device(models.Model):
  name         = models.CharField(max_length=30)
  device_id    = models.IntegerField(default=0)
  descr        = models.CharField(max_length=200)
  class_id     = models.ForeignKey(Class_type)
  info_float1  = models.CharField(max_length=30)
  info_float2  = models.CharField(max_length=30)
  info_float3  = models.CharField(max_length=30)
  info_float4  = models.CharField(max_length=30)

  def __str__(self):
    return self.name

  
class NodeDevice(models.Model):
  node_id      = models.ForeignKey(Node)
  device_id    = models.ForeignKey(Device)
  instance     = models.IntegerField()
  last_status  = models.CharField(max_length=200)
  
  def __str__(self):
    #node = Node.objects.get(id=1)
    return '{} - {}'.format(self.node_id.descr, self.device_id.name)
    
  def mqtt_topic(self):
    return("{}/{}/{}".format(self.node_id.mqtt_topic, \
      self.device_id.name, self.instance))
    
class ndDetail(models.Model):
  nd_id          = models.ForeignKey(NodeDevice)
  detail_type    = models.CharField(max_length=1)
  detail_posn    = models.IntegerField(default=1)
  detail_text    = models.CharField(max_length=30)
  detail_descr   = models.CharField(max_length=200)
  req_value      = models.FloatField(help_text="This value will be sent to the target node as a parameter update")
  reported_value = models.FloatField()
  last_update    = models.DateTimeField()
  min_value      = models.FloatField(null=True)
  max_value      = models.FloatField(null=True)
  
  def __str__(self):
    return "{} - {} - {} - {}".format(self.nd_id.node_id.descr, self.nd_id.device_id.name,\
      self.detail_type, self.detail_text)
    
class RadioMsg(models.Model):
  ID       = models.IntegerField(primary_key=True)
  dt       = models.DateTimeField()
  nodeID   = models.IntegerField()
  deviceID = models.IntegerField()
  instance = models.IntegerField()
  action   = models.CharField(max_length=1)
  result   = models.IntegerField()
  float_1  = models.FloatField()
  float_2  = models.FloatField()
  float_3  = models.FloatField()
  float_4  = models.FloatField()
  tx_rx    = models.CharField(max_length=1)
  RSSI     = models.FloatField()
  req_id   = models.BigIntegerField()
  
  class Meta:
    db_table = "radio_msg"
    managed=False
    
