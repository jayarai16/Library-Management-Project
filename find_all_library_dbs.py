import pathlib
base = pathlib.Path(r'C:/Users/hp/Desktop/lib')
print('Searching under', base)
for p in base.rglob('library.db'):
    print(p)
