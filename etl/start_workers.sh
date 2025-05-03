#!/bin/bash

mkdir -p logs 
mkdir -p run 

start_worker(){
  worker_module=$1
  worker_name=$2
  config_path=$3


  echo "Starting [$worker_name] with config: [$config_path]..."
  python3 -m "$worker_module" --config "$config_path" > "logs/${worker_name}.log" 2>&1 &
  echo $! > "run/${worker_name}.pid"

  echo "[$worker_name] started in the background. Check logs for output."
}


start_worker workers.base_worker "url_worker" config/url_config.yaml
start_worker workers.base_worker "file_worker" config/file_config.yaml


