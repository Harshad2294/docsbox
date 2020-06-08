# docsbox [![Build Status](https://travis-ci.org/Harshad2294/docsbox.svg?branch=master)](https://travis-ci.org/Harshad2294/docsbox/)  [![Build Status](https://dev.azure.com/harshadshettigar/docsbox-azure/_apis/build/status/Harshad2294.docsbox?branchName=development)](https://dev.azure.com/harshadshettigar/docsbox-azure/_build/latest?definitionId=1&branchName=development)  [![Codacy Badge](https://api.codacy.com/project/badge/Grade/9abb134a1a4340879bd56b6629a07459)](https://www.codacy.com/app/harshad.shettigar/docsbox?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Harshad2294/docsbox&amp;utm_campaign=Badge_Grade)  [![codecov](https://codecov.io/gh/Harshad2294/docsbox/branch/master/graph/badge.svg)](https://codecov.io/gh/Harshad2294/docsbox)

`docsbox` is a standalone service that allows you to convert office documents, like .docx and .pptx, into more useful filetypes like PDF, for viewing it in browser with PDF.js, or HTML for organizing full-text search of document content.  
`docsbox` uses **LibreOffice** (via **LibreOfficeKit**) for document conversion.

```bash
Accepted parameters
Parameter             Accepted value
response_type         json, text, xml
secure_pdf            true, false
filename              <pdf file name>
```
```bash
curl -F "file=@kittens.doc" 'http://localhost/api/v1/?response_type=json&filename=kittens'
{
    "id": "9b643d78-d0c8-4552-a0c5-111a89896176",
    "status": "queued"
}


curl -F "file=@kittens.doc" 'http://localhost/api/v1/?response_type=xml&filename=kittens'
<?xml version='1.0'?>
<root>
    <id>5bd02e2f-7b31-4639-9bcd-b9e18961dacf</id>
    <status>queued</status>
</root>


curl -F "file=@kittens.doc" 'http://localhost/api/v1/?response_type=text&filename=kittens'
cce76d66-54d9-41e3-88f9-8d6affa32dbd


curl -X GET 'http://localhost/api/v1/cce76d66-54d9-41e3-88f9-8d6affa32dbd?response_type=json'
{
    "status": "finished",
    "result_url": "/media/cce76d66-54d9-41e3-88f9-8d6affa32dbd.zip",
    "id": "cce76d66-54d9-41e3-88f9-8d6affa32dbd"
}


curl -X GET 'http://localhost/api/v1/cce76d66-54d9-41e3-88f9-8d6affa32dbd?response_type=text'
finished,/media/cce76d66-54d9-41e3-88f9-8d6affa32dbd.zip


curl -X GET 'http://localhost/api/v1/cce76d66-54d9-41e3-88f9-8d6affa32dbd?response_type=xml'
<?xml version='1.0'?>
<root>
    <id>cce76d66-54d9-41e3-88f9-8d6affa32dbd</id>
    <status>finished</status>
    <result_url>/media/cce76d66-54d9-41e3-88f9-8d6affa32dbd.zip</result_url>
</root>


curl -O http://localhost/media/cce76d66-54d9-41e3-88f9-8d6affa32dbd.zip

unzip -l cce76d66-54d9-41e3-88f9-8d6affa32dbd.zip
Archive:  cce76d66-54d9-41e3-88f9-8d6affa32dbd.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
    11135  2019-08-15 05:31   txt
   373984  2019-08-15 05:31   kittens.pdf
   147050  2019-08-15 05:31   html
---------                     -------
   532169                     3 files
```

```bash
cat options.json
{
  "formats": ["pdf"],
  "thumbnails": {
    "size": "640x480",
  }
}

curl -F "file=@kittens.doc" -F "options=<options.json" 'http://localhost/api/v1/?response_type=json&filename=kittens'
{
  "id": "b82d0081-a0c6-496a-8ea0-910f259bcf6c",
  "status": "queued"
}

curl -X GET 'http://localhost/api/v1/b82d0081-a0c6-496a-8ea0-910f259bcf6c?response_type=json'
{
  "id": "b82d0081-a0c6-496a-8ea0-910f259bcf6c",
  "status": "finished",
  "result_url": "/media/b82d0081-a0c6-496a-8ea0-910f259bcf6c.zip"
}

curl -O http://localhost/media/b82d0081-a0c6-496a-8ea0-910f259bcf6c.zip

unzip -l afb58e2b-78fa-4dd7-b7f9-a64f75f50cb1.zip
Archive:  b82d0081-a0c6-496a-8ea0-910f259bcf6c.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
   374930  2019-08-15 12:34   kittens.pdf
   192077  2019-08-15 12:35   thumbnails/4.png
    22687  2019-08-15 12:35   thumbnails/5.png
   175240  2019-08-15 12:35   thumbnails/1.png
   102748  2019-08-15 12:35   thumbnails/2.png
   125271  2019-08-15 12:35   thumbnails/3.png
   239591  2019-08-15 12:35   thumbnails/0.png
---------                     -------
  1232544                     7 files

```

# API

```
POST (multipart/form-data) /api/v1/filename=kittens&response_type=json
file=@kittens.docx
options={ # json, optional
    "formats": ["pdf"] # desired formats to be converted in, optional
    "thumbnails": { # optional
        "size": "320x240",
    }
}

GET /api/v1/{task_id}&response_type=json
```

# Install
Currently, installation is powered by docker-compose:

```bash
git clone https://github.com/Harshad2294/docsbox.git && cd docsbox
docker-compose build
docker-compose up
```

Services started by Docker:

```bash
CONTAINER ID        IMAGE                 COMMAND                  CREATED             STATUS              PORTS                    NAMES
7ce674173732        docsbox_nginx         "/usr/sbin/nginx"        8 minutes ago       Up 8 minutes        0.0.0.0:80->80/tcp       docsbox_nginx_1
f6b55773c71d        docsbox_rqworker      "rq worker -c docsbox"   15 minutes ago      Up 8 minutes                                 docsbox_rqworker_1
662b08daefea        docsbox_rqscheduler   "rqscheduler -H redis"   15 minutes ago      Up 8 minutes                                 docsbox_rqscheduler_1
0364df126b36        docsbox_web           "gunicorn -b :8000 do"   15 minutes ago      Up 8 minutes        8000/tcp                 docsbox_web_1
5e8c8481e288        redis:latest          "docker-entrypoint.sh"   9 hours ago         Up 8 minutes        0.0.0.0:6379->6379/tcp   docsbox_redis_1
```

# Settings (env)

```
REDIS_URL - redis-server url (default: redis://redis:6379/0)
REDIS_JOB_TIMEOUT - job timeout (default: 10 minutes)
ORIGINAL_FILE_TTL - TTL for uploaded file in seconds (default: 10 minutes)
RESULT_FILE_TTL - TTL for result file in seconds (default: 24 hours)
THUMBNAILS_DPI - thumbnails dpi, for bigger thumbnails choice bigger values (default: 90)
LIBREOFFICE_PATH - path to libreoffice (default: /usr/lib/libreoffice/program/)
```

# Scaling
Within a single physical server, docsbox can be scaled by docker-compose:
```bash
docker-compose up
docker-compose scale web=4 rqworker=8
```
For multi-host deployment, a global syncronized volume need to be created  (e.g. with flocker),a global redis-server and mount it using `docker-compose.yml` file.

# Supported filetypes

| Input                              | Output              | Thumbnails |
| ---------------------------------- | ------------------- | ---------- |
| Document `doc` `docx` `odt` `rtf`  | `pdf` `txt` `html`  | `yes`      |
| Presentation `ppt` `pptx` `odp`    | `pdf` `html`        | `yes`      |
| Spreadsheet `xls` `xlsx` `ods`     | `pdf` `csv` `html`  | `yes`      |
