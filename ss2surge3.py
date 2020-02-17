# ss config to surge config proxy
import json

ss_content, surge_content = {}, {}


def read_ss_config():
    global ss
    global ss_content
    try:
        ss = open('export.json', 'r+').read()
        ss_content = json.loads(ss)
        return True
    except FileNotFoundError as err:
        print('<<<< File Not Found!')
        return False


def write_surge_config():
    surge_content = open('surge.surgeconfig.template', 'r+').read()
    surge_write = open('surge.surgeconfig', 'w+')
    # transfer
    append_ss = transfer(ss_content)
    # find position
    proxy_start = surge_content.find('[Proxy]\n')
    proxy_end = surge_content.find('\n[Rule]')
    surge_content = surge_content[:proxy_start + 8] + "\n".join(append_ss) + "\n" + surge_content[proxy_end:]
    surge_write.write(surge_content)
    print(surge_content)


def transfer(ss):
    servers = []
    if ss:
        for serve in ss["configs"]:
            template = "{} = {}, {} ,{} ,encrypt-method = {}, password= {}"
            servers.append(template.format(serve["remarks"] if serve["remarks"] else serve["server"], "ss",
                                           serve["server"],
                                           serve["server_port"],
                                           serve["method"],
                                           serve["password"]))
        return servers

    else:
        print('parse error!')


def main():
    if read_ss_config():
        write_surge_config()


if __name__ == '__main__':
    main()
