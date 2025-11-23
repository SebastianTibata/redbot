#!/bin/sh
# wait-for-db.sh

set -e

host="$1"
port="$2"
shift 2
cmd="$@"

until nc -z "$host" "$port"; do
  >&2 echo "Postgres en $host:$port no está disponible - durmiendo"
  sleep 1
done

>&2 echo "Postgres está disponible - ejecutando comando"
exec $cmd