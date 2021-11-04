
# Library import
from typing import Optional

# Project imports
from sigbox.signal_box import SignalBoxClass
from sigbox.signal_data import DecoratedSignalData


class SignalDecorator:
    def __init__(self, signal_name: Optional[str] = None):
        self.signal_name = signal_name

    def __call__(self, func):
        def newf(*args, **kwargs):

            # Throw exception if the decorator is used with a class that doesn't inherit SignalBoxClass
            if not issubclass(type(args[0]), SignalBoxClass):
                raise Exception("Parent class must inherit from SignalBoxClass")

            # Use function name if signal named not specified
            self.signal_name = self.signal_name if self.signal_name else func.__name__

            # Call the decorated method
            ret = func(*args, **kwargs)

            # Get signal instance
            signal = args[0].signals.get(self.signal_name)

            # Prepare signal data
            sig_data = DecoratedSignalData(signal=signal, data={"decorator_return": ret},
                                           decorated_method=func.__name__, decorated_return=ret)

            # Trigger the signal
            args[0].signals.trigger(self.signal_name, signal_data=sig_data)

            # Return the decorator's return value
            return ret

        # Return the decorated function
        return newf