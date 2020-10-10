 docker run -d \
    -p 6379:6379 \
    --name notifier_redis \
    -v ~/dev/vadim_notifier/data:/data \
    redis redis-server