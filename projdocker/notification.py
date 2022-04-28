#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import json
import os
from pickle import TRUE
import smtplib
import amqp_setup

monitorBindingKey = "*.notify"

############################### VARIABLES USED ###############################
sender = "Share Share <shareshare@example.com>" # our website "url"
buyer_email = "Buyer <buyer@example.com>" # self.buyeremail
seller_email = "Seller <seller@example.com>" # self.selleremail

############################### EMAIL MESSAGES (GOOGLE PAY SUCCESSFUL) ###############################
# TO BUYER #
message = f"""\
Subject: CONFIRMATION OF ORDER
To: {buyer_email}
From: {sender}

PAYMENT IS SUCCESSFUL.

This is to inform you that your ORDER has been paid successfully and the seller has
been notified. For any further inquiries, contact the seller directly.

Thank you.
"""

# TO SELLER #
message1 = f"""\
Subject: ORDER was placed
To: {seller_email}
From: {sender}

An order was made on Share Share. Go to "View my listings" to view the various orders.

For any further inquiries, contact the buyer directly.

Thank you.

"""

############################### EMAIL MESSAGES (OTHER PAYMENT METHODS) ###############################
# TO BUYER #
message2 = f"""\
Subject: PENDING payment for interested item
To: {buyer_email}
From: {sender}

This is to inform you that the seller has been notified that you will be using their preferred method.
The seller will contact you directly.

Thank you.
"""

# TO SELLER #
message3 = f"""\
Subject: Your listing has a pending payment
To: {seller_email}
From: {sender}

A buyer from your listings would like to make payment through your preferred method, please
liaise with them directly.

Thank you.

"""


def receiveOrderLog():
    amqp_setup.check_setup()

    queue_name = 'Notification'

    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages;
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.


def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived log by " + __file__) #comment out once can get the googlepay email
    orderlist = json.loads(body)

    if orderlist['googlepay'] == TRUE:
        googlepaysuccessful()

    else:
        otherpaymentmethod()    # change

    print() # print a new line feed


def googlepaysuccessful():
    with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
        server.starttls() # secure the connection
        server.login("d309baf5a68328", "751d258b2b4e03")
        server.sendmail(sender, buyer_email, message)
        print("Successfully sent email to buyer")

    with smtplib.SMTP("smtp.mailtrap.io", 587) as server1:
        server1.starttls() # secure the connection
        server1.login("d309baf5a68328", "751d258b2b4e03")
        server1.sendmail(sender, seller_email, message1)
        print("Successfully sent email to seller")

def otherpaymentmethod():
    with smtplib.SMTP("smtp.mailtrap.io", 25) as server2:
        server2.starttls() # secure the connection
        server2.login("d309baf5a68328", "751d258b2b4e03")
        server2.sendmail(sender, buyer_email, message2)
        print("Successfully sent email to buyer")

    with smtplib.SMTP("smtp.mailtrap.io", 465) as server3:
        server3.starttls() # secure the connection
        server3.login("d309baf5a68328", "751d258b2b4e03")
        server3.sendmail(sender, seller_email, message3)
        print("Successfully sent email to seller")



if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveOrderLog()
