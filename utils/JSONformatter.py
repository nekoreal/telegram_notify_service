
ICONS = {
    dict: '📦',
    list: '📋',
    str: '💬',
    int: '#️⃣',
    float: '#️⃣',
    bool: '⚡',
    type(None): '🚫',
    'key': '🔑',
    'last': '└─',
    'not_last': '├─',
    'not_linked': "│   "
}


def string_maxer(
        max_length:int=60,
        is_last:bool=False,
        s:str="",
        prefix:str="",
        indent:int=3,
):
    s = s.replace("\n", " ")
    res=""
    prefix=F'{prefix}{ICONS["not_linked"] if not is_last else ""}'+(" "*indent)
    i=0
    while len(s)>0:
        if i!=0:
            s=prefix+s
        res+=s[:max_length]+'\n'
        s=s[max_length:]
        i+=1
    return res

def value_formatter(
        value:str|float|int|None,
        key=None,
        prefix:str='',
        max_length:int=60,
        is_last:bool=False,

):
    skey = f'{ICONS["key"]}{key}: ' if key  else ''
    res=F'{prefix}{ICONS["last"] if is_last else ICONS["not_last"]}{skey}{ICONS[type(value)]}{value}'
    res = string_maxer(
                    s=res,
                    max_length=max_length,
                    is_last=is_last,
                    prefix=prefix, )
    return res


def list_and_dict_formatter(
        obj:dict|list,
        prefix:str='',
        child_prefix:str='',
        key_name:str|None="Корень",
        max_length: int = 60,
        max_recursion_depth: int = None,
        recursion_depth: int = 0,
        is_last_obj: bool = False,
):
    res=""
    if isinstance(obj, dict) or isinstance(obj, list) :
        s_obj=f"{prefix}{ f"{ICONS["key"]}{key_name}: " if key_name else ""}{ICONS[type(obj)]}{"dict" if type(obj)==dict else "aray"}({len(obj)})"
        s_obj=string_maxer(max_length=max_length,is_last=(False if len(obj)!=0 else True),prefix=child_prefix,s=s_obj,indent=1)
        res=res+s_obj
        if (not obj) or (recursion_depth == max_recursion_depth):
            return res
        last_index=len(obj)-1
        if isinstance(obj,dict):
            for ind, (key, value) in enumerate(obj.items()):
                is_last=(ind == last_index)
                if isinstance(value, dict) or isinstance(value, list):
                    res=res+list_and_dict_formatter(
                        obj=value,
                        prefix=f"{child_prefix}{ICONS['last'] if is_last else ICONS['not_last']  }",
                        child_prefix=f"{child_prefix}{"    " if is_last else ICONS["not_linked"]}",
                        key_name=key,
                        max_length=max_length,
                        max_recursion_depth=max_recursion_depth,
                        recursion_depth=recursion_depth+1,
                        is_last_obj=is_last
                    )
                    if not is_last: res=res+f"{child_prefix}│\n"
                elif type(value) in (int, float, bool, str,type(None)):
                    res=res+value_formatter(
                        value=value,
                        key=key,
                        prefix=child_prefix,
                        is_last=is_last,
                        max_length=max_length,
                    )
                else:
                    res=res+f"{prefix}unreg type {type(value)}\n"
        else:
            for ind,value in enumerate(obj):
                is_last = (ind == last_index)
                if isinstance(value, dict) or isinstance(value, list):
                    res = res + list_and_dict_formatter(
                        obj=value,
                        prefix=f"{child_prefix}{ICONS['last'] if is_last else ICONS['not_last']}",
                        child_prefix=f"{child_prefix}{"    " if is_last else ICONS["not_linked"]}",
                        key_name=None,
                        max_length=max_length,
                        max_recursion_depth=max_recursion_depth,
                        recursion_depth=recursion_depth + 1,
                        is_last_obj=is_last
                    )
                    if not is_last: res = res + f"{child_prefix}│\n"
                elif type(value) in (int, float, bool, str, type(None)):
                    res = res + value_formatter(
                        value=value,
                        key=None,
                        prefix=child_prefix,
                        is_last=is_last,
                        max_length=max_length,
                    )
                else:
                    res = res + f"{prefix}unreg type {type(value)}\n"
    return res


def json_format(
        body:dict|list|None=None,
        max_length:int=45,
        max_recursion_depth:int=None,
):
    if body is None:
        body = {"data": "empty"}
    return list_and_dict_formatter(obj=body,max_length=max_length,max_recursion_depth=max_recursion_depth)