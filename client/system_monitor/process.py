import psutil
import logging

# 获取系统活跃进程数和总进程数
def get_process_counts():
    try:
        total_processes = 0
        active_processes = 0
        for proc in psutil.process_iter(['status']):
            total_processes += 1
            if proc.info['status'] == psutil.STATUS_RUNNING:
                active_processes += 1
        return total_processes, active_processes
    except Exception as e:
        logging.error(f"Error in get_process_counts: {e}")
        return 0, 0

# 获取占用率前十的进程，并根据CPU和内存占用进行综合排序
def get_top_10_processes():
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        # 按CPU和内存占用综合排序并获取前十名
        top_10_processes = sorted(
            processes,
            key=lambda p: (p['cpu_percent'] + p['memory_percent']),
            reverse=True
        )[:10]
        return top_10_processes
    except Exception as e:
        logging.error(f"Error in get_top_10_processes: {e}")
        return []

# 组合功能，返回系统活跃进程数、总进程数和占用率前十的进程信息
def get_system_process_info():
    total_process_count, active_process_count = get_process_counts()
    top_10_processes = get_top_10_processes()

    data = {
        'total_process_count': total_process_count,
        'active_process_count': active_process_count,
        'top_10_processes': top_10_processes
    }
    return data

# 示例使用
if __name__ == "__main__":
    system_process_info = get_system_process_info()
    print(system_process_info)
