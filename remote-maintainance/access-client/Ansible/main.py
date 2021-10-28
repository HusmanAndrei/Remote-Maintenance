import requests
import subprocess

HOSTS_FILE = '/etc/ansible/hosts'
API_URL = "http://192.168.0.103:3003"

def get_hosts():
	devices = requests.request("GET", API_URL + "/devices").json()['devices']
	print(devices)
	dev_dict = {}
	for dev in devices:
		url_list = dev['ssh_url'].replace("tcp://", '').split(':')
		hostname = url_list[0]
		port = url_list[1]
		dev_dict[dev['uuid']] = (hostname, port, dev['customer_id'])
	return dev_dict

def update_inventory(hosts):
	index = 0
	with open(HOSTS_FILE, 'w') as f:
		for host_id in hosts:
			host_info = hosts[host_id]
			hostname = host_info[0]
			port = host_info[1]
			user = host_info[2]
			f.write('[' + host_id + ']\n')
			f.write(hostname + ' ansible_user=' + user + ' ansible_port=' + port + '\n')
			index += 1

def run_ansible():
	exec_cmd = ['ansible-playbook', 'mytask.yml']
	proc = subprocess.Popen(exec_cmd)
	proc.wait()

if __name__ == "__main__":
	hosts_dict = get_hosts()
	print(hosts_dict)
	update_inventory(hosts_dict)
# 	run_ansible()