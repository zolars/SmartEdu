import os
import json
import logging

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for, make_response, send_from_directory)
from werkzeug.exceptions import abort

from app.utils import record_res_history
from app.auth import login_required

bp = Blueprint('files', __name__)


@bp.route('/download/<filetype>/<filepath>')
@login_required
def download(filetype, filepath):
    record_res_history(filepath=filepath,
                       user_ip=request.remote_addr,
                       operation=2)
    directory = os.getcwd()
    filename = ''
    for temp in os.listdir(directory + '/files/' + filetype + '/' + filepath):
        if temp != 'cover.png' and temp != '.DS_Store':
            filename = temp

    response = make_response(
        send_from_directory(directory,
                            './files/' + filetype + '/' + filepath + '/' +
                            filename,
                            as_attachment=True))
    response.headers["Content-Disposition"] = " filename={}".format(
        filename.encode().decode('latin-1'))  # attachment;

    return response


@bp.route('/cover/<filetype>/<filepath>')
def cover(filetype, filepath):
    import base64
    img_stream = ''
    with open('./files/' + filetype + '/' + filepath + '/cover.png',
              'rb') as f:
        img_stream = f.read()
    return img_stream
