s = 'index.html1'

def is_res(path):
    sub = path[path.rfind('.')+1:len(path)]
    return sub in ['html', 'js', 'css']
print(is_res(s))