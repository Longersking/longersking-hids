import asyncio
from network_monitor.packet_sniffer import start_sniffing
from network_monitor.packet_loss_calculator import calculate_packet_loss

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(calculate_packet_loss())
    loop.run_until_complete(start_sniffing())
