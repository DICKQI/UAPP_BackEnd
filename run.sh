#!/bin/bash
case $1 in
    "up")
        # 创建运行日志文件夹
        if [ ! -d "/var/log/utime-log/`date +%Y%m%d`" ];then
            mkdir /var/log/utime-log/`date +%Y%m%d`
        fi
        # 启动UTiime服务命令
        uwsgi --socket :8000 --buffer-size 32768 --daemonize /var/log/utime-log/`date +%Y%m%d`/utime.log --module UTime.wsgi --http-websockets &
        # 加入启动日志
        echo " `date +%Y%m%d%H%M%S` UTime已启动 " >> /var/log/utime-log/start-up-log/start-up.log

        echo "UTime已启动"
    ;;
    "down")
        port=8000
        lsof -i :$port | awk '{print $2}' > tmp
        pid=$(awk 'NR==2{print}' tmp);

        kill -9 $pid

        echo "UTime已经关闭"

        rm tmp
    ;;
    "restart")
        port=8000
        lsof -i :$port | awk '{print $2}' > tmp
        pid=$(awk 'NR==2{print}' tmp);

        kill -9 $pid


        if [ ! -d "/var/log/utime-log/`date +%Y%m%d`" ];then

            mkdir /var/log/utime-log/`date +%Y%m%d`
        fi

        uwsgi --socket :8000 --buffer-size 32768 --daemonize /var/log/utime-log/`date +%Y%m%d`/utime.log --module UTime.wsgi &

        echo " `date +%Y%m%d%H%M%S` UTime重启成功 " >> /var/log/utime-log/start-up-log/start-up.log

        echo "UTime重启成功"

        rm tmp
    ;;
    "initdatabase")
#        python3 manage.py makemigrations account FandQ helps log market chatroom tailwind
        python3 manage.py makemigrations Account Log Tailwind ChatRoom FandQ

        python3 manage.py migrate

        echo "初始化项目数据库成功"
    ;;
    "makemigrations")

        python3 manage.py makemigrations ${@:2}
#        echo ${@:2}
    ;;
    "migrate")
        python3 manage.py migrate
    ;;
    "createsuperuser")
        python3 manage.py createsuperuser
    ;;
    "log")

        tail -f /var/log/utime-log/`date +%Y%m%d`/utime.log
    ;;
    "backup")
#        nowtime= date +"%Y-%m-%d"

        mysqldump -u root -p Utime > /home/database-backup/utime_database_backup.sql
    ;;
    # "clearlog")
    #     sudo rm /var/log/Utime.log
    #     echo "日志已清除"
    # ;;
    *)
        echo "unknown command"
    ;;
esac