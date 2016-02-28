# bqrunner

These are some scripts to test sending commands threw Wifi to an Aquaris BQ 4.5

- runner
    - put this file on the ubuntu phone this is command server via usb at /home/phablet/Documents/
    - edit rc.local and add python /home/phablet/Documents/runner &
    - then reboot the phone or in a terminal do a "sh /etc/rc.local"
    verify the script is running with a ps aux | grep runner
- SMS
    - Edit the file, change the Phone Number like +33612345678 and message to "MESSAGE"
- 888
    - Edit the file, change the Phone Number 888 for Orange FAI
- Test
    - Nothing just send ls -a