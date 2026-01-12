from dataclasses import dataclass

@dataclass(frozen=True)
class PortStatistics:
    port_no: int
    port_name: str
    bytes_recv: int
    bytes_send: int
    crc_packets: int
