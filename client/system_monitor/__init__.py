from .cpu import get_cpu_info
from .memory import get_memory_info
from .swap import get_swap_info
from .disk import get_disk_info
from .network import get_network_info
from .system import get_system_info, get_logined_users
from .process import get_system_process_info
class Monitor:
    def cpu(self):
        return get_cpu_info()

    def mem(self):
        return get_memory_info()

    def swap_memory(self):
        return get_swap_info()

    def disk(self):
        return get_disk_info()

    def net(self):
        return get_network_info()

    def lastest_start_time(self):
        return get_system_info()

    def logined_users(self):
        return get_logined_users()
    def processes_info(self):
        return get_system_process_info()
