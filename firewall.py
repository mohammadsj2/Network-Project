import enum


class FirewallType(enum.Enum):
    BLACK_LIST = 0
    WHITE_LIST = 1


class Firewall:
    def __init__(self):
        self.port_list = []
        self.type = FirewallType.BLACK_LIST

    def is_valid(self, port: int) -> bool:
        if self.type == FirewallType.BLACK_LIST:
            return port not in self.port_list
        return port in self.port_list

    def set_firewall_type(self, firewall_type: FirewallType):
        self.type = firewall_type
        self.port_list = []

    def close_port(self, port: int):
        if self.type == FirewallType.BLACK_LIST:
            if port not in self.port_list:
                self.port_list.append(port)
        elif port in self.port_list:
            self.port_list.remove(port)

    def open_port(self, port: int):
        if self.type == FirewallType.WHITE_LIST:
            if port not in self.port_list:
                self.port_list.append(port)
        elif port in self.port_list:
            self.port_list.remove(port)