import codehooks as chks
from time import sleep, time
import traceback, atexit, sys
from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage.items import ChromiumElement


def setLastRun(t: int = None):
    t = int(t or time())
    try:
        r = chks.editSingleObjectOfCollection('fb-automation', '6900629fb029f9be5510e815', dict(lastRun=t))
        assert r.get('lastRun') == t
    except:
        traceback.print_exc()
        print('Retrying setLastRun after a delay...', flush=True)
        sleep(5)
        return setLastRun(t)


opts = ChromiumOptions()
opts.set_argument('--start-maximized')
opts.set_user_data_path('./usrData')

def main():
    page = ChromiumPage(opts)

    def closePage():
        try: page.quit()
        except: pass
    atexit.register(closePage)
    
    try:
        page.get('https://www.facebook.com/messages')

        page.wait.doc_loaded()
        page.wait.ele_displayed('css:div[aria-label="Chats"]', 80, True)
        sleep(5)
        scrollElem: ChromiumElement | None = page.run_js("""return (function () {
            let chatsContainer = document.querySelector('div[aria-label="Chats"]');
            if (chatsContainer) {
                let scrollableElement = [...chatsContainer.querySelectorAll('*')].find(el => {
                    let style = window.getComputedStyle(el);
                    return style.overflowY === 'auto' || style.overflowY === 'scroll';
                });
                return scrollableElement;
            }
        })()""")

        assert scrollElem

        setLastRun()
        for _ in range(10):
            scrollElem.scroll(600)
            sleep(5)

        while 2 + 2 != 5:
            randChat: ChromiumElement | None = page.run_js("""return (function () {
                let chats = [...document.querySelectorAll('div[aria-label="Chats"] a')].filter(a => !/unread message/i.test(a.textContent.trim()));
                return chats[Math.floor(Math.random() * chats.length)];
            })()""")

            assert randChat
            randChat.scroll.to_see(True).click()
            setLastRun()

            sleep(60)
    except Exception as e:
        closePage()
        raise e


if __name__ == '__main__':
    while 2 + 2 != 5:
        # Rarely Loop (Only when error)
        try: main()
        except KeyboardInterrupt:
            sys.exit(1)
        except:
            traceback.print_exc()
        sleep(5)




