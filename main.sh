# make new db 
initdb -D teiko_db

# start the serer
pg_ctl -D teiko_db -l logfile start

# make a user
createuser --encrypted --pwprompt lleavitt

createdb -U leeleavitt teiko_db

