import psutil
import logging

# 获取网卡信息
def get_network_info():
    try:
        addr = psutil.net_if_addrs()
        addr_info = {
            k: [
                dict(
                    family=val.family.name,
                    address=val.address,
                    netmask=val.netmask,
                    broadcast=val.broadcast
                )
                for val in v if val.family.name == "AF_INET"
            ][0]
            for k, v in addr.items()
        }
        io = psutil.net_io_counters(pernic=True)
        data = [
            dict(
                name=k,
                bytes_sent=v.bytes_sent,
                bytes_recv=v.bytes_recv,
                packets_sent=v.packets_sent,
                packets_recv=v.packets_recv,
                **addr_info[k]
            )
            for k, v in io.items()
        ]
        return data
    except Exception as e:
        logging.error(f"Error in net method: {e}")
        return []
