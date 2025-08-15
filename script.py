import serial
import serial.tools.list_ports


def test_serial_connection(port_name, connection_type):
    """Test connection to MCTC-MIB-A board through specified port"""
    try:
        # Configure serial parameters (adjust according to your device specs)
        ser = serial.Serial(
            port=port_name,
            baudrate=9600,  # Common default baud rate
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=2  # Seconds to wait for response
        )

        print(f"\n{'=' * 50}")
        print(f"Testing {connection_type} connection on {port_name}")
        print(f"Serial configuration: {ser}")

        # Test command (replace with your device's actual command)
        test_command = b"*IDN?\r\n"  # Common identification query

        print(f"Sending command: {test_command.decode().strip()}")
        ser.write(test_command)

        # Read response
        response = ser.readline()
        if response:
            print(f"Received: {response.decode().strip()}")
            print(f"SUCCESS: Valid response from {connection_type} port")
        else:
            print("ERROR: No response from device")

        ser.close()

    except Exception as e:
        print(f"ERROR on {port_name}: {str(e)}")


if __name__ == "__main__":
    print("MCTC-MIB-A Connection Tester")
    print("=" * 50)

    # Detect available ports
    ports = serial.tools.list_ports.comports()
    print("\nAvailable serial ports:")
    for i, port in enumerate(ports):
        print(f"{i + 1}. {port.device} - {port.description}")

    # Test dedicated serial port
    serial_port = input("\nEnter dedicated SERIAL port name (e.g. COM1): ").strip()
    if serial_port:
        test_serial_connection(serial_port, "SERIAL")

    # Test USB serial port
    usb_port = input("\nEnter USB-SERIAL port name (e.g. /dev/ttyUSB0): ").strip()
    if usb_port:
        test_serial_connection(usb_port, "USB-SERIAL")

    print("\nTesting complete. Review output above.")