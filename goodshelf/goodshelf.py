import submit_shelfie
import shelfie_check_status
import time

def goodshelf(image_path):
    shelfie_info = submit_shelfie.submit_shelfie(image_path)
    time.sleep(10)
    status = shelfie_check_status.shelfie_check_status(*shelfie_info)
    while status != 'success':
        time.sleep(10)
        status = shelfie_check_status.shelfie_check_status(*shelfie_info)
        "still pending!"

if __name__ == "__main__":
    from sys import argv
    script, image_path = argv
    goodshelf(image_path)