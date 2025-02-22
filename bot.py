from mail.mail_reader import MailReader

if __name__ == "__main__":
    reader = MailReader()
    reader.connect()
    reader.watch(process_previous_messages=True)