#!/usr/bin/env python
"""Post slack message."""

# https://github.com/os/slacker
# https://api.slack.com/methods
import rospy
import os
import sys
from slacker import Slacker
from rosgraph_msgs.msg import Log
from std_msgs.msg import String


def post_slack():
    """Post slack message."""
    try:
        slack = Slacker('')

        obj = slack.chat.post_message(
            channel='#sara-diagnostics',
            text='I have a major problem with my battery..',
            as_user=True,
            attachments=[{"text": ''}])
        print obj.successful, obj.__dict__['body']['channel'], obj.__dict__[
            'body']['ts']
    except KeyError, ex:
        print 'Environment variable %s not set.' % str(ex)


def callback(data):
    """Post slack message."""
    level = int(data.level)
    if level >= 8:
        try:
            slack = Slacker('')

            obj = slack.chat.post_message(
                channel='#sara-diagnostics',
                text=data.msg,
                as_user=True,
                attachments=[{"text": ''}])
            print obj.successful, obj.__dict__['body']['channel'], obj.__dict__[
                'body']['ts']
        except KeyError, ex:
            print 'API key error. Look in the slack channel "sara-diagnostics" to get the api key or use your own'


def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('logs_listener_to_slack', anonymous=True)
    try:
        slack = Slacker('oxb-231539362580-FCRtOiGtG1ffL8d4YIB2vPq1')

        obj = slack.chat.post_message(
            channel='#sara-diagnostics',
            text="*SARA just woke up* :wm: :sunny:",
            as_user=True,
            attachments=[{"text": ''}])
        print obj.successful, obj.__dict__['body']['channel'], obj.__dict__[
            'body']['ts']
    except:
        sys.stderr.write('API key error. Look in the slack channel "sara-diagnostics" to get the api key or use your own')
        sys.exit(0)

    rospy.Subscriber("rosout_agg", Log, callback)
    rospy.logerr("*SARA just woke up* :wm: :sunny:")
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()
