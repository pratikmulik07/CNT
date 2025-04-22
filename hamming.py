# Function to calculate parity bits and encode data using Hamming (7, 4)
def hamming_encode(data):
    # Data is assumed to be a list of 4 bits
    # Calculating parity bits for Hamming (7, 4)
    p1 = data[0] ^ data[1] ^ data[3]  # Parity bit p1
    p2 = data[0] ^ data[2] ^ data[3]  # Parity bit p2
    p4 = data[1] ^ data[2] ^ data[3]  # Parity bit p4

    # The final encoded data is: p1, p2, d1, p4, d2, d3, d4
    encoded = [p1, p2, data[0], p4, data[1], data[2], data[3]]
    
    # Return encoded data and the parity bits for clarity
    return encoded, (p1, p2, p4)

# Function to detect and correct errors in the received Hamming code
def hamming_correct(received):
    # Calculate the syndrome bits (s1, s2, s4)
    s1 = received[0] ^ received[2] ^ received[4] ^ received[6]  # Check p1
    s2 = received[1] ^ received[2] ^ received[5] ^ received[6]  # Check p2
    s4 = received[3] ^ received[4] ^ received[5] ^ received[6]  # Check p4

    # Print the syndrome bits (s1, s2, s4)
    print(f"Syndrome bits: s1 = {s1}, s2 = {s2}, s4 = {s4}")

    # Error position (if any)
    error_pos = s1 * 1 + s2 * 2 + s4 * 4  # Syndrome decoding
    if error_pos:
        print(f"Error detected at position {error_pos}. Correcting...")
        received[error_pos - 1] ^= 1  # Correct the error by flipping the bit
    else:
        print("No error detected.")

    # Return the corrected 7-bit block and corrected data bits
    return received, (received[2], received[4], received[5], received[6])

# Main function to simulate the encoding, error transmission, and correction
def main():
    # Step 1: Ask the user for a character input
    char = input("Enter a character: ")
    ascii_value = ord(char)  # ASCII value of the entered character
    binary_data = format(ascii_value, '08b')  # Convert to 8-bit binary
    print(f"\nCharacter: '{char}'")
    print(f"ASCII Value: {ascii_value}")
    print(f"Binary Representation: {binary_data}")

    # Step 2: Split the 8-bit binary into two 4-bit parts
    data_part1 = [int(b) for b in binary_data[:4]]  # First 4 bits
    data_part2 = [int(b) for b in binary_data[4:]]  # Last 4 bits

    # Step 3: Encode both 4-bit parts using Hamming (7, 4)
    encoded_part1, parity_bits1 = hamming_encode(data_part1)
    encoded_part2, parity_bits2 = hamming_encode(data_part2)

    # Step 4: Print the first part with parity bits
    print("\nFirst part encoding (4 data bits + 3 parity bits):")
    print(f"Data: {data_part1}")
    print(f"Parity bits: {parity_bits1}")
    print(f"Encoded (7 bits): {''.join(map(str, encoded_part1))}")

    # Step 5: Print the second part with parity bits
    print("\nSecond part encoding (4 data bits + 3 parity bits):")
    print(f"Data: {data_part2}")
    print(f"Parity bits: {parity_bits2}")
    print(f"Encoded (7 bits): {''.join(map(str, encoded_part2))}")

    # Step 6: Combine the two encoded parts to form the final encoded message
    encoded_message = encoded_part1 + encoded_part2
    print(f"\nFinal Encoded Message (14 bits): {''.join(map(str, encoded_message))}")

    # Step 7: Ask the user for the position to introduce an error
    error_pos = int(input("\nEnter the position (1-14) to introduce an error, or 0 for no error: "))

    # Step 8: Simulate the error if a position is provided
    if error_pos != 0:  # If there's an error, flip the chosen bit
        encoded_message[error_pos - 1] = 1 - encoded_message[error_pos - 1]
        print(f"\nError introduced at position {error_pos}. Modified encoded message: {''.join(map(str, encoded_message))}")
    else:
        print("\nNo error introduced.")

    # Step 9: Correct the received message
    print("\nCorrecting first part of the encoded message...")
    corrected_part1, corrected_data1 = hamming_correct(encoded_message[:7])  # Correct the first part
    print("\nCorrecting second part of the encoded message...")
    corrected_part2, corrected_data2 = hamming_correct(encoded_message[7:])  # Correct the second part

    # Step 10: Combine the corrected full 14-bit encoded message
    corrected_full_encoded = corrected_part1 + corrected_part2
    print(f"\nCorrected full 14-bit encoded message: {''.join(map(str, corrected_full_encoded))}")  # <--- ADDED

    # Step 11: Combine the corrected data and convert back to the original character
    corrected_message = ''.join(map(str, corrected_data1 + corrected_data2))
    corrected_ascii = int(corrected_message, 2)
    corrected_char = chr(corrected_ascii)

    print(f"\nCorrected 8-bit binary data: {corrected_message}")
    print(f"Corrected ASCII value: {corrected_ascii}")
    print(f"Corrected character: '{corrected_char}'")

if __name__ == "__main__":
    main()
