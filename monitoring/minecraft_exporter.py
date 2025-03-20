# #!/usr/bin/env python3
# import time
# import argparse
# from mcstatus import JavaServer
# from prometheus_client import start_http_server, Gauge, Counter
#
# # Parse command-line arguments
# parser = argparse.ArgumentParser(description='Minecraft Prometheus Exporter')
# parser.add_argument('--host', default='localhost', help='Minecraft server host')
# parser.add_argument('--port', type=int, default=25565, help='Minecraft server port')
# parser.add_argument('--listen-port', type=int, default=9150, help='Exporter listen port')
# args = parser.parse_args()
#
# # Create metrics
# PLAYERS_ONLINE = Gauge('minecraft_players_online', 'Number of players currently online')
# MAX_PLAYERS = Gauge('minecraft_players_max', 'Maximum player capacity')
# LATENCY = Gauge('minecraft_latency_ms', 'Server latency in milliseconds')
# VERSION = Gauge('minecraft_version_info', 'Server version information', ['version'])
# QUERY_SUCCESS = Counter('minecraft_query_success_total', 'Number of successful server queries')
# QUERY_FAILURES = Counter('minecraft_query_failures_total', 'Number of failed server queries')
#
# # Set up server
# minecraft_server = JavaServer(args.host, args.port)
#
# # Report metrics
# def get_server_stats():
#     try:
#         # Get server status
#         status = minecraft_server.status()
#
#         # Update metrics
#         PLAYERS_ONLINE.set(status.players.online)
#         MAX_PLAYERS.set(status.players.max)
#         LATENCY.set(status.latency)
#         VERSION.labels(version=status.version.name).set(1)
#
#         # Try to get player names if query is enabled
#         try:
#             query = minecraft_server.query()
#             # Additional metrics could be added here
#             QUERY_SUCCESS.inc()
#         except:
#             # Query protocol might not be enabled
#             pass
#
#     except Exception as e:
#         print(f"Error querying Minecraft server: {e}")
#         QUERY_FAILURES.inc()
#
# if __name__ == '__main__':
#     # Start up the server to expose metrics
#     start_http_server(args.listen_port)
#     print(f"Minecraft exporter started, listening on port {args.listen_port}")
#
#     # Loop forever collecting metrics
#     while True:
#         get_server_stats()
#         time.sleep(15)  # Update every 15 seconds
# !/usr/bin/env python3
"""
Minecraft Prometheus Exporter
"""

import time
import argparse
from mcstatus import JavaServer
from prometheus_client import start_http_server, Gauge, Counter

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Minecraft Prometheus Exporter')
parser.add_argument('--host', default='localhost', help='Minecraft server host')
parser.add_argument('--port', type=int, default=25565, help='Minecraft server port')
parser.add_argument('--listen-port', type=int, default=9150, help='Exporter listen port')
args = parser.parse_args()

# Create metrics
PLAYERS_ONLINE = Gauge('minecraft_players_online', 'Number of players currently online')
MAX_PLAYERS = Gauge('minecraft_players_max', 'Maximum player capacity')
LATENCY = Gauge('minecraft_latency_ms', 'Server latency in milliseconds')
VERSION = Gauge('minecraft_version_info', 'Server version information', ['version'])
QUERY_SUCCESS = Counter('minecraft_query_success_total', 'Number of successful server queries')
QUERY_FAILURES = Counter('minecraft_query_failures_total', 'Number of failed server queries')

# Set up server
minecraft_server = JavaServer(args.host, args.port)


# Report metrics
def get_server_stats():
    """Fetch and report server statistics"""
    try:
        # Get server status
        status = minecraft_server.status()

        # Update metrics
        PLAYERS_ONLINE.set(status.players.online)
        MAX_PLAYERS.set(status.players.max)
        LATENCY.set(status.latency)
        VERSION.labels(version=status.version.name).set(1)

        # Try to get player names if query is enabled
        try:
            query = minecraft_server.query()
            # Additional metrics could be added here
            QUERY_SUCCESS.inc()
        except Exception:
            # Query protocol might not be enabled
            pass

    except Exception as e:
        print(f"Error querying Minecraft server: {e}")
        QUERY_FAILURES.inc()


if __name__ == '__main__':
    # Start up the server to expose metrics
    start_http_server(args.listen_port)
    print(f"Minecraft exporter started, listening on port {args.listen_port}")

    # Loop forever collecting metrics
    while True:
        get_server_stats()
        time.sleep(15)  # Update every 15 seconds
