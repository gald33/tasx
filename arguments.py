# NOT IN USE because connection to gcal requires args as well

# Check cmd line arguments

def get_args():
    try:
        import argparse

        flags = argparse.ArgumentParser(description="TasX - Enter title", parents=[tools.argparser])
        flags.add_argument('-t', '--title', help='Event title', required=False)
        flags.add_argument('-f', '--feedback', help='User feedback on task completion', required=False)
        args = flags.parse_args()
        if args.title:
            args['create_new_task_flag'] = True
        else:
            args['create_new_task_flag'] = False
        if args.feedback:
            args['get_user_feedback_flag'] = True
        else:
            args['get_user_feedback_flag'] = False

    except ImportError:
        flags = None
        return None
    return args