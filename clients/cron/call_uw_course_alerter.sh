#!/bin/sh

curl -X POST -H 'Cache-Control: no-cache' -H 'Content-Type: application/x-www-form-urlencoded' -d 'email=username%40example.com&session=1165&subject=CS&number=486&level=under' --connect-timeout 20 https://uw-alert.herokuapp.com/check_availability
