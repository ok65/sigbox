
# Library import
import unittest
import importlib

# Project imports
import sigbox


class TestClass(sigbox.SignalBoxClass):
    def __init__(self):
        super().__init__(["apple", "banana", "cherry"])

    @sigbox.SignalDecorator("apple")
    def apple(self, val):
        return val

    @sigbox.SignalDecorator()
    def banana(self, val):
        return val

    def cherry(self, val):
        self.signals.trigger("cherry", {"cherry": val*2})
        return val


class Testing(unittest.TestCase):

    def setUp(self) -> None:
        importlib.reload(sigbox)
        self.sigbox = sigbox.SigBox()
        self.callback_result = []

    def tearDown(self) -> None:
        pass

    def callback(self, data):
        self.callback_result.append(data)

    def test_dual_signal_box(self):
        """
        Test docstring
        """

        def callback(data):
            pass

        sb1 = sigbox.SignalBox()
        sb1.add("box1_sig1")
        sb1.add("box1_sig2")
        sb1.bind("box1_sig1", self.callback)
        sb1.bind("box1_sig2", self.callback)

        sb1.trigger("box1_sig1", {"fruit": "orange"})
        sb1.trigger("box1_sig2", {"fruit": "apple"})

        sb2 = sigbox.SignalBox()
        sb2.add("box2_sig1")
        sb2.add("box2_sig2")
        sb2.bind("box2_sig1", self.callback)
        sb2.bind("box2_sig2", self.callback)

        sb2.trigger("box2_sig1", {"fruit": "pear"})
        sb2.trigger("box2_sig2", {"fruit": "kiwi"})

        self.sigbox.pump()

        check = {"box1_sig1": "orange",
                 "box1_sig2": "apple",
                 "box2_sig1": "pear",
                 "box2_sig2": "kiwi"}

        results = {data.signal.name: data.fruit for data in self.callback_result}

        self.assertDictEqual(check, results)

    def class_setUp(self):
        self.tc1 = TestClass()
        self.tc1.signals.bind("apple", self.callback)
        self.tc1.signals.bind("banana", self.callback)
        self.tc1.signals.bind("cherry", self.callback)

        self.tc2 = TestClass()
        self.tc2.signals.bind("apple", self.callback)
        self.tc2.signals.bind("banana", self.callback)
        self.tc2.signals.bind("cherry", self.callback)

    def class_tearDown(self):
        self.tc1 = None
        self.tc2 = None

    def test_class_decorator_named(self):

        self.class_setUp()

        self.tc1.apple(10)
        self.tc2.apple(20)

        self.sigbox.pump()

        check = {hash(self.tc1.signals): 10, hash(self.tc2.signals): 20}
        results = {}

        for data in self.callback_result:
            results[hash(data.signal.signal_box)] = data.decorator_return

        self.class_tearDown()

        self.assertDictEqual(check, results)


    def test_class_decorator_unnamed(self):

        self.class_setUp()

        self.tc1.banana(11)
        self.tc2.banana(22)

        self.sigbox.pump()

        check = {hash(self.tc1.signals): 11, hash(self.tc2.signals): 22}
        results = {}

        for data in self.callback_result:
            results[hash(data.signal.signal_box)] = data.decorator_return

        self.class_tearDown()

        self.assertDictEqual(check, results)


    def test_class_manual(self):

        self.class_setUp()

        self.tc1.cherry(3)
        self.tc2.cherry(7)

        self.sigbox.pump()

        check = {hash(self.tc1.signals): 6, hash(self.tc2.signals): 14}
        results = {}

        for data in self.callback_result:
            results[hash(data.signal.signal_box)] = data.cherry

        self.class_tearDown()

        self.assertDictEqual(check, results)




