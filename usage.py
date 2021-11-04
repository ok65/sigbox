
from typing import Any

from sigbox import _Signal, SignalBoxClass, SignalDecorator


class MyClass(SignalBoxClass):

    def __init__(self):
        super().__init__(["start", "stop", "update"])

    @SignalDecorator("start")
    def start(self, a):
        pass

    def update(self, b):
        self.signals.trigger("update", {"b": "stuff"})

    @SignalDecorator("stop")
    def stop(self, exit_code):
        return exit_code


if __name__ == "__main__":

    def start_cb(sig_data):
        print("on start callback")

    def stop_cb(sig_data):
        print(f"on stop callback, code: {sig_data.decorated_return}")

    def update_cb(sig_data):
        print("update")

    myc = MyClass()

    myc.signals.bind("start", start_cb)
    myc.signals.bind("stop", stop_cb)

    myc.start(10)

    myc.stop(20)

    pass