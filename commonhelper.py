class Helper:
  
  def format_date_time(epoch):
    year = utime.localtime(epoch)[0]
    month = '{:02}'.format(utime.localtime(epoch)[1])
    day = '{:02}'.format(utime.localtime(epoch)[2])
    hour = '{:02}'.format(utime.localtime(epoch)[3])
    minute = '{:02}'.format(utime.localtime(epoch)[4])
    second = '{:02}'.format(utime.localtime(epoch)[5])    
    return '%s-%s-%sT%s:%s:%s.0000000Z' % (year,month,day,hour,minute,second)

  def get_uid():
    uid = str(ubinascii.hexlify(machine.unique_id()))
    invalid = "\\'"
    for idx in range(0,len(invalid)):
      uid = uid.replace(invalid[idx],'')
    return uid + '-' + str(esp.flash_id())
  
  def get_sys_info():
    global debug_mode
    newline = '\\r\\n'
    uname = os.uname()
    lt = time.localtime()
    wl = network.WLAN(network.STA_IF)
    cg = wl.ifconfig()
    info = 'Plataform ' + str(uname[4]) + newline
    info += 'Clock ' + str(machine.freq() / 1000000) + ' MHz' + newline
    info += 'Total flash size ' + str(esp.flash_size() / 1000000) + 'Mb' + newline
    info += 'Free flash size ' + str(esp.freemem() / 1000) + 'Kb' + newline
    info += 'Free heap ' + str(gc.mem_free()) + ' bytes' + newline
    info += 'Allocated heap ' + str(gc.mem_alloc()) + ' bytes' + newline
    info += 'Stack in use ' + str(micropython.stack_use()) + newline
    info += 'Timestamp ' + str(lt[0]) + '-' + str(lt[1]) + '-' + str(lt[2]) + ' ' + str(lt[3]) + ':' + str(lt[4]) + ':' + str(lt[5]) + newline
    info += 'Directories ' + str(sys.path) + newline
    info += 'GPIO 0 set to read' + newline
    info += 'GPIO 2 set to write' + newline
    if debug_mode: print(info)
    return info

  def get_network_info():
    global debug_mode
    wl= network.WLAN(network.STA_IF)
    cg = wl.ifconfig()
    newline = '\\r\\n'
    info  = 'IPv4 ' + str(cg[0]) + newline
    info += 'DNS address: ' + str(cg[3]) + newline
    info += 'Gateway: ' + str(cg[2]) + newline
    info += 'Net mask: ' + str(cg[1]) + newline
    print(str(wl.config('mac')) + newline)
    if network.phy_mode() == 1: info += 'PHY mode MODE 11B IEEE 802.11b' + newline
    if network.phy_mode() == 2: info += 'PHY mode MODE 11G IEEE 802.11g' + newline
    if network.phy_mode() == 3: info += 'PHY mode MODE 11N IEEE 802.11n' + newline
    if debug_mode: print(info)
    return info
    
  def get_version_info():
    global debug_mode
    uname = os.uname()
    newline = '\\r\\n'
    info  = 'Vendor Microworking systems' + newline
    info += 'Model Microthing v1 build 2022-09-15' + newline
    info += 'Devide ID ' + str(esp.flash_id()) + newline
    info += 'Plataform ' + str(uname[4]) + newline
    info += 'Devkit ' + str(uname[2]) + newline
    info += 'Firmware ' + sys.version[6:] + newline
    info += 'Language version ' + sys.version[:5]  + newline
    info += 'Port modules ' + str(sys.modules) + newline
    info += 'User modules ' + str(os.listdir()) + newline
    info += 'GitHub https://github.com/microworking/telegram-iot-api'
    if debug_mode: print(info)
    return info


