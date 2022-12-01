
class MqttService:

  def connect_and_subscribe(self):
    import ssl
    global mqtt_client_id, mqtt_server, mqtt_port, mqtt_user, mqtt_pass, mqtt_topic_sub, mqtt_keepalive, mqtt_ssl, debug_mode
    try:
      client = MQTTClient(mqtt_client_id, mqtt_server, port=mqtt_port, user=mqtt_user, password=mqtt_pass, keepalive=mqtt_keepalive, ssl=mqtt_ssl)
      client.set_callback(self.new_message_handler)
      client.connect()
      client.subscribe(mqtt_topic_sub)
      if debug_mode: print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, mqtt_topic_sub))
      return client
    except Exception as exception:
      if debug_mode: print('Connect and subscribe handler exception: ' + str(exception))
      pass

  def restart_and_reconnect(self):
    global mqtt_client, debug_mode
    try:
      if debug_mode: print('Failed to connect to MQTT broker. Reconnecting...')
      mqtt_client = connect_and_subscribe()
    except Exception as exception:
      if debug_mode: print('Restart and reconnect handler exception: ' + str(exception))
      pass

  def new_message_handler(self, topic, msg):
    global debug_mode
    try:
      if debug_mode: print(msg)
      msg_str = ujson.loads(msg.decode())
      msg_obj = ActionRequest(msg_str)
      if msg_obj.uid == Helper.get_uid():
        ActionHandler.select_action(msg_obj)
    except Exception as exception:
      if debug_mode: print('New message handler exception: %s' % str(exception))
      pass

  def publish_handler(self, payload_obj):
    global mqtt_client, mqtt_topic_pub, debug_mode
    try:
      if debug_mode: print(payload_obj.to_payload())
      mqtt_client.publish(mqtt_topic_pub, payload_obj.to_payload(), retain=False, qos=0)
      if debug_mode: print('MQTT is healthing!')
    except Exception as exception:
      if debug_mode: print('Publish message handler exception: %s' % str(exception))
      if debug_mode: print('MQTT disconnected!')
      connect_and_subscribe()

