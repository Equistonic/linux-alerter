import alerter
import subprocess
import re
import time
from datetime import datetime, timedelta

# Define the threshold for failed login attempts
FAILED_ATTEMPTS_THRESHOLD = 3

# Define the time interval to check logs (in minutes)
CHECK_INTERVAL = 1

# Define the regex pattern to match failed login attempts
FAILED_LOGIN_PATTERN = re.compile(r'Failed password for')

# Functions
def capture_webcam():
    current_time = get_current_time()
    subprocess.run(['fswebcam', '-r', '5', '--jpeg', '95', f'/home/scott/Desktop/projects/linux-alerter/captures/{current_time}'])
    print('Captured that motherfucker')
    return current_time # name of file is current time

# Function to be called after threshold is reached
def get_current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def on_failed_login_attempts(fail_timestamps: list):
    # capture the webcam
    capture_name = capture_webcam()

    # create embeds
    embeds = []
    embeds.append(
        alerter.generate_embed(
            '**Multiple Failed Logins Detected**',
            alerter.hex_to_decimal(alerter.STATUS_COLORS.get('critical')),
            {'name': 'Failed Attempts', 'value': str(get_failed_login_attempts()[0]), 'inline': 'true'},
            {'name': 'Time Checked', 'value': get_current_time(), 'inline': 'true'},
            {'name': 'Timestamps', 'value': '\n'.join(fail_timestamps), 'inline': 'false'},
            {'name': 'Webcam Capture Name', 'value': capture_name, 'inline': 'true'}
        )
    )

    message = alerter.parse_message(
        '',
        '<eq> Alerter',
        embeds
    )

    alerter.post_message(message)

# Function to get the number of failed login attempts from journalctl


def get_failed_login_attempts():
    try:
        timestamp = (datetime.now() - timedelta(minutes=CHECK_INTERVAL)).strftime('%Y-%m-%d %H:%M:%S')

        result = subprocess.run([
            'journalctl',
            '-q',
            'SYSLOG_FACILITY=10',
            'SYSLOG_FACILITY=4',
            f'--since={timestamp}'
        ],
            stdout=subprocess.PIPE
        )

        # Decode the output to string
        output = result.stdout.decode()

        # Now, you can use `output` as input for grep
        try:
            grep_output = subprocess.check_output(['grep', 'password check failed for user'], input=output.encode())
        except subprocess.CalledProcessError as e:
            return [0, []]

        the_list = grep_output.decode().strip().split('\n')
        times_failed = len(the_list)
        fail_timestamps = [output[0:16] for output in the_list]

        return [times_failed, fail_timestamps]
    
    except Exception as e:
        print(f"Error accessing system logs: {e}")
        return [0, []]

# Main monitoring loop


def monitor_failed_logins():
    print("Initializing Login Monitor")
    while True:
        failed_attempts_count = get_failed_login_attempts()
        print(f'Checking for failed attempts. {failed_attempts_count[0]} Detected. [{get_current_time()}]')

        if failed_attempts_count[0] >= FAILED_ATTEMPTS_THRESHOLD:
            print("Too Many Failed Attempts Detected.")
            on_failed_login_attempts(failed_attempts_count[1])

        # Wait for the specified interval before checking again
        time.sleep(CHECK_INTERVAL * 60)


if __name__ == '__main__':
    monitor_failed_logins()
