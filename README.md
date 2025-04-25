# Korean-tranding

## 1. Build & Up Containers
```shell
## 1. 빌드 (빌드만 따로 하고 싶을 경우) ##
$ docker compose build app

## 2. 자동 빌드 후 컨테이너 띄우기 ##
$ docker compose up # 이미 빌드된 이미지가 있다면, 재빌드 없이
# or
$ docker compose up --build # 명시적으로 빌드 수행
```