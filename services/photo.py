import boto3


def get_last_photos(n=100):
    return [
        "https://www.petmd.com/sites/default/files/what-does-it-mean-when-cat-wags-tail.jpg",
        "https://www.catster.com/wp-content/uploads/2017/08/A-fluffy-cat-looking-funny-surprised-or-concerned.jpg"
    ]


def save_photo(user, photo):
    s3 = boto3.resource('s3')
    s3.Bucket('my-bucket').put_object(Key='test.jpg', Body=photo.stream._file)
