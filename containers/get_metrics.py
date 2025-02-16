from __future__ import print_function
from kubernetes import client
from kubernetes.client.rest import ApiException
from pprint import pprint
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError
from datetime import datetime
from time import sleep
import time
import sys
import ast
import os

with open("/run/secrets/kubernetes.io/serviceaccount/token", "r") as file:
    api_token = file.read().strip('\n')

cluster_name = os.environ.get('CLUSTER_NAME', 'demo_cluster')
api_endpoint = os.environ.get('API_ENDPOINT', 'api.sno.openshift.training')
influxdb_endpoint = os.environ.get('INFLUXDB_ENDPOINT', 'influxdb.apps.sno.openshift.training')
 
configuration = client.Configuration()
configuration.api_key['authorization'] = api_token
configuration.verify_ssl = True
configuration.api_key_prefix['authorization'] = 'Bearer'
configuration.host = "https://" + api_endpoint + ":6443"

def get_resourcequota():
    with client.ApiClient(configuration) as api_client:
        api_instance = client.CoreV1Api(api_client)
        # _continue = '_continue_example'
        pretty = 'true'
        
        try:
            api_response = api_instance.list_resource_quota_for_all_namespaces(pretty=pretty)
            # pprint(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_resource_quota_for_all_namespaces: %s\n" % e)

    # for v in api_response.items:
    #     print(v.metadata.namespace,
    #         v.status.hard['limits.cpu'], 
    #         v.status.hard['limits.memory'], 
    #         v.status.used['limits.cpu'], 
    #         v.status.used['limits.memory'])
    return api_response

    
def get_namespace(label):
    with client.ApiClient(configuration) as api_client:
        api_instance = client.CoreV1Api(api_client)
        # _continue = '_continue_example'
        pretty = 'true'
        label_selector = 'label'
        
        try:
            api_response = api_instance.list_namespace(pretty=pretty, label_selector=label_selector)
            # pprint(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespace: %s\n" % e)

    for ns in api_response.items:
        print(ns.metadata.labels['uaid'], ns.metadata.name)

def get_nodestats(node):
    with client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = client.CoreV1Api(api_client)
        name = node # str | name of the NodeProxyOptions
        path = '/stats/summary' # str | path to the resource

        try:
            api_response = api_instance.connect_get_node_proxy_with_path(name, path)
            # pprint(api_response)
            return api_response
        except ApiException as e:
            print("Exception when calling CoreV1Api->connect_get_node_proxy_with_path: %s\n" % e)


def get_node_list():
    with client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = client.CoreV1Api(api_client)
        pretty = 'true' # str | If 'true', then the output is pretty printed. Defaults to 'false' unless the user-agent indicates a browser or command-line HTTP tool (curl and wget). (optional)
        # allow_watch_bookmarks = True # bool | allowWatchBookmarks requests watch events with type \"BOOKMARK\". Servers that do not implement bookmarks may ignore this flag and bookmarks are sent at the server's discretion. Clients should not assume bookmarks are returned at any specific interval, nor may they assume the server will send any BOOKMARK event during a session. If this is not a watch, this field is ignored. (optional)
        # _continue = '_continue_example' # str | The continue option should be set when retrieving more results from the server. Since this value is server defined, kubernetes.clients may only use the continue value from a previous query result with identical query parameters (except for the value of continue) and the server may reject a continue value it does not recognize. If the specified continue value is no longer valid whether due to expiration (generally five to fifteen minutes) or a configuration change on the server, the server will respond with a 410 ResourceExpired error together with a continue token. If the kubernetes.client needs a consistent list, it must restart their list without the continue field. Otherwise, the kubernetes.client may send another list request with the token received with the 410 error, the server will respond with a list starting from the next key, but from the latest snapshot, which is inconsistent from the previous list results - objects that are created, modified, or deleted after the first list request will be included in the response, as long as their keys are after the \"next key\".  This field is not supported when watch is true. Clients may start a watch from the last resourceVersion value returned by the server and not miss any modifications. (optional)
        # field_selector = 'field_selector_example' # str | A selector to restrict the list of returned objects by their fields. Defaults to everything. (optional)
        # label_selector = 'label_selector_example' # str | A selector to restrict the list of returned objects by their labels. Defaults to everything. (optional)
        # limit = 56 # int | limit is a maximum number of responses to return for a list call. If more items exist, the server will set the `continue` field on the list metadata to a value that can be used with the same initial query to retrieve the next set of results. Setting a limit may return fewer than the requested amount of items (up to zero items) in the event all requested objects are filtered out and kubernetes.clients should only use the presence of the continue field to determine whether more results are available. Servers may choose not to support the limit argument and will return all of the available results. If limit is specified and the continue field is empty, kubernetes.clients may assume that no more results are available. This field is not supported if watch is true.  The server guarantees that the objects returned when using continue will be identical to issuing a single list call without a limit - that is, no objects created, modified, or deleted after the first request is issued will be included in any subsequent continued requests. This is sometimes referred to as a consistent snapshot, and ensures that a kubernetes.client that is using limit to receive smaller chunks of a very large result can ensure they see all possible objects. If objects are updated during a chunked list the version of the object that was present at the time the first list result was calculated is returned. (optional)
        # resource_version = 'resource_version_example' # str | resourceVersion sets a constraint on what resource versions a request may be served from. See https://kubernetes.io/docs/reference/using-api/api-concepts/#resource-versions for details.  Defaults to unset (optional)
        # resource_version_match = 'resource_version_match_example' # str | resourceVersionMatch determines how resourceVersion is applied to list calls. It is highly recommended that resourceVersionMatch be set for list calls where resourceVersion is set See https://kubernetes.io/docs/reference/using-api/api-concepts/#resource-versions for details.  Defaults to unset (optional)
        # send_initial_events = True # bool | `sendInitialEvents=true` may be set together with `watch=true`. In that case, the watch stream will begin with synthetic events to produce the current state of objects in the collection. Once all such events have been sent, a synthetic \"Bookmark\" event  will be sent. The bookmark will report the ResourceVersion (RV) corresponding to the set of objects, and be marked with `\"k8s.io/initial-events-end\": \"true\"` annotation. Afterwards, the watch stream will proceed as usual, sending watch events corresponding to changes (subsequent to the RV) to objects watched.  When `sendInitialEvents` option is set, we require `resourceVersionMatch` option to also be set. The semantic of the watch request is as following: - `resourceVersionMatch` = NotOlderThan   is interpreted as \"data at least as new as the provided `resourceVersion`\"   and the bookmark event is send when the state is synced   to a `resourceVersion` at least as fresh as the one provided by the ListOptions.   If `resourceVersion` is unset, this is interpreted as \"consistent read\" and the   bookmark event is send when the state is synced at least to the moment   when request started being processed. - `resourceVersionMatch` set to any other value or unset   Invalid error is returned.  Defaults to true if `resourceVersion=\"\"` or `resourceVersion=\"0\"` (for backward compatibility reasons) and to false otherwise. (optional)
        # timeout_seconds = 56 # int | Timeout for the list/watch call. This limits the duration of the call, regardless of any activity or inactivity. (optional)
        # watch = True # bool | Watch for changes to the described resources and return them as a stream of add, update, and remove notifications. Specify resourceVersion. (optional)

        try:
            api_response = api_instance.list_node(pretty=pretty)
            # pprint(api_response)
            return api_response
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_node: %s\n" % e)

def send_data_influx(data):
    # Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImluZmx1eGRiIiwiZXhwIjoxNzY5NDcwNzYzLjU1NzI4Mn0.qU9vt_gQB4SMn1ywDYv-fPR58I53afq3kZwi27aA9hI
    series = []
    now = datetime.today()
    influxdb_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImluZmx1eGRiIiwiZXhwIjoxNzY5NDcwNzYzLjU1NzI4Mn0.qU9vt_gQB4SMn1ywDYv-fPR58I53afq3kZwi27aA9hI'
    client = InfluxDBClient(host=influxdb_endpoint, 
                            port=443, ssl=True, verify_ssl=True, 
                            username=None, password=None, 
                            headers={"Authorization": "Bearer " + influxdb_token},
                            database='openshift'
                            )
    version = client.ping()
    print("Successfully connected to InfluxDB: " + version)

    # node_start_time = int(datetime.strptime(data['node']['startTime'], "%Y-%m-%dT%H:%M:%SZ").strftime('%s'))
    node_start_time = data['node']['startTime']
    node_name = data['node']['nodeName']

    for nk, nv in data['node'].items():
        if isinstance(nv, dict) and nk not in ['systemContainers', 'network']:
            if nk == 'runtime':
                for rtk, rtv in nv.items():
                    if isinstance(rtv, dict):
                        field_time = rtv['time']
                        pointValues = {
                                "time": field_time,
                                "measurement": 'node_' + nk + '_' + rtk,
                                "fields": rtv,
                                "tags": {
                                    "node_name": node_name,
                                    "cluster_name": cluster_name,
                                    "runtime": 1,
                                },
                            }

                        pointValues['fields'].pop('time')
                        pointValues['fields'].update({'node_start_time': node_start_time})
                        series.append(pointValues)
            else:
                pointValues = {
                        "time": nv['time'],
                        "measurement": 'node_' + nk,
                        "fields": nv,
                        "tags": {
                            "node_name": node_name,
                            "cluster_name": cluster_name, 
                        },
                    }

                pointValues['fields'].pop('time')
                pointValues['fields'].update({'node_start_time': node_start_time})
                series.append(pointValues)
        
        # pprint(series)

    for sc in data['node']['systemContainers']:
        for k,v in sc.items():
            if isinstance(v, dict):
                field_time = v['time']
                pointValues = {
                        "time": field_time,
                        "measurement": 'container_' + k,
                        "fields": v,
                        "tags": {
                            "node_name": node_name,
                            "cluster_name": cluster_name, 
                            "container_name": sc['name'], 
                            "container_type": 'systemContainers', 
                        },
                    }
        
                pointValues['fields'].pop('time')
                pointValues['fields'].update({'node_start_time': node_start_time})
                pointValues['fields'].update({'container_start_time': sc['startTime']})
                series.append(pointValues)
                # pprint(series)

    for pod in data['pods']:
        for k,v in pod.items():
            if isinstance(v, dict) and k not in ['podRef', 'containers', 'volume', 'process_stats']:
                field_time = v['time']
                pointValues = {
                        "time": field_time,
                        "measurement": 'pod_' + k,
                        "fields": v,
                        "tags": {
                            "node_name": node_name,
                            "cluster_name": cluster_name, 
                            "container_type": 'namespace', 
                        },
                    }
        
                t = pointValues['fields'].pop('time')
                pointValues['fields'].update({'node_start_time': node_start_time})
                pointValues['fields'].update({'pod_start_time': pod['startTime']})
                pointValues['tags'].update(pod['podRef'])
                # pprint(series)

                if k == 'cpu':
                    pointValues['fields'].update({'process_count': pod['process_stats']['process_count']})

                if k == 'network':
                    pointValues['tags'].update({"network_name": v['name']})
                    ii = pointValues['fields'].pop('interfaces')
                    series.append(pointValues)
                    for i in ii:
                        pointValues = {
                                "time": t,
                                "measurement": 'pod_' + k + '_interface',
                                "fields": i,
                                "tags": {
                                    "node_name": node_name,
                                    "cluster_name": cluster_name, 
                                    "network_name": v['name'], 
                                    "interface_name": i['name'], 
                                    "container_type": 'namespace', 
                                },
                            }
                
                        pointValues['fields'].pop('name')
                        pointValues['tags'].update(pod['podRef'])
                        series.append(pointValues)
                        # pprint(pointValues)

                else: 
                    series.append(pointValues)


            if k == 'volume' and isinstance(v, list):
                for vv in v:
                    field_time = vv['time']
                    pointValues = {
                            "time": field_time,
                            "measurement": 'pod_' + k,
                            "fields": vv,
                            "tags": {
                                "node_name": node_name,
                                "cluster_name": cluster_name, 
                                "volume_name": vv['name'], 
                                "container_type": 'namespace', 
                            },
                        }
            
                    pointValues['fields'].pop('name')
                    pointValues['fields'].pop('time')
                    if 'pvcRef' in pointValues['fields']:
                        pvc = pointValues['fields'].pop('pvcRef')
                        pointValues['tags'].update({'pvc_ref_name': pvc['name']})
                        pointValues['tags'].update({'pvc_ref_namespace': pvc['namespace']})
                    pointValues['fields'].update({'node_start_time': node_start_time})
                    pointValues['fields'].update({'pod_start_time': pod['startTime']})
                    pointValues['tags'].update(pod['podRef'])
                    series.append(pointValues)
                    # pprint(pointValues)


            if isinstance(v, list) and k =='containers':
                for c in v:
                    for k,m in c.items():
                        if isinstance(m, dict):
                            field_time = c['startTime']
                            pointValues = {
                                    "time": field_time,
                                    "measurement": 'contanier_' + k ,
                                    "fields": m,
                                    "tags": {
                                        "node_name": node_name,
                                        "cluster_name": cluster_name, 
                                        "container_type": 'namespace', 
                                        "container_name": c['name'], 
                                    },
                                }
                    
                            pointValues['fields'].pop('time')
                            pointValues['fields'].update({'node_start_time': node_start_time})
                            pointValues['fields'].update({'pod_start_time': pod['startTime']})
                            pointValues['fields'].update({'container_start_time': field_time})
                            pointValues['tags'].update({'pod_name': pod['podRef']['name']})
                            pointValues['tags'].update({'pod_namespace': pod['podRef']['namespace']})
                            pointValues['tags'].update({'pod_uid': pod['podRef']['uid']})
                            series.append(pointValues)
                            # pprint(pointValues)


    # pprint(series)
    # retention_policy = 'server_data'
    # client.create_retention_policy(retention_policy, '30d', 3, default=True)
    client.write_points(series)

if __name__ == '__main__':
    for node in get_node_list().items:
        send_data_influx(ast.literal_eval(get_nodestats(node.metadata.name)))
    
    # send_data_influx()
    sys.stdout.flush()
    time.sleep(1)
