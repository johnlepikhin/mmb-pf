#!/bin/bash
#
# Postgres db backuper
#
# Help of creation backuper user
# su - postgres
# psql
# CREATE ROLE backuper WITH LOGIN SUPERUSER PASSWORD '123456';
#
# sudo vi /etc/postgresql/11/main/pg_hba.conf
# local  all            backuper                                trust
#
# sudo systemctl restart postgresql
#
# vers 0.1

BACKUP_DIR="/opt/backup/db_backup"
BASE_NAME="mmb_pf"
MAX_DAYS_STORE=60
USERNAME="backuper"

if [[ ! -d "${BACKUP_DIR}" ]] ; then
    mkdir -p ${BACKUP_DIR}
fi

if [[ -n "$1"  ]] ; then
    BASE_NAME=$1
fi

for file_name in $(find ${BACKUP_DIR}/*.${BASE_NAME}.dump.tgz -type f -mtime +${MAX_DAYS_STORE}) ; do
    echo "Remove: ${file_name}"
    rm -f ${file_name}
done

exit_code=0
cd ${BACKUP_DIR}
DUMP_FILE="$(date +%F-%H-%M).${BASE_NAME}.dump"
echo "Dump file name: ${DUMP_FILE}"
pg_dump -f ${BACKUP_DIR}/${DUMP_FILE} -Fc -U${USERNAME} ${BASE_NAME}
if [[ $? -ne "0" ]] ; then
    echo "FAIL: Exitcode from pg_dump non zero [$?]"
    exit_code=1
fi

tar czvf ${BACKUP_DIR}/${DUMP_FILE}.tgz ${DUMP_FILE}
rm -f ${DUMP_FILE}

exit ${exit_code}