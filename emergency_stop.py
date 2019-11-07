from raspihats.i2c_hats import AI3tcDQ4rly

b = AI3tcDQ4rly(0x70)


value = b.dq.value
if value & 0x01:
    b.dq.value = 0x02
    print('Successfully turned off heating element and started fan!')
elif value & 0x02:
    b.dq.value = 0x00
    print('Successfully turned off fan!')
else:
    print('Nothing to do!')

