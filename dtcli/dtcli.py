#!/usr/bin/python
# -*- coding: UTF-8 -*-
# auth: wolf-li
# version: 0.2
# date: 2022-11-10
# description: dependency track cli tool
# 

import requests
import json
import re
import os
import argparse

class DependencyTrackApi:

    def __init__(self, url, token):
        self.url = url
        self.token = token
        self.header = {"X-API-Key":token, "Content-Type": "application/json"}
        self.api = url + "/api"
        self.apikey_check = self.api + "/v1/permission"
        self.api_project = self.api + "/v1/project"
        self.api_metrics = self.api + "/v1/metrics"
        self.api_metrics_project = self.api_metrics + "/project/"

    def url_format(self):
        re_url = r'^(?:https?:\/\/)?[\w-]+(?:\.[\w-]+)+:\d{1,5}$'
        if re.match(re_url, self.url):
            return True
        else:
            raise Exception("Invalid url", self.url)

    def check_apikey(self):
        try:
            self.url_format()
            response = requests.get(self.url, headers = self.header, timeout=2.5).status_code
            if response >= 200 and response < 300:
                response = requests.get(self.apikey_check, headers = self.header).status_code
                if response == 200:
                    return True
                else:
                    raise Exception("Invalid token!", self.token)
            else:
                raise Exception("Connect url error",self.url)
        except requests.exceptions.ConnectTimeout:
            raise Exception("Connect url timeout",self.url)

    def get_project_uuid(self, project_name):
        if self.check_apikey():
            tmp_url = self.api_project + "?name=" + project_name
            response = requests.get(tmp_url, headers = self.header)
            if response.json():
                res = response.json()[0]
                return res["uuid"]
            else:
                return None
        else:
            raise Exception("Invalid token!", self.token)

    def get_project_metrics(self, project_name):
        if self.get_project_uuid(project_name):
            tmp_url = self.api_metrics_project + self.get_project_uuid(project_name) + "/current"
            response = requests.get( tmp_url, headers = self.header)
            res = response.json()
            res_dict = {"critical" : res["critical"], "high" : res["high"], "medium" : res["medium"], "vulnerableComponents" : res["vulnerableComponents"], "components":res["components"]}
            #return res["critical"], res["high"],  res["medium"], res["vulnerableComponents"], res["components"]
            return res_dict
        else:
            return False 

    def get_project_all(self):
        if self.check_apikey(): 
            response = requests.get( self.api_project + "?excludeInactive=false", headers = self.header)
            res = response.json()
            res_list = []
            for i in res:
                res_list.append(i["name"].encode('utf-8'))
            return res_list
        else:
            raise Exception("Invalid token!", self.token)

    def put_create_project(self, project_name, classifier):
        if self.get_project_uuid(project_name):
            raise Exception("The project already created!", project_name)
        else:
            enum_classifier = [ "APPLICATION", "FRAMEWORK", "LIBRARY", "CONTAINER", "OPERATING_SYSTEM", "DEVICE", "FIRMWARE", "FILE" ]
            if classifier not in enum_classifier:
                raise Exception("wrong classifier!", classifier)
            tmp_data = {
            "name": project_name,
                "classifier": classifier,
            "active": True
            }
            req = requests.request(method = 'PUT', url = self.api_project , headers = self.header, json = tmp_data)
            req.encoding = 'utf-8'
            res = json.loads(req.content)
            return res['uuid']

    def delete_project(self, project_name):
        if self.get_project_uuid(project_name):
            req = requests.request(method = 'DELETE', url = self.api_project + "/" + self.get_project_uuid(project_name), headers = self.header)
            if req.status_code == 204:
                return "delete " + project_name 
            else:
                return "delete fail"
        else:
            raise Exception("The project isn't exist!", project_name)


def main():
    parser = argparse.ArgumentParser(description='DependencyTrack cli tool.',prog='dtcli')
    parser.add_argument('-u', '--url',dest='input_url', metavar='http(s)://ip:port', type=str, help='Dependency Track backgroud api url.', required=True)
    parser.add_argument('-t', '--token', dest='input_token', metavar='xx-xxx-xx', type=str, help='Dependency Track backgroud api token.',required=True)    
    parser.add_argument('-c', dest='create_project', metavar='ProjectName ProjectType', type=str, help='Create project in the Dependency Track.', nargs=2)    
    parser.add_argument('-d', '--delete-project', dest='delete_project', metavar='ProjectName', type=str, help='Delete project in the Dependency Track.')    
    parser.add_argument('-l', '--list-all-project', dest='list_project',  help='List all projects in the Dependency Track.',action='store_true')    
    parser.add_argument('-sv', dest='summary_vuln_project', metavar='ProjectName', type=str, help='Summary of Vulnerability Number project in the Dependency Track.')    
    args = parser.parse_args()
    dpt = DependencyTrackApi(args.input_url, args.input_token)
    if args.create_project:
        print(dpt.put_create_project(args.create_project[0],args.create_project[1]))
    elif args.delete_project:
        print(dpt.delete_project(args.delete_project))
    elif args.summary_vuln_project:
        print(dpt.get_project_metrics(args.summary_vuln_project))
    elif args.list_project:
        print(dpt.get_project_all())
    else:
        print(dpt.check_apikey())
   

if __name__ == '__main__':
    main()
