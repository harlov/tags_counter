# Tags counter

REST сервис для подсчета количества html тегов на странице.

Установка.

1. `pip install -r requirements.txt`
2. cp `config/clean/*` в `config/`
3. запустить RabbitMQ и MongoDB (docker-compose up)
4. запуск воркеров - `scripts/run_worker.sh`
5. запуск api - `scripts/run_api.sh`

