import cv2

DELIMITER = "#####"


def encode_image(image_path, secret_data, output_path):

    # Add delimiter to mark end of message
    data = secret_data + DELIMITER

    # Convert data to binary
    binary_data = ''.join(format(ord(i), '08b') for i in data)

    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("❌ Image not found")

    data_index = 0
    data_length = len(binary_data)

    for row in img:
        for pixel in row:
            for n in range(3):

                if data_index < data_length:

                    # Replace last bit with message bit
                    pixel[n] = int(
                        format(pixel[n], '08b')[:-1] +
                        binary_data[data_index],
                        2
                    )

                    data_index += 1

                else:
                    # Stop encoding when message ends
                    cv2.imwrite(output_path, img)
                    return

    cv2.imwrite(output_path, img)


def decode_image(image_path):

    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("Image not found")

    binary_data = ""
    decoded_data = ""

    for row in img:
        for pixel in row:
            for n in range(3):

                binary_data += format(pixel[n], '08b')[-1]

                # Convert every 8 bits into character
                if len(binary_data) == 8:

                    decoded_data += chr(int(binary_data, 2))
                    binary_data = ""

                    # Stop when delimiter found
                    if decoded_data.endswith(DELIMITER):
                        return decoded_data.replace(DELIMITER, "")

    return decoded_data