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
driver = webdriver.Chrome(options=chrome_options)

run_id = "{:05d}".format(random.randint(1,10000))
if len(sys.argv)>=3:
    run_id = sys.argv[2]

driver.get("http://10.67.185.120:5001")
assert "NKT" in driver.title
elem = driver.find_element(By.NAME,"button")
elem.click()

assert "Apic Login" in driver.title
elem = driver.find_element(By.ID,"deploy_vm-checkbox")
elem.click()
elem = driver.find_element(By.NAME,"fabric")
elem.clear()
elem.send_keys("fab1-apic1.cam.ciscolabs.com")
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
elem.send_keys("calico_dev_v4")
elem = driver.find_element(By.NAME,"ipv4_cluster_subnet")
elem.clear()
elem.send_keys("192.168.39.0/24")
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
elem.send_keys("calico_dev_v4/vrf")
elem = driver.find_element(By.ID,'contract')
elem.send_keys("common/calico_dev")
elem = driver.find_element(By.ID,'physical_dom')
elem.send_keys("Fab1")

add_anchor_node("1","1","101","1.1.1.101","192.168.39.101")
add_anchor_node("1","1","102","1.1.1.102","192.168.39.102/24")

current_url = driver.current_url

elem = driver.find_element(By.ID,"submit")
elem.click()

#Wait for the page to be loaded
WebDriverWait(driver, 15).until(EC.url_changes(current_url))

assert "NKT - Cluster Network" in driver.title
elem = driver.find_element(By.ID,"vlan_id")
elem.send_keys("11")
elem = driver.find_element(By.ID,"submit")
current_url = driver.current_url
elem.click()
#driver.quit()
