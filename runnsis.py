import sys
from ctypes import *

StrLen = 0x10000

class stack_t(Structure):
    def __init__(self, next=None, text=b''):
        self.next = pointer(next) if next else None
        self.text = text

    def push(self, text):
        self.text = text
        top = stack_t(next=self)
        return top

    def pop(self):
        if bool(self.next):
            return self.next[0]
        else:
            return None

stack_t._fields_ = [('next', POINTER(stack_t)), ('text', c_char * StrLen)]

dllPath = sys.argv[1]
dllFn = sys.argv[2]

args = sys.argv[3:]
args.reverse()
stack = stack_t()
for arg in args:
    stack = stack.push(arg.encode())


pluginDll = CDLL(dllPath)
fn = getattr(pluginDll, dllFn)


hProcess = cdll.kernel32.GetCurrentProcess()
usrvars = b'\x00\x00'

fn(hProcess, StrLen, usrvars, pointer(stack), None)

while(True):
    stack = stack.pop()

    if stack is None:
        break
    else:
        print(stack.text)

