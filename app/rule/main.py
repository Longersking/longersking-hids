from rule_manager import RuleManager
from string_matcher import StringMatcher
from packet_processor import PacketProcessor
from worker import Worker

def main():
    # 初始化规则管理器
    rule_manager = RuleManager('rule.json')
    rules = rule_manager.get_enabled_rules()
    string_matcher = StringMatcher(rules)
    packet_processor = PacketProcessor(string_matcher)
    worker = Worker(packet_processor)

    # 启动工作线程
    worker.start_workers()

    # 示例数据包
    packets = [
        {'src_ip': '192.168.1.1', 'dst_ip': '192.168.1.2', 'payload': ':${%23a%3dnew%20java.lang.ProcessBuilder(new%20java.lang.String[]{%22whoami%22}).start().getInputStream(),%23b%3dnew%http://20java.io.InputStreamReader(%23a),%23c%3dnew%http://20java.io.BufferedReader(%23b),%23d%3dnew%20char[51020],%23c.read(%23d),%23screen%3d%23context.get(%27com.opensymphony.xwork2.dispatcher.HttpServletResponse%27).getWriter(),%23screen.println(%23d),%23screen.close()}%22%3Etest.action?redirect:${%23a%3dnew%20java.lang.ProcessBuilder(new%20java.lang.String[]{%22test%22}).start().getInputStream(),%23b%3dnew%http://20java.io.InputStreamReader(%23a),%23c%3dnew%20java'},
        {'src_ip': '192.168.1.2', 'dst_ip': '192.168.1.3', 'payload': '-extractvalue(1,concat(0x5c,database()))-'},
        {'src_ip': '192.168.1.3', 'dst_ip': '192.168.1.4', 'payload': '/safety/ping.htm'},
        {'src_ip': '192.168.1.4', 'dst_ip': '192.168.1.5', 'payload': 'a'}
    ]

    # 将数据包放入队列
    for packet in packets:
        worker.add_packet(packet)

    # 等待所有数据包处理完毕
    worker.wait_for_completion()

    # 停止工作线程
    worker.stop_workers()

    # 处理结果
    while not packet_processor.result_queue.empty():
        result = packet_processor.result_queue.get()
        return result

if __name__ == "__main__":
    print(main())
