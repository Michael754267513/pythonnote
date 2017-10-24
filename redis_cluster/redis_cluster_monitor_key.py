startup_nodes = [
    {"host": "192.168.12.171", "port": "6379"},
    {"host": "192.168.12.171", "port": "6380"},
    {"host": "192.168.12.171", "port": "6381"},
    {"host": "192.168.12.172", "port": "6379"},
    {"host": "192.168.12.172", "port": "6380"},
    {"host": "192.168.12.172", "port": "6381"}
]

monitor_cluster_key = [
    'cluster_state',
    'cluster_slots_assigned',
    'cluster_known_nodes',
    'cluster_slots_fail',
    'cluster_stats_messages_received',
    'cluster_size',
    'cluster_current_epoch',
    'cluster_stats_messages_sent',
    'cluster_slots_pfail',
    'cluster_my_epoch',
    'cluster_slots_ok'
]
