def start_packet(stream):
    buffer = []
    position = 0
    while True:
        buffer.append(stream.read(1))
        position += 1
        if len(buffer)==5:
            buffer.pop(0)
        if len(buffer)==4:
            print(set(buffer))
            print(len(set(buffer)))
            if len(set(buffer))==4:
                return position


if __name__ == '__main__':
    with open('input.txt', 'r') as data_stream:
        found_packet = start_packet(data_stream)
        print(found_packet)

