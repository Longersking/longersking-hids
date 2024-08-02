import asyncio
import time

import psutil
from .utils import get_ip_address, SIMULATED_PACKET_LOSS_RATE, PACKET_LOSS_INTERVAL
from .websocket_client import send_data

async def calculate_packet_loss():
    print("Starting packet loss calculation...")  # Log for starting the function
    previous_stats = psutil.net_io_counters(pernic=True)
    await asyncio.sleep(PACKET_LOSS_INTERVAL)

    while True:
        try:
            current_stats = psutil.net_io_counters(pernic=True)
            packet_loss_rates = {}

            for nic in current_stats.keys():
                if nic in previous_stats:
                    sent_diff = current_stats[nic].packets_sent - previous_stats[nic].packets_sent
                    recv_diff = current_stats[nic].packets_recv - previous_stats[nic].packets_recv
                    drop_diff = current_stats[nic].dropin + current_stats[nic].dropout - \
                                (previous_stats[nic].dropin + previous_stats[nic].dropout)

                    if sent_diff + recv_diff > 0:
                        packet_loss_rate = drop_diff / (sent_diff + recv_diff)
                    else:
                        packet_loss_rate = SIMULATED_PACKET_LOSS_RATE  # 模拟丢包率

                    packet_loss_rates[nic] = packet_loss_rate

            # Calculate the average packet loss rate
            average_packet_loss_rate = sum(packet_loss_rates.values()) / len(packet_loss_rates) if packet_loss_rates else SIMULATED_PACKET_LOSS_RATE

            packet_loss_stats = {
                'ip': get_ip_address(),
                'packet_loss_rate': average_packet_loss_rate,
                'time': time.strftime("%H:%M:%S", time.localtime())
            }
            print(f"Sending packet loss data: {packet_loss_stats}")  # Log for sending data
            await send_data(packet_loss_stats, "packet_loss")

            previous_stats = current_stats
            await asyncio.sleep(PACKET_LOSS_INTERVAL)
        except Exception as e:
            print(f"Error calculating packet loss: {e}")
            await asyncio.sleep(PACKET_LOSS_INTERVAL)
