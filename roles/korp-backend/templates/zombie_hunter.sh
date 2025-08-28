#!/usr/bin/env bash

MEMORY_LIMIT_GB={{ gunicorn_worker_max_mem_gb }}
MEMORY_LIMIT_KB=$((MEMORY_LIMIT_GB * 1024 * 1024))

ps -eo pid,comm,rss --no-headers | grep gunicorn | while read pid comm rss; do
    if [ "$rss" -gt "$MEMORY_LIMIT_KB" ]; then
        gib=$(awk "BEGIN {printf \"%.2f\", $rss/1048576}")
        echo $(date)": Killing gunicorn process $pid using ${gib}GB of memory" >> {{ zombie_hunter_logfile }}
        kill -TERM "$pid"
        sleep 1
        # If TERM doesn't work, use KILL after a delay
        if kill -0 "$pid" 2>/dev/null; then
            sleep 5 && kill -KILL "$pid" 2>/dev/null &
            echo $(date)":  gunicorn process $pid was unresponsive, had to kill -9" >> {{ zombie_hunter_logfile }}
        fi
    fi
done
