import submit_shelfie
import shelfie_check_status
import time
import check_for_shelf

def goodshelf(image_path, shelf_name):
    """Given an bookshelf image and a shelf name, will add all books in the image to a corresponding GR shelf, as well as your 'read' shelf."""
    sleep_time = 10
    if check_for_shelf.check_for_shelf(shelf_name):
        pass
    else:
        raise Exception('Something went wrong with creating your shelf.')
    shelfie_info = submit_shelfie.submit_shelfie(image_path, shelf_name)
    time.sleep(sleep_time)
    status = shelfie_check_status.shelfie_check_status(*shelfie_info)
    i = 1
    while status != 'success':
        print "Scan #", i
        print "Scanning..."
        time.sleep(sleep_time)
        status = shelfie_check_status.shelfie_check_status(*shelfie_info)
        i += 1

if __name__ == "__main__":
    from sys import argv
    script, image_path, shelf_name = argv
    goodshelf(image_path, shelf_name)