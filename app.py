# coding: utf-8
import asyncio
from aiosmtpd.controller import Controller
from email.message import EmailMessage

class CustomSMTPHandler:
    async def handle_DATA(self, server, session, envelope):
        # 处理接收到的邮件
        msg = EmailMessage()
        msg.set_content(envelope.content.decode('utf-8'))
        msg['From'] = envelope.mail_from
        msg['To'] = envelope.rcpt_tos
        msg['Subject'] = 'Forwarded Email'

        # 打印邮件内容或保存到文件
        print(f"Received message from {msg['From']}")
        print(f"Message for {msg['To']}")
        print(f"Message data:\n{msg.get_content()}")

        return '250 Message accepted for delivery'

async def main():
    handler = CustomSMTPHandler()
    controller = Controller(handler, hostname='localhost', port=1025)
    controller.start()

    print("SMTP server is running on localhost:1025")
    try:
        await asyncio.Event().wait()  # 等待直到手动停止
    except KeyboardInterrupt:
        pass
    finally:
        controller.stop()

if __name__ == '__main__':
    asyncio.run(main())