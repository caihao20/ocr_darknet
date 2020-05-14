export LANG=zh_CN.UTF-8

export RUN_PATH="/Users/ss/workspace/python/web/ocr" #"/data/PRG/ocr" 

export PRG_KEY="8009"

cd $RUN_PATH

case "$1" in
    start)
        pid=`ps -ef|grep ":${PRG_KEY}"|awk '/python/{print $2}'`
        if [[ "x" != "x"${pid} ]]; then
            echo "pid file exists"
            exit 1
        fi

        nohup python3 manage.py runserver 0:$PRG_KEY --noreload >> logs/start.log 2>&1 &
        echo "$PRG_KEY started, please check log."

        ;;

    stop)
        pid=`ps -ef|grep ":${PRG_KEY}"|awk '/python/{print $2}'`
        if [[ $pid -gt 0 ]]; then
            pgrep -f ${PRG_KEY}|xargs kill -9    
            echo "$PRG_KEY stoped!"
        else
            echo "$PRG_KEY not found, nothing to stop!"
        fi

        ;;

    restart)
        $0 stop
        sleep 1
        $0 start

        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
esac

exit 0


