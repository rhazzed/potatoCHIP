#########################################
# pickle2reducer.py - NO FRIGGIN CLUE how this code works, but its job is to handle
#                     object-serialization differences between Python 3 and Python2.
#                     This was necessary when server.py and threadtest.py stopped using
#                     a CMD_FILE (file) to communicate robot commands and switched to
#                     using Python multiprocessing "sockets".
#
# HISTORICAL INFORMATION -
#
#  2020-02-09  msipin  Copied verbatim from this URL -
#       https://stackoverflow.com/questions/45119053/how-to-change-the-serialization-method-used-by-the-multiprocessing-module
#########################################

from multiprocessing.reduction import ForkingPickler, AbstractReducer

class ForkingPickler2(ForkingPickler):
    def __init__(self, *args):
        if len(args) > 1:
            args[1] = 2
        else:
            args.append(2)
        super().__init__(*args)

    @classmethod
    def dumps(cls, obj, protocol=2):
        return ForkingPickler.dumps(obj, protocol)


def dump(obj, file, protocol=2):
    ForkingPickler2(file, protocol).dump(obj)


class Pickle2Reducer(AbstractReducer):
    ForkingPickler = ForkingPickler2
    register = ForkingPickler2.register
    dump = dump
