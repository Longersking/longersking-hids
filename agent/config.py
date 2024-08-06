import os

def get_config()->dict:
    """
    get config from os type
    params:
        none
    return:
        config dict
    """
    if os.name == 'nt':
        return {
            "paths_to_monitor": ["W:\Temp"],
            "process_to_monitor": ["tcp","udp","ssh","telnet"]
        }
    elif os.name == 'posix':
        return {
            "paths_to_monitor" : ["/etc/passwd", "/etc/shadow", "/root/.bash_history", "/etc/init.d"],
            "process_to_monitor": ["tcp","udp","ssh","telnet"]
        }

if __name__ == '__main__':
    print(get_config())