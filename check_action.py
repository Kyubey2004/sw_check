import os
import time
import smtplib
from email.mime.text import MIMEText


def find(path,need):
    today = time.strftime("%Y-%m-%d")
    find_list=[]
    target_size = 0  # 只记录目标文件大小
    for root, dirs, files in os.walk(path):
        for file in files:

            full_path = os.path.join(root, file)
            file_time = time.localtime(os.path.getmtime(full_path))
            file_date = time.strftime("%Y-%m-%d", file_time)
            file_size = os.path.getsize(full_path)
            if file == need or file.startswith(f'{need}.'):
                target_size = file_size
            if (file == need or file.startswith(f'{need}.')) and file_date == today and file_size >= 1024000:
                find_list.append(file)

    return find_list,target_size

def send_email(title,content, receiver_list=None):
    if not receiver_list:
        receiver_list = ["qwertyliyue@163.com"]
    smtp_server = "smtp.163.com"#服务器
    smtp_port = 25#端口号
    smtp_username = "qwertyliyue@163.com"
    smtp_password = "PXTJnishcKdUui3B"
    # sender = "qwertyliyue@163.com"
    try:
        for receiver in receiver_list:
            # 写
            email=MIMEText(content, "plain", "utf-8")
            email['from']=smtp_username
            email["To"] = receiver
            email["Subject"] = title
    #         发
            service=smtplib.SMTP(smtp_server,smtp_port)
            service.login(smtp_username,smtp_password)
            service.sendmail(smtp_username,receiver,email.as_string())
            service.quit()
    except:
        print('Failed to send')

def main():
    # path = input("文件路径")
    # need = input('文件名')
    path=r'E:\projects\pythonprojects\southwest\Data'
    need='southwest_temp_flight_20'
    result,target_size = find(path,need)
    if result :
        send_email(f'存在{need}','成功')
    else:
        try:
            receiver_list = ["qwertyliyue@163.com",
             'zx9622223renfu745@163.com']
            send_email(f"{need[0:8]}的大小为{target_size / 1024:.2f} KB", "0.00kb就是没有今天的文件\n今天的内容小于1000kb", receiver_list=receiver_list)
        #     如果文件大小正常还fail就是今天的文件不存在
        except:
            send_email(f"{need} not exist", "fail")
            # send_email2(f"不存在{need}", "没有今天的文件")


if __name__ == '__main__':
    main()
    while True:
        now = time.strftime("%H:%M")
        if now == "12:00" or now == "12:01":
            main()
            time.sleep(120)
        time.sleep(20)
