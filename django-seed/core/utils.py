import re
import json
import threading

def divide_work(handle, datas, datas_length, max_item, thread_done=None):
    for pointer in range(0, datas_length, max_item):
        sub_datas = datas[pointer:pointer + max_item]
        worker_thread = threading.Thread(target=handle, args=(sub_datas,))
        worker_thread.start()
        worker_thread.join()
        if thread_done and hasattr(thread_done, '__call__'):
            thread_done()


def json_from(data):
    def default(o):

        if isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, ObjectId):
            return str(o)

    return json.dumps(data, default=default)


def convert_camel_case_to_kebab_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()