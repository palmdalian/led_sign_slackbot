import time
from slackclient import SlackClient
import serial
try:
    # Python 2.6-2.7 
    from HTMLParser import HTMLParser
except ImportError:
    # Python 3
    from html.parser import HTMLParser
h = HTMLParser()

ser = serial.Serial(<SERIAL-LOCATION>, 300)
# Pikachu
# ser.write("<ID01><GR>GGGGYBGGGBYGGBBBGGGGGGGYYYYYGGBYYBGGGGGGGYBYBYGBYYBBGGGGGGGYYYYYGBYYBGGGGGGGGRYYYRBBYBGGGGGGGGGGGBYYBYYBGGGGGGGGGGGBYYYYYBGGGG\x0D\x0A")
# Robot
# ser.write("<ID01><GY>GGGGGGGRRRGGGGGGGGGGGGGRRRRRRRGGGGGGGGRGGRRBRBRRGGRGGGGGRGGRRBRBRRGGRGGGGRRRGRRRRRRRGRRRGGRRRRGRRYYYRRGRRRRGGRRRGRRRRRRRGRRRGG\x0D\x0A")
# Mario
# ser.write("<ID01><GY>GGGGGGRRRRRGGGGGGGGGGGGRRRRRRRRBGGGGGGGGGBBBYYBYGGGGGGGGGGGYBYYYBYYBGGGGGGGGGYBBYYYBYYGGGGGGGGGBYYYYBBBBGGGGGGGGGGYYYYYYYGGGGG\x0D\x0A")

slack_client = SlackClient(<API-TOKEN>)

supported_emojis ={
":phone:": "<BA>",
":telephone:": "<BA>",
":glasses:": "<BB>",
":tap:": "<BC>",
":rocket:": "<BD>",
":monster:": "<BE>",
":key:": "<BF>",
":shirt:": "<BG>",
":helicopter:": "<BH>",
":car:": "<BI>",
":tank:": "<BJ>",
":house:": "<BK>",
":home:": "<BK>",
":teapot:": "<BL>",
":fork_and_knife:": "<BM>",
":duck:": "<BN>",
":motorcycle:": "<BO>",
":bike:": "<BP>",
":crown:": "<BQ>",
":pikachu:": "<BR>", # Original is lame. Let's use it for custom graphics
":arrow_right:": "<BS>",
":arrow_left:": "<BT>",
":arrow_lower_left:": "<BU>",
":arrow_lower_right:": "<BV>",
":beer:": "<BW>",
":coffee:": "<BW>",
":chair:": "<BX>",
":robot:": "<BY>", # Original is lame. Let's use it for custom graphics
":wine_glass:": "<BZ>",
":cocktail:": "<BZ>"
}



def write_to_screen(text):
    final = "<ID01>{}\x0D\x0A".format(text)
    print(final)
    ser.write(final)

def replace_emojis(text):
    for k, v in supported_emojis.items():
        if k in text:
            text = text.replace(k, v)
    return text

def fix_text(text):
    text = h.unescape(text)
    # Smart quotes are getting out of control
    text = text.replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u'\u201c', '"').replace(u'\u201d', '"')
    text = text.encode("utf-8")
    return text


def handle_command(message):
    text = ""
    name = ""
    if 'username' in message:
        name = message['username']
    else:
        resp = slack_client.api_call("users.info", user=message['user'])
        if "ok" in resp and resp['ok']:
            name = resp['user']['profile']['display_name']

    fixed_text = fix_text(message['text'])
    fixed_text = replace_emojis(fixed_text)
    spaces = "        " # Extra spaces to strip 
    text = "<CB>{} <CC>-{}{}".format(fixed_text, name, spaces)
    print(text)
    write_to_screen(text)


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and output['channel'] == <SLACK_CHANNEL_ID>:
                # print(output)
                return output
    return None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Handbot connected and running!")
        while True:
            message = parse_slack_output(slack_client.rtm_read())
            if message:
                handle_command(message)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
