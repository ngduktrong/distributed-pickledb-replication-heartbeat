#
import asyncio

from heartbeat_manager import HeartbeatManager # Gửi yêu cầu heartbeat đến các node sao chép để kiểm tra tình trạng hoạt động của chúng

manager = HeartbeatManager(
    [
        "http://127.0.0.1:8001",
        "http://127.0.0.1:8002"
    ]
)

asyncio.run( # Chạy vòng lặp sự kiện để liên tục gửi yêu cầu heartbeat đến các node sao chép và xử lý phản hồi từ chúng
    manager.monitor()
)