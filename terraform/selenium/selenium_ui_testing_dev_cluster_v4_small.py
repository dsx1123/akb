from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import sys
import random
from time import sleep
def add_anchor_node(pod_id,rack_id,node_id,rtr_id,node_ipv4):
    elem = driver.find_element(By.NAME,"pod_id")
    elem.send_keys(pod_id)
    elem = driver.find_element(By.NAME,"rack_id")
    elem.clear()
    elem.send_keys(rack_id)
    select = Select(driver.find_element(By.ID,'node_id'))
    select.select_by_visible_text(node_id)
    elem = driver.find_element(By.NAME,"rtr_id")
    elem.clear()
    elem.send_keys(rtr_id)
    elem = driver.find_element(By.NAME,"node_ipv4")
    elem.clear()
    elem.send_keys(node_ipv4)
    elem = driver.find_element(By.ID,"add_node")
    elem.click()
    sleep(1)

def add_calico_ndoe(hostname, ip, rack_id):
    elem = driver.find_element(By.NAME,"hostname")
    elem.clear()
    elem.send_keys(hostname)
    elem = driver.find_element(By.NAME,"ip")
    elem.clear()
    elem.send_keys(ip)
    elem = driver.find_element(By.NAME,"rack_id")
    elem.clear()
    elem.send_keys(rack_id)
    elem = driver.find_element(By.ID,"add_node")
    elem.click()
    sleep(1)

chrome_options = Options()
if len(sys.argv)>=2:
    port= sys.argv[1]
    chrome_options.add_argument(sys.argv[1])
driver = webdriver.Chrome()

run_id = "{:05d}".format(random.randint(1,10000))
if len(sys.argv)>=3:
    run_id = sys.argv[2]

driver.get("http://10.67.185.120:5001")
assert "NKT" in driver.title
elem = driver.find_element(By.NAME,"button")
elem.click()

assert "Apic Login" in driver.title
elem = driver.find_element(By.NAME,"fabric")
elem.clear()
elem.send_keys("fab2-apic1.cam.ciscolabs.com")
elem = driver.find_element(By.NAME,"username")
elem.clear()
elem.send_keys("admin")
elem = driver.find_element(By.NAME,"password")
elem.clear()
elem.send_keys("123Cisco123")
elem = driver.find_element(By.ID,"submit")
current_url = driver.current_url
elem.click()
#Wait for the page to be loaded
WebDriverWait(driver, 15).until(EC.url_changes(current_url))

assert "L3OUT" in driver.title
elem = driver.find_element(By.ID,'l3out_tenant')
elem.send_keys("calico1")
elem = driver.find_element(By.NAME,"ipv4_cluster_subnet")
elem.clear()
elem.send_keys("192.168.2.0/24")
elem = driver.find_element(By.NAME,"dns_servers")
elem.send_keys("10.67.185.100")
elem = driver.find_element(By.NAME,"dns_domain")
elem.send_keys("cam.ciscolabs.com")
# WAIT FOR THE vrf_name_list TO BE POPULATED WITH AT LEAST 2 ELEMENTs (The first one is just the palce holder)
# THAT SHOULD BE ALL IT TAKES TO HAVE THE REST OF THE PAGE READY...
try:
    elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="vrf_name_list"]/option[2]')))
except ValueError as e:
    print("Loading took too much time!")

elem = driver.find_element(By.ID,'vrf_name')
elem.send_keys("calico1/vrf")
elem = driver.find_element(By.ID,'contract')
elem.send_keys("common/calico_dev")
elem = driver.find_element(By.ID,'physical_dom')
elem.send_keys("Fab1")

add_anchor_node("1","1","201","1.1.1.201","192.168.2.201")
add_anchor_node("1","1","202","1.1.1.202","192.168.2.202/24")
add_anchor_node("1","2","203","1.1.1.204","192.168.2.203")
add_anchor_node("1","2","204","1.1.1.205","192.168.2.204/24")

current_url = driver.current_url

elem = driver.find_element(By.ID,"submit")
elem.click()

#Wait for the page to be loaded
WebDriverWait(driver, 15).until(EC.url_changes(current_url))

assert "vCenter Login" in driver.title
elem = driver.find_element(By.NAME,"url")
elem.send_keys("vc2.cam.ciscolabs.com")
elem = driver.find_element(By.NAME,"username")
elem.send_keys("administrator@vsphere.local")
elem = driver.find_element(By.NAME,"pass")
elem.send_keys("123Cisco123!")
elem = driver.find_element(By.ID,"template_checkbox")
elem.click()
elem = driver.find_element(By.ID,"submit")
current_url = driver.current_url
elem.click()

#Wait for the page to be loaded
WebDriverWait(driver, 15).until(EC.url_changes(current_url))
assert "vCenter Details" in driver.title
select = Select(driver.find_element(By.ID,'dc'))
select.select_by_visible_text("STLD")

#Wait for vCenter API to populate the page
try:
    elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="datastore_list"]/option[1]')))
except ValueError as e:
    print("Loading took too much time!")

elem = driver.find_element(By.ID,'datastore')
elem.send_keys("esxi5-RAID5")
select = Select(driver.find_element(By.ID,'cluster'))
select.select_by_visible_text("Cluster")
elem = driver.find_element(By.ID,'port_group')
elem.send_keys("ACI/CalicoL3OUT_300/vlan-300")
elem = driver.find_element(By.ID,'vm_templates')
elem.send_keys("Ubuntu21SandBox")
elem = driver.find_element(By.ID,'vm_folder')
elem.send_keys("Calico-Cluster1")
elem = driver.find_element(By.ID,"submit")
current_url = driver.current_url
elem.click()

#Wait for the page to be loaded
WebDriverWait(driver, 15).until(EC.url_changes(current_url))
assert "Calico Nodes" in driver.title
elem = driver.find_element(By.ID,'calico_nodes')
elem.clear()
add_calico_ndoe('nkt-master-{}-1'.format(run_id),'192.168.2.1/24', '1')
add_calico_ndoe('nkt-master-{}-2'.format(run_id),'192.168.2.2/24', '1')
add_calico_ndoe('nkt-master-{}-3'.format(run_id),'192.168.2.3/24', '1')
add_calico_ndoe('nkt-worker-{}-1'.format(run_id),'192.168.2.4/24', '1')
add_calico_ndoe('nkt-worker-{}-2'.format(run_id),'192.168.2.5/24', '1')
add_calico_ndoe('nkt-worker-{}-3'.format(run_id),'192.168.2.6/24', '1')


elem = driver.find_element(By.ID,"submit")
current_url = driver.current_url
elem.click()

#Wait for the page to be loaded
WebDriverWait(driver, 15).until(EC.url_changes(current_url))
assert "Cluster" in driver.title
elem = driver.find_element(By.ID,'advanced')
elem.click()
elem = driver.find_element(By.ID,'timezone')
elem.send_keys("Australia/Sydney")
elem = driver.find_element(By.ID,'docker_mirror')
elem.send_keys("10.67.185.120:5000")
elem = driver.find_element(By.ID,'ntp_server')
elem.send_keys("72.163.32.44")
elem = driver.find_element(By.ID,'ubuntu_apt_mirror')
elem.send_keys("ubuntu.mirror.digitalpacific.com.au/archive/")
elem = driver.find_element(By.ID,"submit")
current_url = driver.current_url
elem.click()
WebDriverWait(driver, 15).until(EC.url_changes(current_url))
#Wait for the page to be loaded
WebDriverWait(driver, 15).until(EC.url_changes(current_url))
assert "Cluster Network" in driver.title
elem = driver.find_element(By.ID,"submit")
current_url = driver.current_url
elem.click()