import subprocess
import optparse
import re

def parse_options():
  parser = optparse.OptionParser()
  parser.add_option('-m', '--mac-address', dest="mac", help="New MAC address to set")
  parser.add_option('-i', '--interface', dest="interface", help="Network interface to change MAC address of")

  (options, args) = parser.parse_args()

  if not options.mac or not options.interface:
    parser.error("--mac-address and --interface are mandatory options")

  return options


def get_current_mac(interface):
  output = subprocess.getoutput("ifconfig " + interface)
  rs = re.search('ether (\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)', output)
  mac = rs.group(1)
  print("The current mac is: " + mac)
  return mac

def change_mac(interface, new_mac):
  subprocess.run(['ifconfig', interface, 'down'], check=True)
  subprocess.run(['ifconfig', interface, 'hw', 'ether', new_mac], check=True)
  subprocess.run(['ifconfig', interface, 'up'], check=True)


if __name__ == "__main__":
  options = parse_options()
  get_current_mac(options.interface)
  change_mac(options.interface, options.mac)
  new_mac = get_current_mac(options.interface)
  if new_mac != options.mac:
    raise RuntimeError("Mac hasn't been changed")
