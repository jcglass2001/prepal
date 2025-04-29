#!/bin/bash

mkdir -p logs 
mkdir -p run 

start_worker(){
  worker_module=$1
  worker_name=$2

  echo "Starting [$worker_name]..."
  python3 -m "$worker_module" > "logs/${worker_name}.log" 2>&1 &
  echo $! > "run/${worker_name}.pid"

  echo "[$worker_name] started in the background. Check logs for output."
}


start_worker workers.url_worker "url_worker"
start_worker workers.video_worker "video_worker"


