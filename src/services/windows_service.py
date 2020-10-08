from send2trash import send2trash


class WindowsService:
    def __init__(self):
        pass

    def move_to_recycle_bin(self, file_path):
        send2trash(file_path)
