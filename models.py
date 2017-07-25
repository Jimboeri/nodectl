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
    node = Node.objects.get(id=1)
    return '{} - {}'.format(self.node_id.descr, self.device_id.name)
    
class RadioMsg(models.Model):
  ID       = models.IntegerKey(primary_key=True)
  dt       = models.DateTimeField()
  nodeID   = models.ForeignKey(Node)
  deviceID = models.ForeignKey(Device)
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
