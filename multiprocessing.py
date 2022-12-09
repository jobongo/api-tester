from multiprocessing import Process
import time

def fun():

    print('calling fun')
    time.sleep(2)

def main():

    print('main fun')

    p = Process(target=fun)
    p.start()
    p.join()

    print(f'Process p is alive: {p.is_alive()}')


if __name__ == '__main__':
    main()