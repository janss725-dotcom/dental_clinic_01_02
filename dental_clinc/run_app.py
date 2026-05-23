import os
import sys
import streamlit.web.cli as stcli

def resolve_path(path):
    # این تابع مسیر فایل‌ها را در فایل EXE پیدا می‌کند
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, path)
    return os.path.join(os.path.abspath("."), path)

if __name__ == '__main__':
    # این دستور به صورت خودکار برنامه استریم‌لیت تو را اجرا می‌کند
    sys.argv = ["streamlit", "run", resolve_path("app.py"), "--global.developmentMode=false"]
    sys.exit(stcli.main())