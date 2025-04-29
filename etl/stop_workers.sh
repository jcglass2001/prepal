#!/bin/bash

stop_worker(){
  pid_file=$1
  worker_name=$2

  if [ -f "$pid_file" ]; then
    pid=$(cat "$pid_file")

    if kill -0 "$pid" 2>/dev/null; then
      kill -9 "$pid"
      echo "[$worker_name] (PID $pid) stopped."
    else
      echo "[$worker_name] (PID $pid) not running. Cleaning up directory..."
      rm "$pid_file"
    fi 
  else
    echo "[$worker_name] No PID file found"
  fi 
}

stop_worker run/url_worker.pid "url_worker"
stop_worker run/video_worker.pid "video_worker"
