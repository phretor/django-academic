import os

FILEBROWSER_URL_FILEBROWSER_MEDIA = STATIC_URL + "filebrowser/"
FILEBROWSER_PATH_FILEBROWSER_MEDIA = os.path.join(STATIC_ROOT, 'filebrowser')
FILEBROWSER_VERSIONS_BASEDIR = 'thumbs_cache/'
FILEBROWSER_MAX_UPLOAD_SIZE = 31457280
FILEBROWSER_VERSIONS = {
    'fb_thumb': {
        'verbose_name': 'Admin Thumbnail',
        'width': 60,
        'height': 60,
        'opts': 'crop upscale'},

    'home_banner': {
        'verbose_name': 'Homepage banner (627x208px)',
        'width': 627,
        'height': 208,
        'opts': 'crop'},

    'thumbnail': {
        'verbose_name': 'Thumbnail (140px)',
        'width': 140,
        'height': '',
        'opts': ''},

    'small': {
        'verbose_name': 'Small (300px)',
        'width': 300,
        'height': '',
        'opts': ''},

    'medium': {
        'verbose_name': 'Medium (460px)',
        'width': 460,
        'height': '',
        'opts': ''},

    'big': {
        'verbose_name': 'Big (620px)',
        'width': 620,
        'height': '',
        'opts': ''},

    'cropped': {
        'verbose_name': 'Cropped (60x60px)',
        'width': 60,
        'height': 60,
        'opts': 'crop'},

    'person_picture': {
        'verbose_name': 'Person picture (200x200px)',
        'width': 200,
        'height': 200,
        'opts': 'crop upscale'},

    'croppedthumbnail': {
        'verbose_name': 'Cropped Thumbnail (140x140px)',
        'width': 140,
        'height': 140,
        'opts': 'crop'},
}

FILEBROWSER_SELECT_FORMATS = {
    'File': [
        'Image',
        'Document',],

    'Image': [
        'Image'],

    'Document': [
        'Document'],

    'Media': [
        'Video',
        'Audio'],
}
