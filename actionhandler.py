
class ActionHandler:
  
    def select_action(msg_obj):
      try:
        action = ActionResponse()
        action.identity_token = msg_obj.identity_token
        action.update_id = msg_obj.update_id
        action.chat_id = msg_obj.chat_id
        action.message_id = msg_obj.message_id
        action.uid = Helper.get_uid()
        action.gpio = msg_obj.gpio
        action.action = msg_obj.action
        action.owner = msg_obj.owner
        action.peripheral = msg_obj.peripheral
        action.message = msg_obj.message
        action.date = msg_obj.date
        if msg_obj.action == 'start': ActionHandler.start_action(action)
        if msg_obj.action == 'stop': ActionHandler.stop_action(action)
        if msg_obj.action == 'read': ActionHandler.read_action(action)
        if msg_obj.action == 'restart': ActionHandler.restart_action(action)
        if msg_obj.action == 'debug': ActionHandler.debug_action(action)
        if msg_obj.action == 'broadcast': ActionHandler.broadcast_action(action)
        if msg_obj.action == 'sys': ActionHandler.get_sys_info_action(action)
        if msg_obj.action == 'network': ActionHandler.get_network_info_action(action)
        if msg_obj.action == 'version': ActionHandler.get_version_info_action(action)
        if msg_obj.action == 'echo': ActionHandler.echo_action(action)
      except Exception as exception:
        if debug_mode: print('ActionHandler.select_action exception: %s' % str(exception))
        pass
    
    def start_action(action):
      global sensor, mqtt, gpio0_state_1_action_message, broadcast_enable
      action.message = gpio0_state_0_action_message % (action.peripheral, action.owner)
      sensor.value(0)
      if broadcast_enable:
        action.identity_token = '8o1nx9zfTFUiAkYdgWR3GUlX9fxpREFOQw1dtoidR0jfa5ihR0alIj9GmuV4YrIE'
        action.action = 'broadcast'
      mqtt.publish_handler(action)

    def stop_action(action):
      global sensor, mqtt, gpio0_state_0_action_message, broadcast_enable
      action.message = gpio0_state_1_action_message % (action.peripheral, action.owner)
      sensor.value(1)
      if broadcast_enable: 
        action.identity_token = '8o1nx9zfTFUiAkYdgWR3GUlX9fxpREFOQw1dtoidR0jfa5ihR0alIj9GmuV4YrIE'
        action.action = 'broadcast'
      mqtt.publish_handler(action)
 
    def read_action(action):
      global mqtt, sensor, gpio0_state_0_read_message, gpio0_state_1_read_message
      if(sensor.value() == 0):
        action.message = gpio0_state_0_read_message % (action.peripheral)
      else:
        action.message = gpio0_state_1_read_message % (action.peripheral)
      mqtt.publish_handler(action)

    def restart_action(action):
      global mqtt, restart_message, broadcast_enable
      action.message = restart_message % (action.peripheral, action.owner)
      if broadcast_enable: 
        action.identity_token = '8o1nx9zfTFUiAkYdgWR3GUlX9fxpREFOQw1dtoidR0jfa5ihR0alIj9GmuV4YrIE'
        action.action = 'broadcast'
      mqtt.publish_handler(action)
      machine.reset()
      
    def debug_action(action):
      global mqtt, debug_mode, debug_mode_message, broadcast_enable
      msg = None
      if debug_mode == True:
        debug_mode = False
        msg = 'desabilitado'
      else:
        debug_mode = True
        msg = 'habilitado'
      action.message = debug_mode_message % (msg, action.peripheral, action.owner)
      if broadcast_enable:
        action.identity_token = '8o1nx9zfTFUiAkYdgWR3GUlX9fxpREFOQw1dtoidR0jfa5ihR0alIj9GmuV4YrIE'
        action.action = 'broadcast'
      mqtt.publish_handler(action)
          
    def broadcast_action(action):
      global mqtt, broadcast_enable, broadcast_enable_message
      msg = None
      if broadcast_enable == True:
        broadcast_enable = False
        msg = 'desabilitado'
      else:
        broadcast_enable = True
        msg = 'habilitado'
      action.message = broadcast_enable_message % (msg, action.peripheral, action.owner)
      if broadcast_enable:
        action.identity_token = '8o1nx9zfTFUiAkYdgWR3GUlX9fxpREFOQw1dtoidR0jfa5ihR0alIj9GmuV4YrIE'
        action.action = 'broadcast'
      mqtt.publish_handler(action)

    def get_sys_info_action(action):
      global mqtt
      action.message = Helper.get_sys_info()
      mqtt.publish_handler(action)
          
    def get_network_info_action(action):
      global mqtt
      action.message = Helper.get_network_info()
      mqtt.publish_handler(action)
      
    def get_version_info_action(action):
      global mqtt
      action.message = Helper.get_version_info()
      mqtt.publish_handler(action)
        
    def echo_action(action):
      global mqtt, debug_mode, last_date_time
      last_date_time = action.date
      if debug_mode: print('MQTT health checked, date time is refresh for %s in device %s' % (last_date_time, action.uid))
      
