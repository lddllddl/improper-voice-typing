#python3.9 -m asyncio

import asyncio# as a 
#import keyboardcontrol_x11 as kc
from pynput import keyboard

from pynput._util.xorg import display_manager

import time

import os

#a = [keyboard.Key.ctrl,keyboard.Key.alt,'h'] #Wrong!
#a = [keyboard.Key.ctrl,keyboard.Key.alt,keyboard.KeyCode.from_char('h')] #Wrong!
#b = keyboard.HotKey.parse('<ctrl>+<alt>+h')
#a == b
#keyboard.Listener.canonical=lambda self,x:x
#hotkey = keyboard.HotKey(
#    #a,
#    #keyboard.HotKey.parse('<ctrl>+<alt>+h'),
#    #[keyboard.Key.ctrl,keyboard.Key.alt,'h'],
#    #[keyboard.Key.ctrl,keyboard.Key.shift,keyboard.KeyCode.from_char('x')],#OK
#    #[keyboard.Key.ctrl,keyboard.Key.shift_l,keyboard.KeyCode.from_char('x')],
#    #[keyboard.Key.ctrl,keyboard.Key.shift_l,keyboard.KeyCode.from_char('X')],
#    #[keyboard.Key.ctrl,keyboard.Key.shift_r,keyboard.KeyCode.from_char('X')],
#    #[keyboard.Key.shift_l,keyboard.Key.shift_r,keyboard.KeyCode.from_char('X')],
#    [keyboard.Key.shift_l,keyboard.Key.shift_r],
#    on_activate)

loops=[None]
listeners=[None]

keys_down = set()
keys_snapshot = set()

import threading
string_handling_lock=threading.Lock()
grand_lock_handling_lock=threading.Lock()
grand_lock=threading.Semaphore(value=2)
shift_lock=threading.Lock() #not really used
#shift_cancelled = {
#    keyboard.Key.shift_l:0,
#    keyboard.Key.shift_r:0,
#}

#hot_tokes

kc = keyboard.Controller()

volatility = [[],[],""]

import tkinter as tk

window = tk.Tk()
window.overrideredirect(True)
#window.geometry("2400x400")
window.wait_visibility(window)
window.wm_attributes('-alpha',0.5)
#https://stackoverflow.com/questions/18394597/is-there-a-way-to-create-transparent-windows-with-tkinter
#window.attributes('-alpha', 0.1)
splash_label= tk.Label(window,
    text= "", #"Hello World!",
    #fg= "green",
    font= ('Droid Sans', 50)
    )#.pack(pady=1)
splash_label.pack()
#splash_label = tx.Text(exportselection=0, font=('Droid Sans', 20))

def center_window(win):
    width = win.winfo_screenwidth()//2 #2400
    height = win.winfo_screenheight()//8 #400
    x = (win.winfo_screenwidth() - width) // 2
    y = (win.winfo_screenheight() - height) // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


async def main():
    import pyppeteer as p
    #kb_out = kc.KeyboardEmulation()
    #kb_in = kc.KeyboardCapture()
    #def kd(s):
    #    print(s)

    #kb_in.key_down=kd;
    #kb_in.suppress_keyboard(['a'])
        
    browser = await p.launch(
        headless = False,
        executablePath = "chromium",
        userDataDir = "/dev/shm/improper-voice-typing-chrome-temporary-profile",
        args= [
            "--window-size=100,100",
            "--start-maximized", #not effective?
        ] , devtools= True
        )
    #await browser._connection
    page = await browser.newPage()
    #page = await (await browser.createIncognitoBrowserContext()).newPage()

    import json
    import pdb
    def cb(x):
        #any exception in this callback seems to hang the whole thread???
        #print('aaaa')
        #print(x)
        #print([j._remoteObject for j in x.args])
        try:
            if (
                ["string","string","object"] ==
                    [j._remoteObject["type"] for j in x.args]
                and "on" ==
                    x.args[0]._remoteObject["value"][:2]
                ):
                #kc.release(keyboard.Key.shift_l)
                #kc.release(keyboard.Key.shift_r)
                print("SSSSSSSSSSSSSSSSSSSSSS")
                xs = [j._remoteObject for j in x.args]
                print("event:",xs[0]["value"])
                caught = json.loads(xs[1]["value"])
                if xs[0]["value"] == "onstart":
                    print("START!")
                    #window.eval('tk::PlaceWindow . center')
                    center_window(window)
                    splash_label.config(text='')
                    window.deiconify() #It is OK called here but not in the keydown callback
                    window.update() # The window does not need to handle user input
                elif xs[0]["value"] == "onspeechstart":
                    print("SNAP!")
                    keys_snapshot.clear()
                    keys_snapshot.update(keys_down)
                elif xs[0]["value"] == "onend":
                    # use lock to move after shift up?
                    with grand_lock_handling_lock:
                        grand_lock.acquire()
                        grand_lock.acquire()
                        try:
                            print("END!")
                            window.withdraw()
                            window.update()
                            #kc.tap(keyboard.Key.caps_lock)

                            s = volatility[2]
                            #caps_on = False # not a very good assumption
                            #end_caps = False # restore caps purely by oddity of caps taps
                            shift_up = True
                            #shift_up = keys_down.isdisjoint([
                            #    keyboard.Key.shift_l,
                            #    keyboard.Key.shift_r]) #inaccurate
                            #assert(not shift_up)
                            for c in s:
                                if ' ' == c: time.sleep(0.005)
                                else: time.sleep(0.003)
                                #shift_up = keys_down.isdisjoint([
                                #    keyboard.Key.shift_l,
                                #    keyboard.Key.shift_r]) #inaccurate
                                is_upper = c.isupper()
                                #desired_caps = bool(is_upper) == bool(shift_up)
                                #if bool(caps_on) != bool(desired_caps):
                                #    kc.tap(keyboard.Key.caps_lock)
                                #    caps_on = not caps_on
                                #    end_caps = not end_caps
                                #    time.sleep(0)
                                if is_upper and shift_up:
                                    kc.press(keyboard.Key.shift)
                                    shift_up = False
                                elif (not is_upper) and (not shift_up):
                                    kc.release(keyboard.Key.shift)
                                    shift_up = True
                                kc.tap(c.lower())
                                #kc.tap(keyboard.Key.backspace)
                            if not shift_up:
                                kc.release(keyboard.Key.shift)
                            #if end_caps:
                            #    time.sleep(0)
                            #    kc.tap(keyboard.Key.caps_lock)
                                
                        finally:
                            grand_lock.release()
                            grand_lock.release()
                elif xs[0]["value"] == "onresult":
                    print(caught['isTrusted'])
                    print(caught['resultIndex'])
                    print(caught['timeStamp'])
                    r = caught['results']
                    print(r["length"])
                    #ignore final flags can be ignored at all
                    areFinals = [r[str(i)]["isFinal"] for i in range(r["length"])]
                    print(areFinals)
                    n_finals = sum(areFinals)
                    assert(all(areFinals[:n_finals]))
                    assert(not any(areFinals[n_finals:]))
                    leftSs = ([r[str(i)]["0"]['transcript'] for i in range(n_finals)])
                    rightSs = ([r[str(i)]["0"]['transcript'] for i in range(n_finals,r["length"])])
                    #leftWs,rightWs = ([s.strip().split(' ') for s in ss] for ss in [leftSs,rightSs]) 
                    leftWs,rightWs = ([w for s in ss for w in s.strip().split(' ') ]
                        for ss in [leftSs,rightSs]) 
                    print(leftWs)
                    print(rightWs)
                    #volatility[0] += leftWs
                    volatility[0] = leftWs
                    volatility[1] = rightWs
                    
                    fs = [
                        lambda x:x, #''
                        lambda x:x.lower(), #'S'
                        lambda x:x.upper(), #'D'
                        lambda x:x.capitalize(),#'SD' #title(),
                    ]
                    
                    gs = [
                        lambda xs:' '.join(xs),
                        lambda xs:''.join(xs),
                        lambda xs:'-'.join(xs),
                        lambda xs:'_'.join(xs),
                        lambda xs:'.'.join(xs),
                    ]
                    hs = [
                        lambda s:s,
                        lambda s:s[:1].upper()+s[1:],
                        lambda s:s[:1].lower()+s[1:],
                    ]
                    code = lambda xs:sum((keyboard.KeyCode.from_char(xs[i]) in keys_snapshot)*2**i
                        for i in range(len(xs)))
                    f = fs[code('SD')]
                    g = gs[min(code('JKL'),len(gs)-1)]
                    h = hs[min(code('FV'),len(hs)-1)]
                    print("GOGOGO")
                    with shift_lock:
                        try:
                            #with display_manager(listeners[0]._display_stop) as dm:
                            #    listeners[0]._suppress_stop(dm)
                            print(volatility[0]+volatility[1])
                            new_string = h(g(map(f,volatility[0]+volatility[1])))
                            #kc.release(keyboard.Key.shift_l)
                            #kc.release(keyboard.Key.shift_r)
                            #invert_case = kc.shift_pressed:
                            #    kc.tap(keyboard.)
                            #print(kc.shift_pressed)
                            old_string = volatility[2]
                            volatility[2] = new_string
                            common_prefix_length = len(os.path.commonprefix([new_string,old_string]))
                            print(old_string)
                            print(new_string)
                            print(common_prefix_length)
                            #print(shift_cancelled)
                            #shift_cancelled[keyboard.Key.shift_l] = 1
                            #shift_cancelled[keyboard.Key.shift_r] = 1
                            #kc.release(keyboard.Key.shift_l.value) #strange silent fatal error!
                            #kc.release(keyboard.Key.shift_r)

                            splash_label.config(text=new_string)
                            splash_label.update()

                            ##kc.tap(keyboard.Key.caps_lock)
                            #for c in old_string[common_prefix_length:]:
                            #    time.sleep(0)
                            #    kc.tap(keyboard.Key.backspace)
                            #    #kc.press(keyboard.Key.backspace)
                            ##kc.release(keyboard.Key.backspace)
                            #s = new_string[common_prefix_length:]
                            #caps_on = False # not a very good assumption
                            #end_caps = False # restore caps purely by oddity of caps taps
                            #shift_up = keys_down.isdisjoint([
                            #    keyboard.Key.shift_l,
                            #    keyboard.Key.shift_r]) #inaccurate
                            #for c in s:
                            #    time.sleep(0)
                            #    #shift_up = keys_down.isdisjoint([
                            #    #    keyboard.Key.shift_l,
                            #    #    keyboard.Key.shift_r]) #inaccurate
                            #    is_upper = c.isupper()
                            #    desired_caps = bool(is_upper) == bool(shift_up)
                            #    if bool(caps_on) != bool(desired_caps):
                            #        kc.tap(keyboard.Key.caps_lock)
                            #        caps_on = not caps_on
                            #        end_caps = not end_caps
                            #        time.sleep(0)
                            #    kc.tap(c.lower())
                            #    #kc.tap(keyboard.Key.backspace)
                            #if end_caps:
                            #    time.sleep(0)
                            #    kc.tap(keyboard.Key.caps_lock)
                                
                            #desired_caps = False
                            #if bool(caps_on) != bool(desired_caps):
                            #    kc.tap(keyboard.Key.caps_lock)
                            #    desired_caps = caps_on
                            #kc.press(keyboard.Key.shift_l)
                            #kc.press(keyboard.Key.shift_r)
                        except Exception as e:
                            print("EEEEE",e)
                        finally:
                            pass
                            #with display_manager(listeners[0]._display_stop) as dm:
                            #    listeners[0]._suppress_start(dm)
                    print("BBBBBBBBBBBBBBBB")
                    #import time
                    #time.sleep(5)
                    #hot_string_new = ''.join(strings)
                    #print(hot_string_new)

                    #new_
                    #for i in range(r["length"]):
                    #    print()
                elif xs[0]["value"] == "onerror":
                    print(json.dumps(caught,indent=1))
                else:
                    pass
            else:
                for j in x.args:
                    ro = j._remoteObject
                    if "string" == ro["type"]:
                        #even caught exceptions seem to hang the thread?
                        try:
                            print("OS",json.dumps(json.loads(ro["value"]),indent=1))
                        except Exception as e:
                            print("E",e)
                            print("S",ro["value"])
                        #print("S",ro["value"])
                    else:
                        print("O",ro)
        except Exception as e:
            print("EEE",e)
        #pdb.set_trace()


    page.on('console',cb)

    await page.evaluate('console.log("[1,2,3]")')
    
    cdp = await page.target.createCDPSession()
    #cdp = browser._connection
    #ref: https://stackoverflow.com/questions/70306563/how-to-grant-permissions-of-geolocation-from-devtools-protocol-monitor
    await cdp.send('Browser.grantPermissions', {
        #'origin': 'about:blank',
        'permissions': ['audioCapture'] })

    with open("injected.js","r") as f:
        ret = await page.evaluate(f.read())

    #ret = await page.evaluate('recognition.start()')


    queue = asyncio.Queue()

    def do(*xs):
        #print('########################',type(x),asyncio.coroutines.iscoroutine(x))
        if 1 == len(xs) and asyncio.coroutines.iscoroutine(xs[0]):
            loops[0].call_soon_threadsafe(queue.put_nowait,xs[0])
        else:
            loops[0].call_soon_threadsafe(queue.put_nowait,*xs)

    def lock_on():
        self = listeners[0]
        keys_down.clear()
        keys_down.add(keyboard.Key.shift_l)
        keys_down.add(keyboard.Key.shift_r)
        #
        with grand_lock_handling_lock:
            grand_lock.acquire()
            grand_lock.acquire()
        if shift_lock.acquire(blocking = False):
            print('ON!')
            try:
                pass
                #kc.release(keyboard.Key.shift_l) #breaks as well
                #kc.release(keyboard.Key.shift_r)
                #r = page.evaluate('console.log(recognition.start())')
                #loops[0].call_soon_threadsafe(queue.put_nowait,(page.evaluate,'console.log("1111")'))
                #loops[0].call_soon_threadsafe(queue.put_nowait,page.evaluate('console.log("1111")'))

                volatility[0] = volatility[1] = []
                volatility[2] = ""
                do(page.evaluate('try{recognition.start();}catch(e){console.log(e);}'))
                with display_manager(self._display_stop) as dm:
                    self._suppress_start(dm)
                #do(lambda :window.deiconify())
                #(r)
            except Exception as e:
                print ( "In lock_on", e)
            finally:
                shift_lock.release()

    def lock_off():
        self = listeners[0]
        try:
            grand_lock.release()
        except Exception as e:
            pass
        try:
            #r = page.evaluate('console.log(recognition.stop())')
            #loops[0].call_soon_threadsafe(queue.put_nowait,(page.evaluate,'console.log("2222")'))
            #loops[0].call_soon_threadsafe(queue.put_nowait,page.evaluate('console.log("2222")'))
            
            #window.withdraw()
            do(page.evaluate('try{recognition.stop();}catch(e){console.log(e);}'))
            print('OFF! 0')
            with display_manager(self._display_stop) as dm:
                self._suppress_stop(dm)
            print('OFF!')
            #(r)
        except Exception as e:
            print ( "In lock_off", e)

    flip = [False]

    def flip_lock():
        if flip[0]:
            lock_off()
        else:
            lock_on()
        flip[0] = not flip[0]

    hotkey = keyboard.HotKey(
        [keyboard.Key.shift_l,keyboard.Key.shift_r],
        #flip_lock
        lock_on) #can't be used to check for release

    def keydown(x):
        keys_down.add(x)
        #if x == keyboard.Key.cmd: lock_on()
        #if x == keyboard.Key.cmd:
        #    if flip[0]:
        #        lock_off()
        #    else:
        #        lock_on()
        #    flip[0] = not flip[0]
        hotkey.press(x)
        #print("DOWN",x)#.__dict__,keys_down)
        print("DOWN",x,keys_down)

    def keyup(x):
        keys_down.discard(x)
        #if x == keyboard.Key.cmd: lock_off()
        if(x in [keyboard.Key.shift_l,keyboard.Key.shift_r]):
            with shift_lock:
                #if {keyboard.Key.shift_l,keyboard.Key.shift_r}.isdisjoint(keys_down):
                #    for k in list(keys_down):
                #        kc.release(k)
                #if shift_cancelled[x]>0:
                #    print('SKIP ONE UP', x)
                #    shift_cancelled[x] -= 1
                #else:
                #    lock_off()
                lock_off()
        hotkey.release(x)
        #print("UP",x)#.__dict__,keys_down)
        print("UP",x,keys_down)

    listeners[0] = keyboard.Listener(
        on_press=keydown,#for_canonical(hotkey.press),
        on_release=keyup,#for_canonical(hotkey.release),
        #suppress = True
        )

    listeners[0].start()

    while True:
        got = queue.get()
        print("GOTTTTTTTTTTTTTTTTTTTTTTTTTTTT",got)
        await (await got)


    #await page.goto('https://example.com')
    #await page.screenshot({'path': 'example.png'})
    #await a.sleep(3)
    #await browser.close()


#try:
loops[0] = asyncio.get_event_loop()
#import signal
#loop.add_signal_handler(signal.SIGTERM, loop.stop)
loops[0].create_task(main())
loops[0].run_forever()#run_until_complete(main())
#except Exception as e:
#    print (e)

