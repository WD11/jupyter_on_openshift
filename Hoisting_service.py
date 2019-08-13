import os
import configparser
import yaml
import time

config=configparser.ConfigParser()
config.read('./conf/properties.conf')
lists_header=config.sections()
for user_name in lists_header:
    with open('./conf/notebook-template-hoisting.yaml') as yaml_file:
        yaml_obj=yaml.load(yaml_file.read())
        yaml_file.close()
        #print(yaml_obj)
        #print(yaml_obj['metadata']['name'])

    with open('./conf/notebook-template-hoisting.yaml','w') as yaml_file:
        yaml_obj['metadata']['name']=config[user_name]['template_name']
        yaml_obj['metadata']['annotations']['openshift.io/display-name'] = config[user_name]['openshift_display_name']
        yaml_obj['parameters'][0]['value'] = config[user_name]['app_name']
        yaml_obj['parameters'][1]['value'] = config[user_name]['volume_size']
        yaml_obj['parameters'][2]['value'] = config[user_name]['persistent_volume_workspace']
        yaml_obj['parameters'][3]['value'] = config[user_name]['persistent_volume_rootdir']
        print(yaml_obj)
        yaml.dump(yaml_obj,yaml_file)
        yaml_file.close()

    os.system('oc create -f {0}'.format('./conf/notebook-template-hoisting.yaml'))
    os.system('oc new-app --template={0}'.format(config[user_name]['template_name']))



