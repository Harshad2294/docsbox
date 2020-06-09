import ujson
import datetime
import xml.etree.ElementTree as ET

from magic import Magic
from tempfile import NamedTemporaryFile

from flask import request,Response
from flask_restful import Resource, abort

from docsbox import app, rq
from docsbox.docs.tasks import remove_file, process_document


class DocumentView(Resource):

    def get(self, task_id):
        """
        Returns information about task status.
        """
        queue = rq.get_queue()
        task = queue.fetch_job(task_id)
        if task:
            response_type = request.args['response_type']
            if response_type is not None and response_type == "text" and task.result is not None:
                return Response(task.status+","+task.result,mimetype='text/plain')
            elif response_type is not None and response_type == "text" and task.result == None:
                return Response("processing",mimetype='text/plain')
            elif response_type is not None and response_type == "xml" and task.result is not None:
                xmlstr = "<?xml version='1.0'?>"
                xmlstr+= "<root>"
                xmlstr+= "<id>"+str(task.id)+"</id>"
                xmlstr+= "<status>"+str(task.status)+"</status>"
                xmlstr+= "<result_url>"+str(task.result)+"</result_url>"
                xmlstr+= "</root>"
                return Response(xmlstr,mimetype='text/xml')
            elif response_type is not None and response_type == "xml" and task.result == None:
                xmlstr = "<?xml version='1.0'?>"
                xmlstr+= "<root>"
                xmlstr+= "<status>"+str(task.status)+"</status>"
                xmlstr+= "</root>"
                return Response(xmlstr,mimetype='text/xml')
            elif (response_type is not None and response_type == "json") or (response_type is None):
                resulturl = task.result
                if resulturl == None:
                    resulturl = "-"
                jsonstr = '{'
                jsonstr+= '  "id": "'+str(task.id)+'",'
                jsonstr+= '  "status": "'+str(task.status)+'",'
                jsonstr+= '  "result_url": "'+str(resulturl)+'"'
                jsonstr+= '}'
                return Response(jsonstr,mimetype='application/json')
            else:
                return abort(400, message="Invalid 'response_type' value")
        else:
            return abort(404, message="Unknown task_id")


class DocumentCreateView(Resource):

    def post(self):
        """
        Receives file and options, checks file mimetype,
        validates options and creates a task
        """
        json_response = None
        if "file" not in request.files:
            return abort(400, message="'file' field is required")
        else:
            with NamedTemporaryFile(delete=False, prefix=app.config["MEDIA_PATH"]) as tmp_file:
                filename = request.args['filename']
                response_type = request.args['response_type']
                request.files["file"].save(tmp_file)
                tmp_file.flush()
                tmp_file.close()
                remove_file.schedule(
                    datetime.timedelta(seconds=app.config["ORIGINAL_FILE_TTL"])
                , tmp_file.name)
                with Magic() as magic: # detect mimetype
                    mimetype = magic.from_file(tmp_file.name)
                    if mimetype not in app.config["SUPPORTED_MIMETYPES"]:
                        return abort(400, message="Not supported mimetype: '{0}'".format(mimetype))
                options = request.form.get("options", None)
                if options: # options validation
                    options = ujson.loads(options)
                    formats = options.get("formats", None)
                    if not isinstance(formats, list) or not formats:
                        return abort(400, message="Invalid 'formats' value")
                    else:
                        for fmt in formats:
                            supported = (fmt in app.config["SUPPORTED_MIMETYPES"][mimetype]["formats"])
                            if not supported:
                                message = "'{0}' mimetype can't be converted to '{1}'"
                                return abort(400, message=message.format(mimetype, fmt))
                    thumbnails = options.get("thumbnails", None)
                    if thumbnails:
                        if not isinstance(thumbnails, dict):
                            return abort(400, message="Invalid 'thumbnails' value")
                        else:
                            thumbnails_size = thumbnails.get("size", None)
                            if not isinstance(thumbnails_size, str) or not thumbnails_size:
                                return abort(400, message="Invalid 'size' value")
                            else:
                                try:
                                    (width, height) = map(int, thumbnails_size.split("x"))
                                except ValueError:
                                    return abort(400, message="Invalid 'size' value")
                                else:
                                    options["thumbnails"]["size"] = (width, height)
                else:
                    if mimetype == "application/pdf":
                        options = {
                            "formats": ["html"]
                        }
                    else:
                        options = app.config["DEFAULT_OPTIONS"]
                if "secure_pdf" in request.args and (request.args['secure_pdf']=="True" or request.args['secure_pdf']=="true"):
                    task = process_document.queue(filename, tmp_file.name, options, {
                        "mimetype": mimetype,
                        },True)
                else:
                    if "secure_pdf" in request.args and (request.args['secure_pdf'] not in ["True","true","False","false"]):
                        return abort(400, message="Invalid 'secure_pdf' value")
                    task = process_document.queue(filename, tmp_file.name, options, {
                        "mimetype": mimetype,
                        })
        if response_type is not None and response_type == "text":
            return Response(task.id,mimetype='text/plain')
        elif response_type is not None and response_type == "xml":
            xmlstr = "<?xml version='1.0'?>"
            xmlstr+= "<root>"
            xmlstr+= "<id>"+str(task.id)+"</id>"
            xmlstr+= "<status>"+str(task.status)+"</status>"
            xmlstr+= "</root>"
            return Response(xmlstr,mimetype='text/xml')
        elif response_type is not None and response_type == "json":
            jsonstr = '{'
            jsonstr+= '  "id": "'+str(task.id)+'",'
            jsonstr+= '  "status": "'+str(task.status)+'"'
            jsonstr+= '}'
            return Response(jsonstr,mimetype='application/json')
        else:
            return abort(400, message="Invalid 'response_type' value")
