#!/usr/bin/env python3
# -*- coding: utf8 -*-

import json
import re
import sys

if (len(sys.argv)) == 1:
    print("请输入 IP, 空白符分割, 按 <Ctrl-D> 结束输入.")

    ips = list()
    for line in sys.stdin:
        ips.extend([ip for ip in line.split() if len(ip) != 0])

    ips_set = set(ips)
    if len(ips) != len(ips_set):
        print(f"#### 有重复 ip, 已进行过滤操作.  ({len(ips_set)}/{len(ips)}) ####")
        ips = list(ips_set)

    illegal_ips = [
        ip
        for ip in ips
        if not re.match(
            r"^((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}$",
            ip,
        )
    ]

    ips = list(set(ips) - set(illegal_ips))

    print(json.dumps(ips))
    print(f"成功总数:{len(ips)}")
    if illegal_ips:
        print(f"非法ip: {illegal_ips}")

elif sys.argv[1] == "-r":

    ip_list_str = input("请输入 IP 列表, 按 <Ctrl-D> 结束输入.\n")
    ip_list_str = re.sub(r'"|\'|\s|\[|\]', "", ip_list_str)

    ip_list = ip_list_str.split(",")
    illegal_ips = [
        ip
        for ip in ip_list
        if not re.match(
            r"^((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}$",
            ip,
        )
    ]

    ip_list = list(set(ip_list) - set(illegal_ips))

    for ip in ip_list:
        print(ip)
    print(f"成功总数:{len(ip_list)}")

    if illegal_ips:
        print(f"非法ip: {illegal_ips}")
