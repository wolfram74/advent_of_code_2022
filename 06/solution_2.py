def start_packet(stream, threshold):
    buffer = []
    position = 0
    while True:
        buffer.append(stream.read(1))
        position += 1
        if len(buffer)==(threshold+1):
            buffer.pop(0)
        if len(buffer)==threshold:
            print(set(buffer))
            print(len(set(buffer)))
            if len(set(buffer))==threshold:
                return position


if __name__ == '__main__':
    with open('input.txt', 'r') as data_stream:
        found_packet = start_packet(data_stream, 14)
        print(found_packet)

