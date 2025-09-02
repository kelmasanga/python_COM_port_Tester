import serial
import serial.tools.list_ports
import time
import os
import sys
from datetime import datetime


class MCTCTester:
    def __init__(self):
        self.ports = []

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        """Print application header"""
        self.clear_screen()
        print("╔══════════════════════════════════════════════════════════╗")
        print("║               MCTC-MIB-A CONNECTION TESTER               ║")
        print("║                 Serial & USB Port Tester                 ║")
        print("╚══════════════════════════════════════════════════════════╝")
        print()

    def detect_ports(self):
        """Detect and list all available serial ports"""
        print("🔍 Scanning for available serial ports...")
        time.sleep(1)
        self.ports = list(serial.tools.list_ports.comports())

        if not self.ports:
            print("❌ No serial ports found!")
            print("   - Check USB cables")
            print("   - Verify drivers are installed")
            print("   - Try rescanning")
            return False

        print(f"✅ Found {len(self.ports)} port(s)")
        return True

    def display_ports(self):
        """Display available ports in a formatted table"""
        if not self.ports:
            print("No ports available")
            return

        print("┌──────┬──────────────┬────────────────────────────────────────────────┐")
        print("│  #   │    Port      │            Description               ──────────│")
        print("├──────┼──────────────┼──────────────────────────────────────┤")

        for i, port in enumerate(self.ports):
            port_num = f"{i + 1}"
            port_name = port.device.ljust(12)
            description = port.description[:40].ljust(40)
            print(f"│ {port_num:4} │ {port_name} │ {description} │")

        print("└──────┴──────────────┴──────────────────────────────────────┘")

    def test_connection(self, port_name, connection_type):
        """Test connection to MCTC-MIB-A board"""
        try:
            print(f"\n📡 Testing {connection_type}: {port_name}")
            print("─" * 50)

            # Configure serial parameters
            ser = serial.Serial(
                port=port_name,
                baudrate=9600,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=2
            )

            # Clear buffers
            ser.reset_input_buffer()
            ser.reset_output_buffer()

            # Test command (adjust based on your device protocol)
            test_command = b"*IDN?\r\n"
            print(f"📤 Sending: {test_command.decode().strip()}")

            ser.write(test_command)
            time.sleep(0.5)

            # Read response
            response = ser.readline()
            if response:
                decoded_response = response.decode().strip()
                print(f"📥 Received: {decoded_response}")

                if decoded_response and len(decoded_response) > 0:
                    print("✅ SUCCESS: Device responded!")
                    result = "SUCCESS"
                else:
                    print("⚠️  WARNING: Empty response")
                    result = "EMPTY_RESPONSE"
            else:
                print("❌ ERROR: No response")
                result = "NO_RESPONSE"

            ser.close()
            return result

        except serial.SerialException as e:
            print(f"❌ SERIAL ERROR: {str(e)}")
            return "SERIAL_ERROR"
        except Exception as e:
            print(f"❌ UNEXPECTED ERROR: {str(e)}")
            return "UNKNOWN_ERROR"

    def test_single_port(self):
        """Test a single port by number or name"""
        self.display_ports()

        if not self.ports:
            input("\nPress Enter to continue...")
            return

        choice = input("\nEnter port number or port name: ").strip()

        if choice.isdigit():
            port_num = int(choice) - 1
            if 0 <= port_num < len(self.ports):
                port = self.ports[port_num]
                self.test_connection(port.device, f"Port {port.device}")
            else:
                print("❌ Invalid port number!")
        else:
            # Direct port name input
            self.test_connection(choice, f"Port {choice}")

        input("\nPress Enter to continue...")

    def test_all_ports(self):
        """Test all available ports"""
        if not self.ports:
            print("❌ No ports to test!")
            input("Press Enter to continue...")
            return

        print("🧪 Testing all available ports...\n")
        results = []

        for port in self.ports:
            result = self.test_connection(port.device, port.description)
            results.append((port.device, result))
            print()
            time.sleep(1)

        # Display summary
        print("📊 TEST SUMMARY:")
        print("─" * 40)
        for port, result in results:
            status = "✅ SUCCESS" if result == "SUCCESS" else "❌ FAILED"
            print(f"{port:15} : {status}")

        input("\nPress Enter to continue...")

    def show_menu(self):
        """Display main menu"""
        self.print_header()

        if not self.detect_ports():
            input("\nPress Enter to rescan...")
            return

        print()
        self.display_ports()

        print("\n" + "═" * 60)
        print("MENU OPTIONS:")
        print("═" * 60)
        print("1. 🔍 Test specific port")
        print("2. 🧪 Test all ports")
        print("3. 🔄 Rescan ports")
        print("4. ⚙️  Settings (baud rate)")
        print("5. ❌ Exit")
        print("═" * 60)

    def run(self):
        """Main application loop"""
        while True:
            try:
                self.show_menu()

                choice = input("\nSelect option (1-5): ").strip()

                if choice == '1':
                    self.test_single_port()
                elif choice == '2':
                    self.test_all_ports()
                elif choice == '3':
                    continue  # Will rescan in next loop
                elif choice == '4':
                    print("\n⚙️  Settings menu coming soon...")
                    time.sleep(1)
                elif choice == '5':
                    print("\n👋 Goodbye!")
                    time.sleep(1)
                    break
                else:
                    print("❌ Invalid choice! Please select 1-5")
                    time.sleep(1)

            except KeyboardInterrupt:
                print("\n\n👋 Application interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                input("Press Enter to continue...")


def main():
    """Main function"""
    tester = MCTCTester()
    tester.run()


if __name__ == "__main__":
    main()