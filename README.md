# gcp_automation

Google Cloud Platform에서 Python을 활용해 VM 인스턴스를 생성, 삭제, 시작, 중단을 자동화하고자 하는 프로젝트입니다.

## Docker 설정

- 해당 코드는 도커 환경을 기반으로 작성하였습니다.
- 먼저 도커 이미지를 생성합니다.

```bash
cd scripts
./docker_builder.sh
```

- 도커 이미지가 빌드되었다면, 도커 컨테이너를 실행합니다.
- 이때 `HOST_PATH`에는 절대경로를 입력해주세요.
```bash
./docker_runner.sh
```

## Google Cloud CLI 준비

- VM 인스턴스를 생성, 중단, 시작, 삭제하기 위해서는 Google Cloud CLI가 필요합니다.
- 도커 컨테이너 내에서 `auth.sh`스크립트를 실행해주세요.

```bash
cd /app/scripts
./auth.sh
```

## VM 생성, 삭제, 시작, 중단하기

- 코드를 실행하기 전, 원하는 설정을 `confs/config.yaml`에 등록해주세요.
- 콘솔에 대응하는 옵션에 관한 정보는 해당 [블로그](https://velog.io/@mmodestaa/GCP-VM-%EC%9D%B8%EC%8A%A4%ED%84%B4%EC%8A%A4-%EC%83%9D%EC%84%B1-%EC%82%AD%EC%A0%9C-%EC%8B%9C%EC%9E%91-%EC%A4%91%EB%8B%A8-Python-%EC%BD%94%EB%93%9C) 혹은 구글 공식 문서를 참고해주세요.
- `confs/basic`의 `project_id`는 소속되어 있는 프로젝트 명을 작성해주시고, `vm_name`은 VM 인스턴스명을 작성해주셔야 합니다.

### VM 생성
```bash
cd /app
python3 create_vm.py
```

### VM 삭제
```bash
cd /app
python3 delete_vm.py
```

### VM 시작
```bash
cd /app
python3 start_vm.py
```

### VM 중단
```bash
cd /app
python3 stop_vm.py
```