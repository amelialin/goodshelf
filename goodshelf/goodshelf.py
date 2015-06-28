import submit_shelfie
import shelfie_check_status
import time
import check_for_shelf

def goodshelf(image_path, shelf_name):
    if check_for_shelf.check_for_shelf(shelf_name):
        pass
    else:
        raise Exception('Something went wrong with creating your shelf.')
    shelfie_info = submit_shelfie.submit_shelfie(image_path, shelf_name)
    time.sleep(10)
    status = shelfie_check_status.shelfie_check_status(*shelfie_info)
    while status != 'success':
        time.sleep(10)
        status = shelfie_check_status.shelfie_check_status(*shelfie_info)
        "still pending!"

if __name__ == "__main__":
    from sys import argv
    script, image_path, shelf_name = argv
    goodshelf(image_path, shelf_name)