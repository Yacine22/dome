import sys
sys.path.insert(1, './build/')
import pyraspii

print(dir(pyraspii))
print(pyraspii.__doc__)

## Test Communication Protocol 
pyraspii.send_data(2, 0x44)
print(pyraspii.getData_from(0x44))