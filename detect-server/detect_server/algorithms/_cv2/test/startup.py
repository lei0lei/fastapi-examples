

def start():
    
    message = 'This is test model'
    
    def inference(im,settings):
        print(message)
    
    def release_inference():
        nonlocal message
        del message
        # 强制垃圾回收
        import gc
        gc.collect()
        print('released')
    return inference, release_inference


def post_start():
    '''
    不要在后处理中使用闭包
    '''
    def post_process(im,settings):
        print('This is test model post process')

    return post_process
